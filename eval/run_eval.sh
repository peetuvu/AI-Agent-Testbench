#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENT_DIR="$ROOT/agent-bench"

# activate venv (adjust if you place it elsewhere)
if [ -f "$ROOT/.venvs/agent-bench/bin/activate" ]; then
  # shellcheck disable=SC1090
  source "$ROOT/.venvs/agent-bench/bin/activate"
else
  echo "ERROR: venv not found at $ROOT/.venvs/agent-bench"
  exit 1
fi

export PYTHONPATH="$AGENT_DIR"

pytest -q "$ROOT/eval/hidden_tests" "$ROOT/eval/test_passk.py"
