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

Remediation options:
{{REMEDIATION_OPTIONS_BRIEF}}

Detailed remediation notes are in the incident report.

Required action:
Reply in Telegram, not email.

Telegram reply format:

A {{NONCE}} — Continue current route and update roadmap later
B {{NONCE}} — Revert worker changes for this task
C {{NONCE}} — Keep partial changes and redirect
D {{NONCE}} — I will provide a new roadmap section
E {{NONCE}} — Stop this implementation run
F {{NONCE}} — Run read-only verifier first
G {{NONCE}} — Approve non-privileged MCP-agent remediation
H {{NONCE}} — Approve privileged remediation only after independent safety review
CUSTOM {{NONCE}} <your instruction>

For H, the controller must prepare an operator plan and use an independent read-only safety verifier before executing newly privileged or dangerous actions. This extra safety gate is not required merely because danger-full-access was already explicitly approved for this run; once recorded, that sandbox is treated as the normal efficient worker mode.

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
