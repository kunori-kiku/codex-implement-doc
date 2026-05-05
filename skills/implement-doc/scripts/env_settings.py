#!/usr/bin/env python3
"""Load implement-doc workflow notification settings from `.env`."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def find_codex_home(start: Path) -> Path:
    current = start.resolve()
    candidates = [current, *current.parents]
    for candidate in candidates:
        if (candidate / "config.toml").exists() and (
            candidate / "skills" / "implement-doc"
        ).exists():
            return candidate

    return Path(__file__).resolve().parents[3]


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" not in line:
            raise ValueError(f"{path}:{line_number}: expected KEY=VALUE")

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"{path}:{line_number}: empty key")
        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]
        values[key] = value

    return values


def load_env_settings(codex_home: Path | None = None) -> dict[str, str]:
    home = codex_home or find_codex_home(Path.cwd())
    env_values = parse_env_file(home / ".env")
    return {**env_values, **os.environ}


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def env_value(settings: dict[str, str], key: str, default: str | None = None) -> str | None:
    value = settings.get(key)
    if value is None or value == "":
        return default
    return value


def env_list(settings: dict[str, str], key: str) -> list[str]:
    return split_csv(settings.get(key))


def is_unfilled(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, list):
        return all(is_unfilled(item) for item in value)
    text = str(value).strip()
    return not text or "FILL_ME" in text or text in {"[]", "None", "null"}

