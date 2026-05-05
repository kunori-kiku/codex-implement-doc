[Codex {{SEVERITY}}] Roadmap decision required

Run: {{RUN_ID}}
Incident: {{INCIDENT_ID}}
Task: {{TASK_ID}}
Roadmap: {{ROADMAP_DOC}}
Worker report: {{WORKER_REPORT_PATH}}
Incident report: {{INCIDENT_REPORT_PATH}}

Summary:
{{SUMMARY}}

Recommended choice:
{{RECOMMENDED_CHOICE}}

Why:
{{RECOMMENDED_REASON}}

Required action:
Reply in Telegram, not email.

Telegram reply format:

A {{NONCE}} — Continue current route and update roadmap later
B {{NONCE}} — Revert worker changes for this task
C {{NONCE}} — Keep partial changes and redirect
D {{NONCE}} — I will provide a new roadmap section
E {{NONCE}} — Stop this implementation run
F {{NONCE}} — Run read-only verifier first
CUSTOM {{NONCE}} <your instruction>

Example:
C {{NONCE}}

Example custom instruction:
CUSTOM {{NONCE}} keep the GPU filtering changes, but revert solver API changes and add an explicit no-public-API-change constraint to the roadmap

Incident Report:
{{INCIDENT_REPORT_CONTENT}}

Worker Report:
{{WORKER_REPORT_CONTENT}}

Notes:
This email is notification-only.
Executable decisions are accepted through allowlisted Telegram plain-text replies only.
