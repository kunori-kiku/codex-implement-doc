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
