#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENT_DIR="$ROOT/agent-bench"
TEST_DIR="$ROOT/eval/hidden_tests"

# Activate venv (adjust if yours differs)
if [ -f "$ROOT/.venvs/agent-bench/bin/activate" ]; then
  # shellcheck disable=SC1090
  source "$ROOT/.venvs/agent-bench/bin/activate"
else
  echo "ERROR: venv not found at $ROOT/.venvs/agent-bench"
  exit 1
fi

# Ensure Python can import: snake (from agent-bench) and eval (from repo root)
export PYTHONPATH="$AGENT_DIR:$ROOT"

# Run ONLY hidden tests and ignore any pytest.ini that might cause recursive collection
pytest -q -c /dev/null "$TEST_DIR"
