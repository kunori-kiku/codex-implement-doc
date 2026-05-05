# Notification Protocol

## Purpose

The notification protocol lets an unattended cloud VM implementation run alert the user when a serious decision is required.

The user should not need to SSH into the VM just to discover that Codex is blocked.

## Channel Split

Default channel split:

```text
Resend Email = formal notification + long incident report + worker report delivery
Telegram = short alert + executable plain-text reply
Signal = disabled by default
```

Remote decision is the default for all user decisions.

The direct Codex session is a fallback only when no configured remote notification or reply path is available.

For catch-all operational blockers, notifications should include a brief remediation summary and point to the incident report for detailed options.

Use `G` to approve non-privileged MCP-agent remediation.

Use `H` to approve newly privileged or dangerous remediation after independent safety review, except when the only elevated condition is `danger-full-access` and that sandbox mode was already explicitly approved for the run. After that approval is recorded, treat `danger-full-access` as the efficient normal worker sandbox and do not re-notify about it.
