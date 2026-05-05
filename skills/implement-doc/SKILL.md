---
name: implement-doc
description: Use this skill when the user asks Codex to implement a roadmap, implementation document, design document, SPEC.md, ROADMAP.md, TODO plan, research engineering plan, or any document-driven implementation task. This skill orchestrates exactly one persistent Codex MCP worker session, stores the worker thread id, assigns bounded implementation tasks, requires detailed implementation reports, performs lightweight verification without loading full diffs into the controller context, escalates roadmap deviations through incident reports, sends notification emails through Resend, and accepts executable remote decisions through Telegram plain-text replies.
---

# Implement Doc Skill

## 0. Purpose

This skill turns a document into an auditable implementation pipeline.

The controller session must not behave like a normal coding session.

The controller session is the roadmap-level orchestrator.

The persistent MCP worker session is the implementation agent.

Optional verifier subagents are read-only auditors used only when lightweight evidence indicates risk.

The controller must protect its context window.

The controller should not load full source files or full diffs unless absolutely necessary.

Heavy code inspection should be delegated to a read-only verifier subagent or verifier worker.

For remote notifications, Resend email and Telegram may both be used.

Resend email is the primary notification and long-report delivery channel.

Telegram is the executable reply channel by default.

Telegram replies must be plain text, not inline keyboard callbacks.

Incident reports must be sent to the user by Resend email when SEV0-SEV2 user decisions are required.

Incident reports should also be sent to Telegram when available.

Signal is disabled by default.

Do not connect generic Signal MCP servers that expose arbitrary send or receive tools.

A future Signal integration may only be notify-only, fixed-recipient, no receive_message, no arbitrary recipient argument, no SSE public listener, and no logging of message bodies or phone numbers.

## 1. Role Split

### 1.1 Controller Session

The current Codex session is the controller.

The controller is responsible for:

- reading the roadmap / implementation document;
- converting it into milestones and acceptance checks;
- creating or resuming a persistent worker session through Codex MCP;
- storing the worker `threadId` in a state file;
- assigning exactly one bounded task at a time;
- reading worker reports;
- performing lightweight diff triage;
- running or requesting relevant tests/checks;
- comparing results against the roadmap;
- deciding whether to continue, correct, complete, or escalate;
- writing incident reports when implementation diverges from the roadmap;
- writing notification intents for SEV0-SEV2 incidents;
- sending notification emails through Resend when available;
- attaching or embedding incident reports in Resend email when available;
- attaching or embedding worker reports in Resend email when useful;
- sending Telegram notification summaries when available;
- sending incident reports to Telegram when available;
- accepting executable user decisions through allowlisted Telegram plain-text replies;
- writing accepted remote decisions under `remote-decisions/`;
- asking the user for a multiple-choice or custom decision only when needed.

The controller must not directly edit implementation code unless:

1. the worker fails twice on the same bounded task;
2. a small controller-side edit is clearly safer than another worker turn;
3. the user explicitly asks the controller to take over.

The controller must not read the full `git diff` by default.

The controller must not use email replies as executable approval by default.

The controller must not use Signal replies as executable approval.

The controller must accept executable remote decisions through Telegram plain-text replies by default.

### 1.2 Persistent MCP Worker Session

The worker is a single persistent Codex MCP session.

The worker is responsible for:

- reading only the relevant implementation context;
- writing code;
- running local checks;
- fixing errors within the assigned bounded task;
- writing a detailed worker report to disk;
- returning only a short summary, status, report path, and suggested next task.

The worker must not:

- spawn another Codex session;
- call `codex`, `codex-reply`, `codex mcp-server`, or any recursive agent/tool that starts another coding agent;
- modify orchestrator state files unless explicitly instructed;
- modify incident reports;
- modify remote decision files;
- modify notification intent files;
- perform broad unrelated refactors;
- reinterpret the roadmap beyond the assigned bounded task;
- delete tests unless explicitly required and justified;
- touch unrelated files without reporting them.

### 1.3 Optional Verifier Subagent

The verifier is read-only.

Use a verifier only when lightweight triage indicates risk.

The verifier may inspect full diffs or larger source regions because its context can be discarded afterwards.

The verifier must not edit files.

The verifier must return:

1. whether the worker report matches actual changes;
2. whether implementation satisfies the assigned acceptance checks;
3. suspicious unrelated edits;
4. missing tests;
5. severity classification if divergence exists.

### 1.4 Notification Layer

The notification layer is optional but supported.

