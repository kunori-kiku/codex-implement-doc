---
description: Implement a roadmap/document using the implement-doc skill and one persistent Codex MCP worker.
argument-hint: DOC=<path> TITLE=<short-title>
---

$implement-doc

Implement according to the document specified below.

Arguments:

$ARGUMENTS

Required behavior:

- Use the implement-doc skill.
- Use exactly one persistent Codex MCP worker session.
- Persist worker threadId in `.codex-orchestrator/implement-doc/state/`.
- Worker must write detailed implementation reports.
- Main controller must verify report + lightweight git metadata + tests against the roadmap.
- Main controller must not read full `git diff` by default.
- Use read-only verifier subagent for heavy diff review when needed.
- Stop and create an incident report if implementation diverges from the roadmap.
- For SEV0-SEV2, send Resend email if configured.
- For SEV0-SEV2, send Telegram notification if configured.
- Resend email is the primary notification and long-report delivery channel.
- Resend email is notification-only by default.
- Telegram is the executable plain-text reply channel.
- Do not use inline keyboard by default.
- Send incident report through Resend email.
- Send worker report through Resend email when useful.
- Accept Telegram replies only from allowlisted users and only with valid nonce.
- Store accepted replies under `.codex-orchestrator/implement-doc/remote-decisions/`.
- Do not use Signal by default.
