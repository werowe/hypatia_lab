#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
LOG_FILE="$SCRIPT_DIR/airport_tracker.log"
PYTHON_BIN="${PYTHON_BIN:-/home/werowe/venvs/main/bin/python3}"

{
  echo "===== $(date -Iseconds) daily collection started ====="
  if [ -f "$SCRIPT_DIR/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    . "$SCRIPT_DIR/.env"
    set +a
  fi
  "$PYTHON_BIN" "$SCRIPT_DIR/tracker.py" collect --hours 24
  flight_result=$?
  "$PYTHON_BIN" "$SCRIPT_DIR/collect_restrictions.py"
  restrictions_result=$?
  "$PYTHON_BIN" "$SCRIPT_DIR/restriction_report.py" --html "$SCRIPT_DIR/dashboard.html"
  dashboard_result=$?
  result=0
  if [ "$flight_result" -ne 0 ] || [ "$restrictions_result" -ne 0 ] || [ "$dashboard_result" -ne 0 ]; then result=1; fi
  echo "Collector exits: flights=$flight_result restrictions=$restrictions_result dashboard=$dashboard_result"
  echo "===== $(date -Iseconds) daily collection finished (exit=$result) ====="
  exit "$result"
} >> "$LOG_FILE" 2>&1
