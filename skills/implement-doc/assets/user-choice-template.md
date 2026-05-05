# User Decision Required

- Run ID:
- Task ID:
- Incident:
- Severity:
- Timestamp:
- Roadmap Doc:
- Worker Report:
- Notification Intent:
- Resend Email:
- Nonce:

## Summary

One paragraph.

## Why User Input Is Needed

Explain the blocker or divergence.

## Recommended Choice

Recommended option:

Reason:

## Choices

A. Continue with the current implementation and update the roadmap later.

B. Revert the worker's changes for this task.

C. Keep partial changes but redirect implementation.

D. I will provide a new roadmap section for this component.

E. Stop this implementation run.

F. Run a read-only verifier audit first.

G. Approve non-privileged MCP-agent remediation of the blocker.

H. Approve privileged or dangerous remediation only after independent safety review.

CUSTOM. Provide a freeform instruction.

Use remote decision first. Ask in the direct Codex session only if no remote notification path is available.

## Notification Sent

The full incident report should be sent to the user by Resend email.

Telegram should contain a short notification and plain-text reply instructions.

## Telegram Reply Format

Reply in Telegram with one of:

```text
A <nonce>
B <nonce>
C <nonce>
D <nonce>
E <nonce>
F <nonce>
G <nonce>
H <nonce>
CUSTOM <nonce> <your instruction>