The controller may use configured MCP tools to notify the user.

Default policy:

- Resend email sends formal notification and detailed reports.
- Telegram sends short notification and accepts executable plain-text replies.
- Telegram inline buttons should not be used by default.
- Telegram replies must include a nonce.
- Only allowlisted Telegram users may approve, reject, redirect, or issue custom instructions.
- Remote decisions must be written to disk before the controller continues implementation.
- Email is notification-only by default.
- Signal is disabled by default.

The notification layer must not silently execute unauthenticated or stale replies.

## 2. Required User Inputs

The user should provide, explicitly or implicitly:

- roadmap document path;
- implementation document path;
- title or task label;
- repository root if not obvious;
- branch if relevant.

If the user says something like:

> Implement as per the doc under docs/roadmap.md says

then infer:

- `roadmap_doc = docs/roadmap.md`
- `title = basename or nearby semantic title`
- `repo_root = current working directory`
- `branch = current git branch`

Do not ask clarification if these can be inferred safely.

Ask clarification only when:

- the document path is not identifiable;
- multiple plausible roadmap documents exist;
- the task could damage data or production systems;
- implementation would require credentials or external side effects;
- notification channels are requested but no configured MCP tool or fallback intent file exists.

If notification tools are unavailable, still write notification intent files and incident reports.

## 3. Required MCP Setup

Use a configured MCP server that exposes Codex as a worker.

Expected server name:

```text
codex_worker
```

Expected tools:

```text
codex
codex-reply
```

When starting a worker session, use the MCP `codex` tool.

When continuing a worker session, use the MCP `codex-reply` tool with the stored `threadId`.

Worker sessions should use:

```json
{
  "approval-policy": "never",
  "sandbox": "workspace-write",
  "include-plan-tool": true
}
```

If a separate worker profile exists, use it.

The worker profile should not expose the same `codex_worker` MCP server to avoid recursive Codex calls.

Recommended worker configuration:

```json
{
  "profile": "worker",
  "approval-policy": "never",
  "sandbox": "workspace-write",
  "include-plan-tool": true,
  "cwd": "<repo-root>"
}
```

Never use `danger-full-access` unless the repository is inside a disposable container or sandbox and the user explicitly requested it.

## 4. Optional Notification MCP Setup

The skill supports notification MCP servers, but should use a strict channel split.

Recommended conceptual MCP servers:

```text
resend
telegram_notifier
```

Recommended Resend behavior:

* send formal incident email;
* include severity, run ID, task ID, incident ID, summary, recommended decision, nonce, and Telegram reply instructions;
* attach or embed full incident report;
* attach or embed worker report if useful;
* remain notification-only;
* do not use inbound email as executable approval by default;
* do not manage contacts, broadcasts, domains, API keys, or webhooks by default.

Recommended Telegram behavior:

* send short notification;
* send incident report if useful;
* ask the user to reply with plain text;
* receive user reply through polling, webhook bridge, MCP receive tool, or external watcher;
* accept only allowlisted Telegram user IDs;
* validate nonce;
* write remote decision file.

Telegram executable replies should use this format:

```text
A <nonce>
B <nonce>
C <nonce>
D <nonce>
E <nonce>
F <nonce>
CUSTOM <nonce> <freeform instruction>
```

Do not rely on inline keyboards.

Do not rely on Resend email replies as the executable approval channel by default.

Do not rely on Signal as the executable approval channel.

## 5. Concrete Notification MCP Tool Map

Preferred Resend MCP server name:

```text
resend
```

Preferred Resend role:

```text
notify_only_email_sender
```

Preferred Resend tool usage:

```text
send email only
```

Do not use these Resend capabilities by default:

```text
received emails
contacts
broadcasts
domains
segments
topics
contact properties
API keys
webhooks
```

If the Resend MCP server exposes exact tool names and Codex supports `enabled_tools`, restrict enabled tools to the email sending tool only.

If the exact email-send tool name is unknown, leave tool filtering unset, but the controller must only use Resend for outbound notification email.

Preferred Telegram MCP server name:

```text
telegram_notifier
```

Preferred Telegram tools:

```text
telegram_notifier.send_message
telegram_notifier.send_document
telegram_notifier.get_updates
```

For SEV0-SEV2 incidents, the controller should attempt notification in this order:

