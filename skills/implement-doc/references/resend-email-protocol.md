# Resend Email Protocol

## Purpose

Resend email is used for formal notification and long-report delivery.

It is not the executable approval channel by default.

The user should be able to read incident details without SSH.

The user should then reply in Telegram with a structured plain-text decision.

## Default Role

Resend is:

```text
notify_only
```

Telegram is:

```text
executable_reply_channel
```

## Email Contents

Every SEV0-SEV2 Resend email should include:

* severity;
* run ID;
* incident ID;
* task ID;
* roadmap path;
* worker report path;
* incident report path;
* one-paragraph summary;
* recommended choice;
* recommendation rationale;
* Telegram reply grammar;
* nonce;
* full incident report;
* worker report if useful.

## Subject Format

Use:

```text
[Codex <severity>] <title> — <run_id>
```

Example:

```text
[Codex SEV2] Roadmap decision required — 20260505-023100-ykx-gpu-parallelization
```

## Attachment Policy

Prefer attaching:

* incident report Markdown file;
* worker report Markdown file if useful.

If attachments are not supported by the current Resend MCP tool call:

* embed incident report content in the email body;
* embed worker report content if useful;
* keep Telegram message short.

## Forbidden Resend Capabilities

The controller must not use these by default:

* received email reading;
* received email attachment download;
* contact creation;
* contact update;
* contact deletion;
* broadcast creation;
* broadcast sending;
* domain management;
* API key management;
* webhook management;
* segment management;
* topic management;
* contact property management.

## Failure Handling

If Resend email send succeeds:

* record success in notification intent;
* record email ID if returned;
* continue Telegram notification/reply flow.

If Resend email send fails:

* record error in notification intent;
* attempt Telegram notification;
* do not claim report was emailed.

If both Resend and Telegram fail:

* set state to `needs-user-decision`;
* write local artifacts;
* stop.

## Security Rules

Use a dedicated Resend API key.

Use a dedicated sender address.

Use a verified sender domain.

Do not use a personal mailbox as the agent identity.

Do not accept email replies as executable approvals by default.

Do not allow the agent to manage API keys or domains.

Do not use Resend inbound email features unless explicitly configured in a separate reviewed workflow.

