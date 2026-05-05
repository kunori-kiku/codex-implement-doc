# Remote Decision Protocol

## Purpose

Remote decisions allow the user to control an unattended implementation run without SSH.

The controller must treat remote decisions as serious side effects.

A remote decision can cause code changes to continue, revert, stop, or redirect.

Therefore every remote decision must be authenticated, validated, stored, and auditable.

## Accepted Source

Default accepted source:

```text
telegram_notifier
```

Resend email is not an accepted executable source by default.

Signal is not an accepted executable source.

## Allowlist

The controller must accept decisions only from configured Telegram user IDs.

Do not accept decisions from:

* unknown users;
* groups unless explicitly configured;
* forwarded messages;
* stale messages;
* email replies unless explicitly configured;
* Signal.

## Nonce

Each notification must include a nonce.

The nonce should be short enough to type but random enough to prevent accidental approval.

Example:

```text
8KQ2
```

Every executable reply must include the nonce.

## Supported Choices

A:

Continue with the current implementation and update roadmap later.

B:

Revert the worker's changes for this task.

C:

Keep partial changes but redirect implementation.

D:

Pause. The user will provide a new roadmap section.

E:

Stop this implementation run.

F:

Run a read-only verifier audit first.

G:

Approve non-privileged MCP-agent remediation of an operational blocker.

H:

Approve privileged or dangerous remediation only after independent read-only safety review.

CUSTOM:

Use the freeform instruction after the nonce.

## CUSTOM Handling

CUSTOM is necessary because serious engineering incidents often cannot be captured by fixed options.

Example:

```text
CUSTOM 8KQ2 keep the GPU filtering changes, but revert solver API changes and add a no-public-API-change constraint to the roadmap
```

The controller must convert CUSTOM into a bounded controller action.

If CUSTOM is ambiguous or unsafe, the controller must ask for clarification through Telegram, using a direct Codex-session prompt only when no remote path is available.

For all user decisions, prefer Telegram remote decision. Direct Codex-session prompts are fallback only when no configured remote notification or reply path is available.

## Remote Decision File

Every accepted reply must produce a file under:

```text
.codex-orchestrator/implement-doc/remote-decisions/
```

The file must include:

* decision ID;
* timestamp;
* source;
* Telegram user ID;
* Telegram chat ID if available;
* run ID;
* incident ID;
* nonce;
* raw reply;
* parsed choice;
* custom instruction if any;
* accepted true/false;
* rejection reason if any;
* controller action;
* follow-up task if any.

## Invalid Reply Handling

If reply cannot be parsed:

* send Telegram help message;
* do not continue worker.

If nonce is wrong:

* reject;
* send help or stale nonce warning;
* do not continue worker.

If sender is not allowlisted:

* reject;
* log;
* do not continue worker.

If reply is stale:

* reject;
* log;
* do not continue worker.

## State Update

After accepted remote decision:

* append remote decision path to state;
* clear pending remote decision;
* update unresolved user decision;
* update status according to chosen action.

## Controller Actions

A:

* set status active;
* continue current implementation route;
* optionally create roadmap update task.

B:

* set status active;
* assign revert task to worker or perform narrow revert;
* verify revert.

C:

* set status active;
* assign correction/redirection task to worker.

D:

* set status paused;
* wait for user roadmap update.

E:

* set status stopped;
* do not continue worker.

F:

* set status active;
* spawn read-only verifier;
* use verifier result to decide.

G:

* set status active;
* assign one bounded non-privileged remediation task to the persistent MCP worker;
* verify the remediation;
* continue the roadmap loop if the blocker is resolved;
* write a new incident update and request another remote decision if remediation fails.

H:

* keep the run blocked until privileged remediation is planned and reviewed;
* skip the two-agent safety gate, incident update, and repeated approval when the only elevated condition is `danger-full-access` and the user already explicitly approved that sandbox mode for this run;
* after approval is recorded, treat `danger-full-access` as the efficient normal worker sandbox for the run and rely on the Codex toolchain authorization boundary;
* use the persistent MCP worker as the operator task to propose exact commands, affected files/services, expected output, risks, and rollback plan;
* create one independent read-only safety verifier task to scrutinize the operator plan;
* proceed only if the verifier accepts the plan and user approval covers the action class;
* if rejected, materially changed, or still unsafe, write an incident update and request another remote decision.

CUSTOM:

* set status active only if instruction is safe and clear;
* create bounded task from custom instruction;
* otherwise ask follow-up.