1. Use `resend` to send formal email with short summary, recommended choice, Telegram reply instructions, and incident/worker report content or attachments.
2. Use `telegram_notifier.send_message` with short incident summary and reply instructions.
3. Use `telegram_notifier.send_document` with the full incident report Markdown file if useful.
4. Use `telegram_notifier.send_document` with the worker report Markdown file if useful.
5. Use `telegram_notifier.get_updates` in long-polling mode while waiting for user reply.

Resend email is the primary notification channel.

Telegram is the executable reply channel.

Signal is disabled by default.

If Resend is unavailable but Telegram is available, continue with Telegram notification and Telegram reply.

If Telegram is unavailable but Resend is available, send Resend email and stop with `needs-user-decision`.

If both Resend and Telegram are unavailable, write notification intent and stop with `needs-user-decision`.

The controller must not continue a SEV0-SEV2 run without either:

* accepted Telegram remote decision;
* direct user instruction in the Codex session;
* explicit roadmap update resolving the incident.

## 6. Required Orchestrator Directories

Create these directories inside the repository if missing:

```text
.codex-orchestrator/implement-doc/state/
.codex-orchestrator/implement-doc/reports/
.codex-orchestrator/implement-doc/incidents/
.codex-orchestrator/implement-doc/prompts/
.codex-orchestrator/implement-doc/decisions/
.codex-orchestrator/implement-doc/remote-decisions/
.codex-orchestrator/implement-doc/notifications/
```

The controller may create these files.

The worker may write reports only under:

```text
.codex-orchestrator/implement-doc/reports/
```

The worker must not directly edit state, incident, decision, remote-decision, or notification files unless explicitly instructed.

## 7. State File

The controller must persist run state.

State files live under:

```text
.codex-orchestrator/implement-doc/state/
```

State filename format:

```text
<run-id>.json
```

Run ID format:

```text
YYYYMMDD-HHMMSS-<slug>
```

Before starting a new worker, search for a matching active state file.

A matching active state file means:

* same repository root;
* same roadmap document;
* same branch if branch exists;
* status is `active`, `paused`, `needs-user-decision`, or `waiting-remote-decision`.

If a matching active state exists, reuse its `worker_thread_id`.

If no matching active state exists, call `codex` to create a new worker session and store the returned `structuredContent.threadId`.

The state file is the source of truth for:

* `run_id`;
* `roadmap_doc`;
* `worker_thread_id`;
* current milestone;
* current task;
* completed tasks;
* reports;
* incidents;
* notifications;
* remote decisions;
* current status.

The controller must not rely only on conversation memory to remember the worker session.

## 8. Main Loop

The controller must follow this loop.

### Step 1 — Load Roadmap

Read the roadmap document.

Extract:

* goals;
* non-goals;
* constraints;
* implementation milestones;
* acceptance checks;
* required tests;
* risky areas;
* dependencies;
* order constraints.

If the document is long, summarize it into a structured checklist and store that checklist in the state file or a decision file.

Do not ask the worker to implement the entire roadmap in one turn.

### Step 2 — Choose One Bounded Task

Pick exactly one bounded task.

A bounded task should usually be one of:

* one module;
* one kernel;
* one API;
* one test layer;
* one benchmark;
* one refactor point;
* one verification step.

Avoid assigning:

* the whole roadmap;
* multiple unrelated modules;
* broad architecture rewrites;
* ambiguous “make it better” tasks.

Each task must include:

* task ID;
* milestone ID;
* exact objective;
* files/directories likely involved;
* acceptance checks;
* tests/commands to run if known;
* forbidden changes;
* report path.

### Step 3 — Write Worker Prompt File

Before sending a worker task, write the exact prompt to:

```text
.codex-orchestrator/implement-doc/prompts/<timestamp>-<task-id>-worker-prompt.md
```

This creates an audit trail.

### Step 4 — Start or Continue Worker

If no `worker_thread_id` exists:

* call MCP tool `codex`;
* pass worker base instructions;
* pass the first task prompt;
* store returned `structuredContent.threadId`.

If `worker_thread_id` exists:

* call MCP tool `codex-reply`;
* pass the stored `threadId`;
* pass the next bounded task prompt.

### Step 5 — Require Worker Report

The worker must write a detailed report to:

```text
.codex-orchestrator/implement-doc/reports/<timestamp>-<task-id>-<slug>.md
```

The worker’s final response to the controller must contain only:

1. one-paragraph summary;
2. status: `complete`, `partial`, `blocked`, or `failed`;
3. report path;
4. commands run;
5. suggested next bounded task.

The worker must not dump long implementation details into the MCP response.

