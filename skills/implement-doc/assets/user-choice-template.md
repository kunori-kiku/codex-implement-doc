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

CUSTOM. Provide a freeform instruction.

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
CUSTOM <nonce> <your instruction>
