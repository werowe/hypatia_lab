#!/bin/bash
set -euo pipefail
umask 077

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"
LOG_FILE="$SCRIPT_DIR/deepstate_download.log"

exec >> "$LOG_FILE" 2>&1
echo "===== $(date -Iseconds) DeepState download started ====="
trap 'result=$?; echo "===== $(date -Iseconds) DeepState download finished (exit=$result) ====="' EXIT

"$PYTHON_BIN" - <<'PY'
import os
from dotenv import load_dotenv

load_dotenv(".env")
missing = [key for key in ("MONGODB_USER", "MONGODB_PWD", "CLUSTER") if not os.getenv(key)]
if missing:
    raise SystemExit("Missing MongoDB settings: " + ", ".join(missing) + ". Configure " + os.path.join(os.getcwd(), ".env"))
PY

"$PYTHON_BIN" -u "$SCRIPT_DIR/download_deepstate.py"

# Check only the historical-data load and gain selector after the download exits successfully.
# The notebook environment already contains GeoPandas/Shapely.
echo "===== $(date -Iseconds) DeepState hotspot check started ====="
/home/werowe/venvs/main/bin/python -u "$SCRIPT_DIR/check_hotspot.py"
echo "===== $(date -Iseconds) DeepState hotspot check finished ====="