Details belong in the report file.

### Step 6 — Lightweight Verification

After the worker returns, the controller must read:

* worker summary;
* worker report file;
* state file;
* roadmap document;
* lightweight git metadata.

The controller should run:

```bash
git status --short
git diff --name-status
git diff --stat
git diff --check
```

The controller must not run plain:

```bash
git diff
```

by default.

The controller must not load full diffs unless a risk trigger is present.

### Step 7 — Compare Against Roadmap

The controller must compare:

* worker report;
* changed file manifest;
* test results;
* lightweight git metadata;
* roadmap acceptance checks.

The controller must decide one of:

```text
continue
correction-needed
done
incident
needs-user-decision
waiting-remote-decision
```

### Step 8 — Continue, Escalate, or Notify

If `continue`:

* update state;
* assign the next bounded task to the same worker thread.

If `correction-needed`:

* assign a precise correction task to the same worker thread;
* do not start a new worker;
* record the correction in state.

If `done`:

* update state status to `completed`;
* write final decision summary.

If `incident`:

* write an incident report;
* classify severity;
* for SEV0-SEV2, write notification intent and notify user through configured channels;
* for SEV0-SEV2, send Resend email if configured;
* for SEV0-SEV2, send Telegram notification if configured;
* for SEV0-SEV2, set state status to `waiting-remote-decision` or `needs-user-decision`;
* for SEV3, attempt one correction task before asking the user;
* for SEV4, record and continue.

If `needs-user-decision`:

* write a user choice prompt;
* notify through Resend and Telegram if configured;
* send incident report through Resend email if available;
* send incident report to Telegram if available;
* stop the loop until user decision is available.

If `waiting-remote-decision`:

* poll or read Telegram replies if a Telegram MCP receive mechanism exists;
* otherwise leave state and notification intent files for an external watcher;
* validate any reply before continuing.

## 9. Lightweight Diff Triage Policy

The controller must protect its context window.

Default verification uses:

1. worker report;
2. touched file manifest;
3. `git status --short`;
4. `git diff --name-status`;
5. `git diff --stat`;
6. `git diff --check`;
7. relevant test outputs;
8. roadmap acceptance checklist.

The controller must not read full git diff by default.

Full diff inspection is allowed only when:

* the worker report is inconsistent with `git diff --name-status`;
* tests fail unexpectedly;
* modified files are surprising;
* a critical file is touched;
* the task is security-sensitive;
* the task is destructive;
* the task changes data migration logic;
* the task changes public APIs;
* the task changes build system configuration;
* roadmap alignment is unclear;
* the user explicitly asks for audit.

If full inspection is needed, prefer spawning a read-only verifier subagent with a narrow scope.

If the controller must inspect diff directly, inspect only specific files:

```bash
git diff -- <path>
git diff -U3 -- <path>
```

Never load full repo diff into controller context unless the diff is small.

## 10. Risk Classification

Classify each worker turn as LOW, MEDIUM, HIGH, or CRITICAL.

### LOW

Use LOW when:

* only expected files changed;
* tests were added or updated;
* diff stat is small or moderate;
* relevant checks passed;
* worker report matches lightweight git metadata.

Action:

```text
continue
```

### MEDIUM

Use MEDIUM when:

* expected files plus nearby dependencies changed;
* tests are partial;
* benchmark is missing but not required for current checkpoint;
* some acceptance checks are unclear;
* worker reports known gaps that do not contradict roadmap.

Action:

```text
correction-needed or continue with caution
```

### HIGH

Use HIGH when:

* unrelated files changed;
* public API changed unexpectedly;
* build/config files changed unexpectedly;
* tests were deleted or weakened;
* diff stat suggests broad refactor;
* worker report does not match changed files;
* implementation direction may deviate from roadmap.

Action:

```text
spawn read-only verifier or write SEV2/SEV3 incident
```

### CRITICAL

Use CRITICAL when:

* destructive deletion occurred;
* secrets, credentials, auth, production deployment, or security-sensitive files changed;
* data migration or irreversible operation was introduced;
* roadmap was contradicted;
* worker modified orchestrator state/incident files improperly;
* worker attempted recursive Codex calls;
* worker ignored explicit forbidden changes.

Action:

```text
write SEV0 or SEV1 incident and ask user through Resend notification + Telegram remote decision flow
```

## 11. Incident Severity

Use these severities.

### SEV0 — Destructive / Unsafe

Examples:

