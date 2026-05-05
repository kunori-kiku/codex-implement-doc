#!/usr/bin/env python3
"""
Heuristic incident classifier for implement-doc.

This script is not authoritative.
The controller must make the final judgment.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CRITICAL_PATTERNS = [
    r"secret",
    r"credential leak",
    r"credential exposure",
    r"credential handling",
    r"password",
    r"token",
    r"\bauth\b",
    r"authentication logic",
    r"authorization logic",
    r"security-sensitive",
    r"deploy",
    r"production",
    r"migration",
    r"rm\s+-rf",
    r"sudo",
    r"destructive",
    r"irreversible",
    r"ownership",
    r"chown",
    r"chmod\s+-r",
    r"service restart",
]

ROADMAP_CONTRADICTION_PATTERNS = [
    r"contradict",
    r"opposite",
    r"replaced architecture",
    r"changed public api",
    r"ignored constraint",
    r"not as roadmap",
]

AMBIGUITY_PATTERNS = [
    r"ambiguous",
    r"missing dependency",
    r"missing package",
    r"missing tool",
    r"missing runtime",
    r"missing compiler",
    r"missing interpreter",
    r"missing credential",
    r"environment",
    r"mcp.*unavailable",
    r"mcp.*failed",
    r"permission denied",
    r"authorization",
    r"quota",
    r"sandbox",
    r"network access",
    r"timeout",
    r"timed out",
    r"cannot notify",
    r"notification.*failed",
    r"telegram.*failed",
    r"resend.*failed",
    r"operational blocker",
    r"blocked by environment",
    r"cannot choose",
    r"user decision",
    r"blocked",
    r"unclear",
]

LOCAL_DEVIATION_PATTERNS = [
    r"unexpected file",
    r"partial",
    r"test missing",
    r"nearby dependency",
    r"small deviation",
]


def contains_any(text: str, patterns: list[str]) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in patterns)


def classify(text: str) -> str:
    if contains_any(text, CRITICAL_PATTERNS):
        return "SEV0"

    if contains_any(text, ROADMAP_CONTRADICTION_PATTERNS):
        return "SEV1"

    if contains_any(text, AMBIGUITY_PATTERNS):
        return "SEV2"

    if contains_any(text, LOCAL_DEVIATION_PATTERNS):
        return "SEV3"

    return "SEV4"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default=None)
    parser.add_argument("--file", default=None)
    args = parser.parse_args()

    if not args.text and not args.file:
        raise SystemExit("Provide --text or --file")

    text = args.text or Path(args.file).read_text(encoding="utf-8", errors="replace")
    severity = classify(text)

    print(json.dumps({
        "severity": severity,
        "note": "Heuristic only. Controller must make final judgment."
    }, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
