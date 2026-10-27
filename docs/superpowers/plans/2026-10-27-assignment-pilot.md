# Assignment Pilot Implementation Plan

> For agentic workers: implement inline using superpowers:executing-plans. The user approved design and build; do not repeat the approval gate.

**Goal:** Deliver a portable, public assignment automation skill with truthful connection discovery and explicit upload/submission controls.

**Architecture:** A concise skill routes to setup, platform, workflow, and relay references. A dependency-free Python helper checks local execution policy; it does not connect accounts or execute submissions. Runtime private data lives outside the package.

**Tech Stack:** Markdown, YAML, Python 3.10+, standard library, GitHub repository.

**Spec:** Approved workspace work/assignment-pilot-design.md; public requirements captured in README and skill references.

## Global constraints

No mandatory paid service. No school data or secrets in the repository. Installing a skill does not connect accounts. Explicit upload-only holds override prior submission schedules. Never equate upload/submission/grade.

## Review focus

Missing authorization must fail closed. Holds survive restarts. Changed files invalidate verification. Time windows use aware timestamps and exclude end time. Relays must not broaden access silently.

## Tasks

- [x] Write skill and progressive references; verify relative links and public scope.
- [x] Write failing tests for authorization, holds, stale hashes, course mismatch, time windows, and duplicate submission.
- [x] Implement `check_action(state, action, now) -> list[str]` and `init`/`check` CLI; run tests.
- [x] Review docs and code; fix material findings, validate skill, scan for private data.
- [x] Install locally, create ZIP, commit, and publish public GitHub repository at user's explicit request. Verify remote contents and URL.

## Execution record

Initial test run failed because the helper did not yet exist. Implemented it; all 13 tests passed. Independent read-only review found no material issues. Bytecode and private state are excluded from packaging. Platform connections and relay deployment remain intentionally untested and are documented as such.

Skill validator and relative-link checks passed. CLI initialization, default-deny eligibility and no-overwrite checks passed. Installed core package, built ZIP, published public repository, and verified remote file listing. Public package contains no school artifacts or private state.
