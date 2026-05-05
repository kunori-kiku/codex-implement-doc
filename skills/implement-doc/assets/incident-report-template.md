# Implementation Incident Report

- Incident ID:
- Severity: SEV0 | SEV1 | SEV2 | SEV3 | SEV4
- Timestamp:
- Run ID:
- Task ID:
- Milestone ID:
- Worker Thread ID:
- Roadmap Doc:
- Worker Report Path:
- Repo Root:
- Branch:
- Incident Category: roadmap_divergence | implementation_blocker | operational_blocker | notification_failure | unsafe_remediation
- Status: open | resolved | superseded

## 1. Summary

One paragraph.

## 2. What Diverged

### Expected According To Roadmap

Describe what the roadmap required.

### Actual Implementation / Worker Behavior

Describe what happened instead.

## 3. Evidence

Include lightweight evidence first.

```bash
git status --short
git diff --name-status
git diff --stat
git diff --check
```

Summarize outputs.

Reference files, reports, tests, or commands.

Do not paste huge full diffs.

## 4. Impact

Explain what breaks or becomes risky if the controller continues.

Possible categories:

- roadmap alignment;
- architecture;
- correctness;
- tests;
- performance;
- security;
- data safety;
- maintainability;
- context pollution;
- user decision required.
- operational blocker;
- environment setup;
- dependency installation;
- permission / authorization;
- notification delivery;
- privileged remediation.

## 5. Severity Rationale

Why this is SEV0 / SEV1 / SEV2 / SEV3 / SEV4.

## 6. Recommended User Decision

Choose one recommendation.

A. Continue with the current implementation and update the roadmap later.
B. Revert the worker's changes for this task.
C. Keep partial changes but redirect implementation.
D. I will provide a new roadmap section for this component.
E. Stop this implementation run.
F. Run a read-only verifier audit first.
G. Approve non-privileged MCP-agent remediation of the blocker.
H. Approve privileged or dangerous remediation only after independent safety review.
CUSTOM. Follow a custom user instruction.

Recommended choice:

Reason:

## 7. Remediation Proposal

Fill this section for operational blockers, environment issues, dependency installs, permission problems, broken MCP tools, notification failures, repeated timeouts, or any issue that prevents the run from continuing.

### Brief Options For Notification

- Option:
- When to choose:
- Risk:

### Detailed Recommended Plan

- Proposed operator: persistent MCP worker
- Exact bounded task:
- Expected commands:
- Expected files/services affected:
- Verification:
- Rollback:
- Estimated risk:

### Privileged / Dangerous Action Review

- Requires `sudo`, production access, destructive command, migration, credential handling, service restart, ownership change, or similar privileged action: yes | no
- `danger-full-access` already explicitly approved for this run: yes | no
- Independent read-only safety verifier required: yes | no
- Operator plan path:
- Safety verifier report path:
- Safety decision:

## 8. Controller Action Taken

- stopped run;
- sent correction task;
- spawned verifier;
- drafted non-privileged remediation task;
- drafted privileged operator plan on persistent MCP worker;
- spawned independent safety verifier;
- asked user;
- sent Resend email notification;
- sent Telegram notification;
- sent incident report through Resend email;
- sent incident report to Telegram;
- waiting for Telegram remote decision;
- continued with warning;
- other:

## 9. Notification Intent

```json
{
  "should_notify_user": true,
  "auto_send_allowed": true,
  "severity": "SEV2",
  "notify_channels": ["resend", "telegram_notifier"],
  "primary_notification_channel": "resend",
  "reply_channel": "telegram_notifier",
  "resend_mode": "notify_only",
  "telegram_mode": "plain_text_reply",
  "send_incident_report": true,
  "send_worker_report": true,
  "title": "",
  "message": "",
  "requires_user_reply": true,
  "report_paths": {
    "worker_report": "",
    "incident_report": ""
  },
  "resend": {
    "from": "Codex Orchestrator <codex-alert@example.com>",
    "to": [],
    "cc": [],
    "bcc": [],
    "reply_to": null,
    "subject": "",
    "send_as_attachment_if_supported": true,
    "embed_report_if_attachment_not_supported": true,
    "allow_inbound_email_decisions": false
  },
  "allowed_responders": {
    "telegram_user_ids": []
  },
  "remote_reply": {
    "enabled": true,
    "incident_id": "",
    "nonce": "",
    "valid_choices": ["A", "B", "C", "D", "E", "F", "G", "H", "CUSTOM"],
    "reply_patterns": [
      "^(A|B|C|D|E|F|G|H)\\s+<nonce>$",
      "^CUSTOM\\s+<nonce>\\s+.+$"
    ],
    "on_valid_reply": "write_remote_decision_and_continue",
    "on_invalid_reply": "send_help_message"
  }
}
```

## 10. Remote Reply Instructions Sent To User

```text
I sent the full incident report to your email through Resend.

Reply in Telegram with one of:

A <nonce> — Continue current route
B <nonce> — Revert worker changes
C <nonce> — Keep partial changes and redirect
D <nonce> — I will provide new roadmap
E <nonce> — Stop run
F <nonce> — Run read-only verifier first
G <nonce> — Approve non-privileged MCP-agent remediation
H <nonce> — Approve privileged remediation after safety review

Or:
CUSTOM <nonce> <your instruction>
```

## 11. Resolution

Fill when resolved.

- Resolution timestamp:
- User choice:
- Remote decision path:
- Follow-up task:
- New roadmap path if any:
- Notes:
