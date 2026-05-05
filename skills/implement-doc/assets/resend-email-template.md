# [Codex {{SEVERITY}}] Roadmap decision required

**Run:** `{{RUN_ID}}`  
**Incident:** `{{INCIDENT_ID}}`  
**Task:** `{{TASK_ID}}`  
**Roadmap:** `{{ROADMAP_DOC}}`  
**Worker report:** `{{WORKER_REPORT_PATH}}`  
**Incident report:** `{{INCIDENT_REPORT_PATH}}`

## Summary

{{SUMMARY}}

## Recommended Choice

**{{RECOMMENDED_CHOICE}}**

{{RECOMMENDED_REASON}}

## Required Action

Reply in **Telegram**, not email.

Telegram reply format:

```text
A {{NONCE}} — Continue current route and update roadmap later
B {{NONCE}} — Revert worker changes for this task
C {{NONCE}} — Keep partial changes and redirect
D {{NONCE}} — I will provide a new roadmap section
E {{NONCE}} — Stop this implementation run
F {{NONCE}} — Run read-only verifier first

CUSTOM {{NONCE}} <your instruction>
