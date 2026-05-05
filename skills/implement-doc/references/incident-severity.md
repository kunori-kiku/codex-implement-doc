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
- wait for Telegram remote decision or direct user decision;
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
- wait for Telegram remote decision or direct user decision.

## SEV2 — Major Ambiguity / Missing Dependency

Definition:

Implementation cannot proceed safely because a major decision is missing.

Examples:

- two possible architectures and roadmap does not choose;
- required dependency unavailable;
- benchmark target undefined;
- acceptance check impossible;
- user must decide tradeoff.

Controller action:

- write incident;
- write notification intent;
- notify through Resend email if configured;
- notify through Telegram if configured;
- send incident report through Resend email;
- wait for Telegram remote decision or direct user decision.

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
