[Codex {{SEVERITY}}] Roadmap decision required

Run: {{RUN_ID}}
Incident: {{INCIDENT_ID}}
Task: {{TASK_ID}}
Roadmap: {{ROADMAP_DOC}}

Summary:
{{SUMMARY}}

Recommended choice:
{{RECOMMENDED_CHOICE}}

Why:
{{RECOMMENDED_REASON}}

Remediation options:
{{REMEDIATION_OPTIONS_BRIEF}}

I sent the full incident report to your email through Resend.

I may also send the incident report below or as an attached Markdown file.

Reply with one of:

A {{NONCE}} — Continue current route and update roadmap later
B {{NONCE}} — Revert worker changes for this task
C {{NONCE}} — Keep partial changes and redirect
D {{NONCE}} — I will provide a new roadmap section
E {{NONCE}} — Stop this implementation run
F {{NONCE}} — Run read-only verifier first
G {{NONCE}} — Approve non-privileged MCP-agent remediation
H {{NONCE}} — Approve privileged remediation only after independent safety review

Or:

CUSTOM {{NONCE}} <your instruction>

Examples:

C {{NONCE}}

CUSTOM {{NONCE}} keep the GPU filtering changes, but revert solver API changes and add an explicit no-public-API-change constraint to the roadmap

For H, newly privileged or dangerous actions require an operator plan plus independent read-only safety review first. Already-approved danger-full-access alone does not trigger that extra gate and is treated as the normal efficient worker mode for this run.
