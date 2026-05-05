#!/usr/bin/env python3
"""
Initialize or locate an implement-doc run state file.

This script is intentionally simple and deterministic.
It does not call Codex MCP.
It does not call Resend MCP.
It does not call Telegram MCP.
It does not call Signal MCP.

The controller is responsible for:
- creating/resuming the MCP worker;
- writing worker_thread_id;
- sending notifications;
- writing remote decisions.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


MELBOURNE_TZ = timezone(timedelta(hours=10))


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "implement-doc"


def git_branch(repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
        branch = result.stdout.strip()
        return branch or None
    except Exception:
        return None


def now_iso() -> str:
    return datetime.now(MELBOURNE_TZ).isoformat(timespec="seconds")


def now_stamp() -> str:
    return datetime.now(MELBOURNE_TZ).strftime("%Y%m%d-%H%M%S")


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def find_matching_state(
    state_dir: Path,
    repo_root: Path,
    roadmap_doc: str,
    branch: str | None,
) -> Path | None:
    if not state_dir.exists():
        return None

    roadmap_norm = os.path.normpath(roadmap_doc)
    repo_norm = str(repo_root.resolve())

    active_statuses = {
        "active",
        "paused",
        "needs-user-decision",
        "waiting-remote-decision",
    }

    for path in sorted(state_dir.glob("*.json"), reverse=True):
        data = load_json(path)
        if not data:
            continue

        if data.get("status") not in active_statuses:
            continue

        if os.path.normpath(str(data.get("roadmap_doc", ""))) != roadmap_norm:
            continue

        if str(Path(data.get("repo_root", "")).resolve()) != repo_norm:
            continue

        if branch and data.get("branch") and data.get("branch") != branch:
            continue

        return path

    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--roadmap-doc", required=True)
    parser.add_argument("--title", default=None)
    parser.add_argument("--force-new", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    branch = git_branch(repo_root)
    title = args.title or Path(args.roadmap_doc).stem
    slug = slugify(title)

    base_dir = repo_root / ".codex-orchestrator" / "implement-doc"
    state_dir = base_dir / "state"
    reports_dir = base_dir / "reports"
    incidents_dir = base_dir / "incidents"
    prompts_dir = base_dir / "prompts"
    decisions_dir = base_dir / "decisions"
    remote_decisions_dir = base_dir / "remote-decisions"
    notifications_dir = base_dir / "notifications"

    for directory in [
        state_dir,
        reports_dir,
        incidents_dir,
        prompts_dir,
        decisions_dir,
        remote_decisions_dir,
        notifications_dir,
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    if not args.force_new:
        existing = find_matching_state(state_dir, repo_root, args.roadmap_doc, branch)
        if existing:
            print(json.dumps({
                "created": False,
                "state_path": str(existing),
                "state": load_json(existing),
            }, indent=2, ensure_ascii=False))
            return 0

    stamp = now_stamp()
    run_id = f"{stamp}-{slug}"
    state_path = state_dir / f"{run_id}.json"

    state = {
        "run_id": run_id,
        "title": title,
        "roadmap_doc": args.roadmap_doc,
        "repo_root": str(repo_root),
        "branch": branch,
        "worker_thread_id": None,
        "status": "active",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "current_milestone": None,
        "current_task_id": None,
        "roadmap_summary": {
            "goals": [],
            "non_goals": [],
            "constraints": [],
            "milestones": [],
            "acceptance_checks": [],
            "risks": []
        },
        "completed_tasks": [],
        "open_tasks": [],
        "blocked_tasks": [],
        "reports": [],
        "incidents": [],
        "decisions": [],
        "remote_decisions": [],
        "notifications": [],
        "last_verified_git_head": None,
        "last_worker_summary": None,
        "last_lightweight_diff_triage": {
            "git_status_short": None,
            "git_diff_name_status": None,
            "git_diff_stat": None,
            "git_diff_check": None
        },
        "unresolved_user_decision": None,
        "pending_remote_decision": None,
        "notification_config": {
            "enabled": True,
            "auto_send_allowed": True,
            "notify_channels": [
                "resend",
                "telegram_notifier"
            ],
            "primary_notification_channel": "resend",
            "reply_channel": "telegram_notifier",
            "resend_mode": "notify_only",
            "telegram_mode": "plain_text_reply",
            "send_incident_report": True,
            "send_worker_report": True,
            "resend": {
                "enabled": True,
                "mode": "notify_only",
                "from": "Codex Orchestrator <codex-alert@example.com>",
                "to": [],
                "cc": [],
                "bcc": [],
                "reply_to": None,
                "allow_inbound_email_decisions": False,
                "allow_contact_management": False,
                "allow_broadcasts": False,
                "allow_domain_management": False,
                "allow_api_key_management": False,
                "allow_webhook_management": False
            },
            "telegram": {
                "enabled": True,
                "mode": "plain_text_reply",
                "allowed_responders": {
                    "telegram_user_ids": []
                }
            },
            "signal": {
                "enabled": False,
                "mode": "future_fixed_recipient_notify_only",
                "reason": "Do not use generic signal_mcp; existing small MCP exposes send/receive account access and is under-hardened."
            }
        },
        "mcp_tool_map": {
            "resend": {
                "server": "resend",
                "role": "notify_only_email_sender",
                "send_email_tool": "use_the_email_send_tool_exposed_by_resend_mcp",
                "forbidden_tool_groups": [
                    "received_emails",
                    "contacts",
                    "broadcasts",
                    "domains",
                    "segments",
                    "topics",
                    "contact_properties",
                    "api_keys",
                    "webhooks"
                ]
            },
            "telegram": {
                "server": "telegram_notifier",
                "send_message": "send_message",
                "send_document": "send_document",
                "get_updates": "get_updates"
            },
            "signal": {
                "server": None,
                "enabled": False
            }
        },
        "notification_intents": []
    }

    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps({
        "created": True,
        "state_path": str(state_path),
        "state": state,
    }, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
