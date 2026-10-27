import copy
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from datetime import datetime, timezone

spec = importlib.util.spec_from_file_location('pilot', Path(__file__).parents[1]/'scripts/assignment_pilot.py')
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)


class Controls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name)/'answer.txt'
        self.file.write_text('checked answer')
        self.state = {
            'schemaVersion': 1, 'courseId': 'course-a', 'assignmentId': 'task-a',
            'authorization': {'courseId': 'course-a', 'assignmentId': 'task-a', 'actions': ['upload', 'submit']},
            'verified': True, 'accountConfirmed': True, 'submissionHold': False,
            'serverCheckedAt': '2026-10-27T17:38:00+00:00', 'serverState': 'not-submitted',
            'files': [{'path': str(self.file), 'sha256': hashlib.sha256(self.file.read_bytes()).hexdigest()}],
            'window': {'start': '2026-10-27T10:35:00-07:00', 'end': '2026-10-27T10:45:00-07:00'}
        }
        self.now = datetime(2026,10,27,17,40,tzinfo=timezone.utc)

    def check(self, action='submit'):
        return pilot.check_action(self.state, action, self.now)

    def test_valid_and_timezone_conversion(self):
        self.assertEqual(self.check(), [])

    def test_hold_blocks_submit_but_allows_upload(self):
        self.state['submissionHold'] = True
        self.assertTrue(self.check())
        self.assertEqual(self.check('upload'), [])

    def test_missing_authorization(self):
        del self.state['authorization']
        self.assertTrue(self.check())

    def test_upload_only_not_submission(self):
        self.state['authorization']['actions'] = ['upload']
        self.assertTrue(self.check())

    def test_scope_mismatch(self):
        self.state['authorization']['assignmentId'] = 'task-b'
        self.assertTrue(self.check())

    def test_changed_file_invalidates_verification(self):
        self.file.write_text('new answer')
        self.assertTrue(self.check())

    def test_window_end_excluded(self):
        self.now = datetime(2026,10,27,17,45,tzinfo=timezone.utc)
        self.assertTrue(self.check())

    def test_naive_time_denied(self):
        self.state['window']['start'] = '2026-10-27T10:35:00'
        self.assertTrue(self.check())

    def test_stale_server_check(self):
        self.state['serverCheckedAt'] = '2026-10-26T17:38:00+00:00'
        self.assertTrue(self.check())

    def test_already_submitted_not_repeated(self):
        self.state['serverState'] = 'submitted'
        self.assertTrue(self.check())

    def test_missing_file_and_unverified_denied(self):
        self.state['verified'] = False
        self.file.unlink()
        self.assertTrue(self.check())

    def test_unknown_action_and_paused(self):
        self.assertTrue(self.check('delete'))
        self.state['paused'] = True
        self.assertTrue(self.check('upload'))

    def test_no_authorization_in_template(self):
        self.assertEqual(pilot.initial_state()['authorization']['actions'], [])
        self.assertTrue(pilot.initial_state()['submissionHold'])


if __name__ == '__main__':
    unittest.main()