* destructive deletion;
* production or credential risk;
* unsafe shell command;
* irreversible data operation;
* security-sensitive changes without explicit permission.

Action:

* stop immediately;
* write incident report;
* write notification intent;
* send Resend email if configured;
* send Telegram notification if configured;
* send incident report through Resend email;
* send incident report to Telegram if useful;
* wait for Telegram remote decision or direct user decision.

### SEV1 — Roadmap Contradiction

Examples:

* implementation direction contradicts core roadmap;
* worker implements a different architecture;
* worker ignores explicit constraints;
* worker replaces rather than extends required design.

Action:

* stop;
* write incident report;
* write notification intent;
* send Resend email if configured;
* send Telegram notification if configured;
* send incident report through Resend email;
* send incident report to Telegram if useful;
* wait for Telegram remote decision or direct user decision.

### SEV2 — Major Ambiguity / Missing Dependency

Examples:

* roadmap lacks enough detail to choose between major technical routes;
* dependency missing;
* implementation requires user decision;
* worker exposes a major feasibility blocker.

Action:

* write incident;
* write notification intent;
* send Resend email if configured;
* send Telegram notification if configured;
* send incident report through Resend email;
* send incident report to Telegram if useful;
* wait for Telegram remote decision or direct user decision.

### SEV3 — Local Deviation

Examples:

* small unexpected edit;
* local design mismatch;
* test gap;
* minor implementation issue;
* manageable correction needed.

Action:

* write incident report or decision note;
* attempt one correction task;
* ask user only if correction fails.

### SEV4 — Informational

Examples:

* technical debt;
* performance uncertainty;
* benchmark not yet run;
* minor risk to revisit later.

Action:

* record;
* continue.

## 12. Incident Report Rules

Incident reports live under:

```text
.codex-orchestrator/implement-doc/incidents/
```

Filename format:

```text
<timestamp>-<severity>-<slug>.md
```

Every incident report must include:

* incident ID;
* severity;
* timestamp;
* run ID;
* task ID;
* worker thread ID;
* roadmap document;
* worker report path;
* summary;
* expected behavior according to roadmap;
* actual implementation behavior;
* evidence;
* impact;
* recommended user decision;
* notification intent;
* remote reply rules.

For SEV0-SEV2, the incident report must be sent to the user through Resend email if Resend MCP is available.

If Resend supports local file attachments, attach the incident report as a Markdown file.

If Resend attachment sending is unavailable, embed the incident report in the email body.

If Telegram supports file sending, also send the incident report as a Markdown file.

If Telegram does not support file sending but supports long messages, send the incident report content split into safe chunks.

If Resend or Telegram report sending fails, record the failure in the notification intent and state file.

The skill must not pretend the user has seen the incident report unless the send operation succeeds or a notification artifact has been created for an external watcher.

## 13. Notification Rules

Notification files live under:

```text
.codex-orchestrator/implement-doc/notifications/
```

For SEV0-SEV2 incidents:

1. Write a notification intent JSON file.
2. Write a Resend email Markdown file.
3. Write a Resend email plaintext file.
4. Write a Telegram message file.
5. Send Resend email if `resend` MCP is configured.
6. Send Telegram notification if `telegram_notifier` MCP is configured.
7. Send incident report through Resend email if possible.
8. Send worker report through Resend email if useful and not too noisy.
9. Send incident report to Telegram if useful.
10. Send worker report to Telegram if useful.
11. Ask user to reply in Telegram with plain text.
12. Do not use inline keyboards by default.
13. Do not treat Resend email reply as executable approval by default.
14. Do not use Signal by default.
15. Set state status to `waiting-remote-decision`.

Resend email should be detailed.

Telegram message should be short.

Incident report must be sent as an email attachment or embedded email content.

The Telegram reply prompt must include:

* incident ID;
* nonce;
* valid options;
* `CUSTOM` option;
* examples.

Default options:

```text
A <nonce> — Continue with the current implementation and update roadmap later.
B <nonce> — Revert the worker's changes for this task.
C <nonce> — Keep partial changes but redirect implementation.
D <nonce> — I will provide a new roadmap section.
E <nonce> — Stop this implementation run.
F <nonce> — Run a read-only verifier audit first.
CUSTOM <nonce> <instruction> — Give a custom instruction to the controller.
```

## 14. Remote Decision Rules

Remote decision files live under:

```text
.codex-orchestrator/implement-doc/remote-decisions/
```

Filename format:

```text
<timestamp>-<incident-id>-telegram-decision.json
```

