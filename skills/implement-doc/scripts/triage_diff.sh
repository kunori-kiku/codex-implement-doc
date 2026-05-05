#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a git worktree. Lightweight diff triage skipped."
  exit 0
fi

echo "## git status --short"
git status --short || true

echo
echo "## git diff --name-status"
git diff --name-status || true

echo
echo "## git diff --stat"
git diff --stat || true

echo
echo "## git diff --check"
git diff --check || true
