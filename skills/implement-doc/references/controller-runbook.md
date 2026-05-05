# Controller Runbook

## Controller Philosophy

The controller is not a coder.

The controller is a roadmap-preserving orchestration layer.

Its most valuable resource is clean context.

It must not pollute its context with full diffs or large source files unless necessary.

It should reason from:

- roadmap;
- state file;
- worker reports;
- lightweight git metadata;
- test outputs;
- verifier reports when needed;
- incident reports;
- notification intents;
- Resend email artifacts;
- Telegram message artifacts;
- remote decisions.

## Default Turn Procedure

1. Read or create state.
2. Read roadmap.
3. Identify current milestone.
4. Create one bounded task.
5. Write worker prompt to disk.
6. Send prompt to MCP worker.
7. Read worker response.
8. Read worker report.
9. Run lightweight diff triage.
10. Compare evidence against acceptance checks.
11. Write controller decision note.
12. Update state.
13. Continue, correct, complete, escalate, or notify.

## What Counts As A Bounded Task

Good examples:

- Implement GPU-side contact pair filtering for one contact path.
- Add tests proving no CPU roundtrip in contact filtering.
- Add benchmark harness for kernel batching.
- Replace one solver component behind an existing interface.
- Add a single adapter layer.
- Audit current code paths for GPU-host synchronization points.

Bad examples:

- Implement the whole roadmap.
- Fully parallelize the entire solver.
- Refactor the architecture.
- Make the code production-ready.
- Fix all performance issues.
- Implement GNN surrogate and solver integration together.

## Controller Must Avoid

- reading full `git diff`;
- reviewing every changed line;
- letting worker redefine roadmap;
- continuing after SEV0-SEV2 without user decision;
- spawning multiple implementation workers;
- trusting worker summary without reports;
- losing worker thread ID;
- relying only on conversation context;
- letting reports scatter across docs;
- letting worker edit orchestrator state;
- letting email replies execute approval by default;
- relying on Telegram inline keyboard by default;
- continuing from stale Telegram replies;
- accepting replies from non-allowlisted users;
- using generic Signal MCP servers by default;
- using Resend contact/broadcast/domain/API-key/webhook tools by default.

## Lightweight Diff Commands

Use:

```bash
git status --short
git diff --name-status
git diff --stat
git diff --check