The controller may continue only after a remote decision is:

* from an allowlisted Telegram user ID;
* associated with the correct run ID or incident ID;
* validated against the current active nonce;
* not expired if expiry is configured;
* parsed into a supported action;
* written to disk;
* recorded in the state file.

Supported replies:

```text
A <nonce>
B <nonce>
C <nonce>
D <nonce>
E <nonce>
F <nonce>
CUSTOM <nonce> <freeform instruction>
```

Meaning:

```text
A — Continue with current implementation and update roadmap later.
B — Revert worker changes for this task.
C — Keep partial changes but redirect implementation.
D — Wait for user to provide a new roadmap section.
E — Stop run.
F — Run read-only verifier first.
CUSTOM — Continue according to user's freeform instruction.
```

Invalid replies should trigger a Telegram help message.

Old replies with stale nonce must be rejected.

Replies from non-allowlisted users must be rejected and logged.

Replies from Resend email must be ignored for execution unless email executable mode is explicitly enabled in state.

Replies from Signal must be ignored for execution.

## 15. User Decision Prompt

For SEV0-SEV2, ask the user with choices.

Do not ask vague open-ended questions if a multiple-choice prompt is possible.

However, always include a `CUSTOM` option for freeform instructions.

Example:

```text
I found a SEV2 roadmap ambiguity.

I sent the full incident report to your email through Resend.

Choose one by replying in Telegram:

A 8KQ2 — Continue with the worker's current implementation route and update the roadmap later.
B 8KQ2 — Revert the worker's current changes for this task.
C 8KQ2 — Keep partial changes but redirect the worker.
D 8KQ2 — I will provide a new roadmap section for this component.
E 8KQ2 — Stop this implementation run.
F 8KQ2 — Run a read-only verifier audit first.
CUSTOM 8KQ2 <your instruction> — Give a custom controller instruction.
```

The controller should also provide:

* incident report path;
* worker report path;
* notification email subject;
* one-paragraph summary;
* recommended choice;
* why the recommendation is best.

## 16. Completion Criteria

The run can be marked `completed` only when:

* all roadmap milestones are either implemented or explicitly marked out-of-scope;
* acceptance checks pass or are explicitly waived by the user;
* no SEV0-SEV2 incident remains unresolved;
* no remote decision is pending;
* state file is updated;
* final report or decision note is written.

## 17. Final User Response

Do not dump long reports into chat.

Final response should contain:

* run status;
* roadmap document;
* worker thread ID;
* latest worker report path;
* latest incident path if any;
* latest notification intent path if any;
* latest Resend email artifact path if any;
* latest Telegram message path if any;
* latest remote decision path if any;
* what was completed;
* what remains;
* whether user decision is required.

Example:

```text
Status: waiting remote decision

Roadmap: docs/roadmap.md
Worker thread: <thread-id>
Latest report: .codex-orchestrator/implement-doc/reports/...
Incident: .codex-orchestrator/implement-doc/incidents/...
Notification intent: .codex-orchestrator/implement-doc/notifications/...
Resend email: .codex-orchestrator/implement-doc/notifications/...
Remote decision: pending

The worker completed M1 but diverged on M2 by changing the solver API rather than adding the GPU filtering layer described in the roadmap.

I sent the full incident report by Resend email.

Recommended choice: C — keep partial changes but redirect the worker.
Reply in Telegram with: C 8KQ2
```

## 18. Hard Rules

* Use exactly one persistent MCP worker session per run.
* Store `threadId` in the state file.
* Reuse the same worker thread for follow-up tasks.
* Do not spawn multiple implementation workers.
* Do not let the worker recursively call Codex.
* Do not read full `git diff` by default.
* Use optional read-only verifier for heavy diff inspection.
* Keep worker tasks bounded.
* Keep controller context clean.
* Treat files and reports as the source of truth, not natural-language claims.
* Stop for SEV0-SEV2.
* For SEV0-SEV2, write incident report.
* For SEV0-SEV2, write notification intent.
* For SEV0-SEV2, send Resend email if configured.
* For SEV0-SEV2, send Telegram notification if configured.
* For SEV0-SEV2, send incident report through Resend email if configured.
* For SEV0-SEV2, accept executable reply through allowlisted Telegram plain-text reply.
* Do not use Telegram inline keyboard by default.
* Do not use Resend email as executable approval by default.
* Do not use Signal by default.
* For SEV3, attempt one correction task.
* For SEV4, record and continue.

