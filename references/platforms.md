# Platform discovery and connection tests

These are discovery targets, not bundled adapters or verified integrations. Do not claim a platform works merely because it appears here. Select tools actually exposed on the current host. Consult current official platform documentation before implementing an API route or relying on changing product behavior.

| Platform or source | What to establish live |
| --- | --- |
| Microsoft Teams for Education | School tenant/account, class and assignment IDs, reference files versus My work, separate attach and Turn in operations, actual grade/feedback source |
| Google Classroom | Correct Google/school account, course/coursework IDs, teacher references versus student work, attachment and submission permissions separately |
| Khan Academy | Learner versus teacher role, class assignments and progress visibility, whether the task is practice or an assessment; do not equate watched content with mastery |
| Canvas | Institution domain, enrollment and assignment IDs, allowed submission types, attempt limits and course policy |
| Moodle | Institution/version, course/module/task identity, draft versus submitted status, file limits and supported web services if available |
| Schoology | Institution account, course/material identity, attachments and attempt/submission semantics |
| Blackboard Learn | Institution/course identity, Original/Ultra interface, attempt and final-submit distinction |
| D2L Brightspace | Institution/course/assignment identity, submission folder, receipt and rubric visibility |
| PowerSchool/StudentVUE/ParentVUE | Read-only grade evidence and assignment matching; do not assume these are submission destinations |
| Google Drive/Docs or OneDrive/Word | Original ownership and permissions, file versus native document formats, private staging and export fidelity |
| Gradescope, Code.org, CodeHS, IXL, ALEKS, Pearson, McGraw Hill | Current institution access, assignment type, assessment restrictions and supported operations; no generic completion automation claim |
| Email or teacher file portal | Explicit destination and accepted formats, exact submission instructions; do not guess that email or a network folder earns credit |
| Other platform | Use the same capability probe; ask for the portal URL when required and report unsupported operations honestly |

Connection ladder: existing authorized connector → supported signed-in browser → user export/manual handoff → scoped local relay if it solves a concrete gap. Prefer the least invasive working route. An account expansion or admin consent requires the host's applicable approval. Installing this skill grants nothing.

Each new route needs an evidence record: platform/domain, account alias, course ID, operation, status, tested timestamp, visible proof, limitation and fallback. Do not persist session tokens or signed URLs. Read/download proof never proves upload/submit access. For a write test, prepare a concrete requested artifact and use the actual authorized assignment; do not create fake submissions in a real class.

For Microsoft file-picker failures, one possible route is private OneDrive staging followed by Teams Cloud files attachment. Verify upload success and file identity first; chooser success alone is insufficient. This is a fallback to test, not a universal fix. Use supported download events and confirm actual file contents; downloads may arrive after a browser-event timeout.
