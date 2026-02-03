#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENT_DIR="$ROOT/agent-bench"
TEST_DIR="$ROOT/eval/hidden_tests"

# Activate your venv (adjust if different)
if [ -f "$ROOT/.venvs/agent-bench/bin/activate" ]; then
  source "$ROOT/.venvs/agent-bench/bin/activate"
else
  echo "ERROR: venv not found at $ROOT/.venvs/agent-bench"
  exit 1
fi

export PYTHONPATH="$AGENT_DIR"
pytest -q "$TEST_DIR"
