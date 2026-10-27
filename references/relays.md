# Optional local relay

A relay is optional infrastructure for a concrete unsupported operation, not part of installing the skill. Do not run a server or grant access during discovery. First test whether an existing supported connector, browser tool, manual export or short file-picker handoff solves the gap.

If a relay is needed, propose its exact operations, origin, filesystem roots, credential storage, startup behavior, expiration, logs and shutdown command. Explain what the agent can read/write. Obtain applicable approval before new access, installations, persistent background execution or public exposure. The user's request to create this skill does not approve those steps for everyone who installs it.

Prefer an established host-supported relay with current official documentation. Verify publisher and source before installation. Default to loopback-only, OS-user ownership, explicit origin checks, authentication, bounded operations and paths, no arbitrary shell endpoint, no credential-return endpoint, no public tunnel, and least privilege. Do not store tokens in the skill, repository, URLs, logs or plain JSON. Use OS/host credential storage and references. Require protection against path traversal, symlink escapes, cross-site requests and replay before enabling writes.

Start with read-only listing of one authorized course or test directory. Verify actual account, operation and returned data without echoing secrets. Test denial outside allowed roots/origins. Only expand to the user's specifically requested upload/submission scope after approval. Use operation IDs, file hashes, bounded retries and server reconciliation. Confirm a kill switch and remove startup persistence on cancellation.

Do not manufacture a generic bridge to bypass school controls, MFA, CAPTCHAs, admin consent, or missing platform permissions. If the environment cannot safely provide a relay, document the gap and offer a manual handoff. Never present relay instructions as a shipped or tested service.
