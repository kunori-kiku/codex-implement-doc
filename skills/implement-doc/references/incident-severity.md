# Incident Severity Reference

## SEV0 — Destructive / Unsafe

Definition:

The worker has done or proposed something that may be destructive, unsafe, security-sensitive, data-risky, or hard to reverse.

Examples:

- deletes large parts of the repo;
- touches secrets or credentials;
- changes auth/security logic;
- introduces production deployment side effects;
- performs irreversible migration;
- uses dangerous shell commands;
- modifies orchestrator files improperly;
- attempts recursive agent spawning.

Controller action:

- stop immediately;
- write incident report;
- write notification intent;
- notify through Resend email if configured;
- notify through Telegram if configured;
- send incident report through Resend email;
- wait for Telegram remote decision, using a direct Codex-session decision only as fallback when no remote path is available;
- do not continue worker.

## SEV1 — Roadmap Contradiction

Definition:

Implementation contradicts the roadmap's core direction.

Examples:

- roadmap says add GPU path, worker replaces solver architecture;
- roadmap says preserve API, worker changes API;
- roadmap says bounded implementation, worker performs rewrite;
- worker implements a different feature.

Controller action:

- stop;
- write incident report;
- write notification intent;
- notify through Resend email if configured;
- notify through Telegram if configured;
- send incident report through Resend email;
- wait for Telegram remote decision, using a direct Codex-session decision only as fallback when no remote path is available.

## SEV2 — Major Ambiguity / Missing Dependency

Definition:

Implementation cannot proceed safely because a major decision is missing.

Examples:

- two possible architectures and roadmap does not choose;
- required dependency unavailable;
- critical environment setup is missing;
- MCP tool or server unavailable;
- package, compiler, runtime, Docker, GPU driver, database, or service dependency must be installed or repaired;
- missing credential, account authorization, quota, network access, permission, or sandbox capability blocks progress;
- benchmark target undefined;
- acceptance check impossible;
- user must decide tradeoff.

Controller action:

- write incident;
- write notification intent;
- notify through Resend email if configured;
- notify through Telegram if configured;
- send incident report through Resend email;
- wait for Telegram remote decision, using a direct Codex-session decision only as fallback when no remote path is available.

## Catch-All Operational Blocker

Definition:

The run cannot keep making progress for an operational reason outside normal implementation quality.

Examples:

- worker cannot start, resume, or produce a report;
- required MCP server is missing, hung, or misconfigured;
- package manager, compiler, test runner, interpreter, Docker, GPU driver, database, or service dependency is unavailable;
- critical environment setup requires installation effort;
- credentials, account authorization, quota, network access, permissions, or sandbox capability are missing;
- notification delivery fails in a way that prevents remote decisions;
- repeated command timeouts or orchestration errors prevent bounded progress.

Default severity:

- SEV2 when the user can choose a non-destructive remediation route;
- SEV0 when remediation may require `sudo`, unapproved `danger-full-access`, production access, secrets, destructive commands, migrations, service restarts, or filesystem ownership changes;
- SEV3 only when one non-privileged correction task can likely fix the blocker without user input.

Controller action:

- write incident report with `incident_category: operational_blocker`;
- write notification intent;
- notify remotely through Resend and Telegram when available;
- include concise remediation options in the notification;
- include detailed remediation plan, risks, and rollback notes in the report;
- recommend `G` for non-privileged MCP-agent remediation;
- recommend `H` for privileged or dangerous remediation;
- use direct Codex-session prompt only if no remote notification path can be created.

Privileged remediation rule:

- before any newly privileged action, create an operator plan and a separate read-only safety verifier review;
- do not require that two-agent safety gate, incident update, or repeated approval merely because the worker uses `danger-full-access` if the user already explicitly approved that sandbox mode for this run after seeing the risk explanation;
- after approval is recorded, treat `danger-full-access` as the efficient normal worker sandbox for that run and rely on the Codex toolchain authorization boundary instead of rechecking it in every incident;
- the verifier must scrutinize safety, scope, reversibility, least privilege, and whether sudo or dangerous access is actually needed;
- proceed only if the user approval covers the action class and the safety verifier accepts the plan;
- otherwise update the incident and request another remote decision.

## SEV3 — Local Deviation

Definition:

A small or medium deviation that can probably be corrected without user input.

Examples:

- nearby file changed unexpectedly;
- test incomplete;
- local API mismatch;
- worker skipped one check;
- small scope creep.

Controller action:

- write note or incident;
- send one correction task;
- ask user only if correction fails.

## SEV4 — Informational

Definition:

A risk or issue worth recording but not blocking.

Examples:

- performance benchmark not conclusive;
- minor technical debt;
- optional cleanup left;
- test runtime too long;
- future work noted.

Controller action:

- record;
- continue.
