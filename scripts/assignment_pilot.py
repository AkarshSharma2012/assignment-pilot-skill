"""Local eligibility checker. No network access, credentials, or submissions."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys


def initial_state():
    return {
        'schemaVersion': 1, 'courseId': '', 'assignmentId': '',
        'authorization': {'courseId': '', 'assignmentId': '', 'actions': []},
        'verified': False, 'accountConfirmed': False, 'submissionHold': True,
        'paused': False, 'files': [], 'serverState': 'unknown',
        'serverCheckedAt': None, 'window': None,
    }


def aware_time(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError('Timestamp must include a UTC offset')
    return result


def check_action(state, action, now=None):
    """Return denial reasons. Caller must still verify live scope and host policy."""
    reasons = []
    if not isinstance(state, dict):
        return ['State must be an object']
    if action not in ('upload', 'submit'):
        return ['Only upload and submit are supported']
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None or now.utcoffset() is None:
        return ['Current time must include a UTC offset']
    if state.get('schemaVersion') != 1:
        reasons.append('Unsupported state schema')
    if state.get('paused') is not False:
        # Missing pause field is allowed for older minimal v1 records.
        if state.get('paused', False) is not False:
            reasons.append('Workflow paused or invalid pause state')
    auth = state.get('authorization')
    if not isinstance(auth, dict):
        auth = {}
    actions = auth.get('actions')
    if not isinstance(actions, list) or action not in actions:
        reasons.append('Action not explicitly authorized')
    for key in ('courseId', 'assignmentId'):
        if not isinstance(state.get(key), str) or not state[key] or auth.get(key) != state[key]:
            reasons.append('Authorization scope mismatch: ' + key)
    if action == 'submit' and state.get('submissionHold') is not False:
        reasons.append('Submission hold is active or unspecified')
    if state.get('accountConfirmed') is not True:
        reasons.append('Live destination account not confirmed')
    if state.get('verified') is not True:
        reasons.append('Outputs not verified')
    files = state.get('files')
    if not isinstance(files, list) or not files:
        reasons.append('No output files')
    else:
        for entry in files:
            try:
                if not isinstance(entry, dict):
                    raise ValueError('Invalid file record')
                path = Path(entry['path'])
                if not path.is_absolute():
                    raise ValueError('File paths must be absolute')
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if digest != entry.get('sha256'):
                    reasons.append('Output changed since verification: ' + path.name)
            except (OSError, KeyError, TypeError, ValueError):
                reasons.append('Output missing or invalid')
    try:
        checked = aware_time(state['serverCheckedAt'])
        age = (now - checked).total_seconds()
        if not 0 <= age <= 300:
            reasons.append('Live server reconciliation is stale or future-dated')
    except (KeyError, TypeError, ValueError, AttributeError):
        reasons.append('Live server reconciliation missing or invalid')
    server = state.get('serverState')
    if server not in ('not-submitted', 'attached'):
        reasons.append('Server state unknown, already submitted, or requires explicit revision workflow')
    window = state.get('window')
    if action == 'submit' and window is not None:
        try:
            start, end = aware_time(window['start']), aware_time(window['end'])
            if not start <= now < end:
                reasons.append('Outside authorized submission window')
        except (KeyError, TypeError, ValueError, AttributeError):
            reasons.append('Submission window invalid')
    return reasons


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init', help='Create private default-deny state without overwriting')
    init.add_argument('--root', type=Path, required=True)
    check = sub.add_parser('check', help='Check local action eligibility; performs no external action')
    check.add_argument('state', type=Path)
    check.add_argument('--action', choices=('upload', 'submit'), required=True)
    check.add_argument('--now', help='Aware ISO timestamp for deterministic checks')
    args = parser.parse_args(argv)
    try:
        if args.command == 'init':
            folder = args.root.resolve()/'.assignment-pilot'
            folder.mkdir(parents=True, exist_ok=True)
            with (folder/'state.json').open('x', encoding='utf-8') as f:
                json.dump(initial_state(), f, indent=2)
                f.write('\n')
            # A private directory remains local even inside a Git project.
            (folder/'.gitignore').write_text('*\n', encoding='utf-8')
            print(folder/'state.json')
            return 0
        state = json.loads(args.state.read_text(encoding='utf-8-sig'))
        now = aware_time(args.now) if args.now else None
        reasons = check_action(state, args.action, now)
        print(json.dumps({'eligible': not reasons, 'action': args.action, 'reasons': reasons}, indent=2))
        return 2 if reasons else 0
    except (OSError, ValueError, TypeError) as error:
        print('Error: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
