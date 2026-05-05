#!/usr/bin/env python3
"""
Parse a plain-text Telegram remote decision reply.

Supported forms:

A <nonce>
B <nonce>
C <nonce>
D <nonce>
E <nonce>
F <nonce>
G <nonce>
H <nonce>
CUSTOM <nonce> <freeform instruction>

This script only parses.
The controller must still validate:
- Telegram user ID allowlist;
- active incident;
- active nonce;
- stale decision status;
- safety of CUSTOM instructions.

Email replies are not parsed by default.
Resend is notification-only by default.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone, timedelta


MELBOURNE_TZ = timezone(timedelta(hours=10))


CHOICE_ACTIONS = {
    "A": "continue_current_route",
    "B": "revert_worker_changes_for_task",
    "C": "keep_partial_changes_and_redirect",
    "D": "pause_for_new_roadmap_section",
    "E": "stop_run",
    "F": "run_read_only_verifier_first",
    "G": "approve_non_privileged_mcp_remediation",
    "H": "approve_privileged_mcp_remediation_after_safety_review",
    "CUSTOM": "continue_with_custom_instruction"
}


def now_iso() -> str:
    return datetime.now(MELBOURNE_TZ).isoformat(timespec="seconds")


def parse_reply(raw_reply: str, expected_nonce: str) -> dict:
    text = raw_reply.strip()

    choice_match = re.fullmatch(r"([A-Ha-h])\s+(\S+)", text)
    if choice_match:
        choice = choice_match.group(1).upper()
        nonce = choice_match.group(2)
        nonce_ok = nonce == expected_nonce
        return {
            "parsed": True,
            "choice": choice,
            "nonce": nonce,
            "nonce_ok": nonce_ok,
            "custom_instruction": None,
            "controller_action": CHOICE_ACTIONS[choice],
            "error": None if nonce_ok else "nonce_mismatch"
        }

    custom_match = re.fullmatch(r"(?i)CUSTOM\s+(\S+)\s+(.+)", text, flags=re.DOTALL)
    if custom_match:
        nonce = custom_match.group(1)
        instruction = custom_match.group(2).strip()
        nonce_ok = nonce == expected_nonce
        return {
            "parsed": True,
            "choice": "CUSTOM",
            "nonce": nonce,
            "nonce_ok": nonce_ok,
            "custom_instruction": instruction,
            "controller_action": CHOICE_ACTIONS["CUSTOM"],
            "error": None if nonce_ok else "nonce_mismatch"
        }

    return {
        "parsed": False,
        "choice": None,
        "nonce": None,
        "nonce_ok": False,
        "custom_instruction": None,
        "controller_action": None,
        "error": "unrecognized_reply_format"
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reply", required=True)
    parser.add_argument("--nonce", required=True)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--incident-id", default=None)
    parser.add_argument("--telegram-user-id", default=None)
    parser.add_argument("--telegram-chat-id", default=None)
    parser.add_argument("--telegram-message-id", default=None)
    args = parser.parse_args()

    parsed = parse_reply(args.reply, args.nonce)

    output = {
        "timestamp": now_iso(),
        "source": "telegram_notifier",
        "telegram_user_id": args.telegram_user_id,
        "telegram_chat_id": args.telegram_chat_id,
        "telegram_message_id": args.telegram_message_id,
        "run_id": args.run_id,
        "incident_id": args.incident_id,
        "expected_nonce": args.nonce,
        "raw_reply": args.reply,
        **parsed
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
