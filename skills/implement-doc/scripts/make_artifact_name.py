#!/usr/bin/env python3
"""
Create deterministic timestamped artifact names for implement-doc reports,
incidents, prompts, decisions, notifications, and remote decisions.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone, timedelta


MELBOURNE_TZ = timezone(timedelta(hours=10))


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "artifact"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--kind",
        choices=[
            "report",
            "incident",
            "prompt",
            "decision",
            "notification",
            "remote-decision",
            "resend-email",
            "telegram-message"
        ],
        required=True,
    )
    parser.add_argument("--task-id", default=None)
    parser.add_argument("--incident-id", default=None)
    parser.add_argument("--severity", default=None)
    parser.add_argument("--title", required=True)
    parser.add_argument("--ext", default="md")
    args = parser.parse_args()

    stamp = datetime.now(MELBOURNE_TZ).strftime("%Y%m%d-%H%M%S")
    slug = slugify(args.title)

    parts = [stamp]

    if args.severity:
        parts.append(args.severity.lower())

    if args.incident_id:
        parts.append(slugify(args.incident_id))

    if args.task_id:
        parts.append(slugify(args.task_id))

    parts.append(slug)

    print("-".join(parts) + "." + args.ext.lstrip("."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
