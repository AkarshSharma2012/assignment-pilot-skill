# Assignment Pilot

A portable agent skill for managing assignment workflows across learning platforms. It discovers available connections, organizes original files and completed work, verifies outputs, and follows separate preparation, upload and submission permissions.

## Start

Copy the `assignment-pilot` skill folder (or this repository's contents inside a folder named `assignment-pilot`) into your agent's supported skills directory. For Codex, that is normally `~/.codex/skills/assignment-pilot/`. Reload skill discovery as required by your host. No dependencies or account connections are installed automatically.

Ask: **“Use Assignment Pilot to set up my school platforms. Prepare my assignments for review, but don't submit anything.”**

It checks your actual tools, helps you sign in through supported flows, asks for missing class/schedule preferences, and explains what it has tested. Autopilot is not required. Without skill support, ask your agent to read `SKILL.md` and its relevant references. Slash-command syntax depends on the host.

## Examples

- “Check Teams and Classroom for new assignments.”
- “Prepare these worksheets, preserving the teacher's layout.”
- “Upload the verified files, but leave them unsubmitted.”
- “Submit only the assignments I approved in this class before 3 PM.”
- “Pause submissions for this assignment.”
- “Monitor feedback and tell me what remains ungraded.”

## Connections and limits

The discovery guide covers Teams, Google Classroom, Khan Academy, Canvas, Moodle, Schoology, Blackboard, Brightspace, document storage, gradebooks and other learning systems. **This release contains no live platform adapters, bundled connector or relay server.** Platform operations depend on the agent host, institution, role, login and available permissions; each is untested until verified in your environment. Khan-style practice/progress is not equivalent to uploading a worksheet. Restricted assessments are handled through permitted tutoring, not unattended test-taking.

Prefer supported connectors, then background browser control. Optional relay guidance helps the agent propose a scoped setup when needed. It does not bypass account controls. No paid service is mandatory.

The skill is instructions for an agent, not a standalone application or background daemon. Schedules require a working host scheduler and availability. It cannot guarantee grades, accepted late work, or execution while your device or session is unavailable.

## Private state and execution checks

Keep `.assignment-pilot/` outside this public package and out of source control. Never publish credentials, account/course identifiers, school files, output receipts or screenshots. Export only sanitized configuration templates. Each user's authorization is established separately.

Optional Python 3.10+ helper (standard library only):

```
python scripts/assignment_pilot.py init --root /path/to/private-project
python scripts/assignment_pilot.py check /path/to/private-project/.assignment-pilot/state.json --action submit
python -m unittest discover -s tests -v
```

`init` creates a default-deny local example. `check` checks that example's action policy; it does not connect accounts, confirm remote status, or execute an action. The agent must supply verified live state and apply host permissions. A human-editable JSON file is not a security boundary.

## Repository scope

Public skill, references and local helper only. No telemetry, account collection, automatic installs or external writes. MIT licensed. See [SKILL.md](SKILL.md) for operation and [the platform guide](references/platforms.md) for discovery targets.
