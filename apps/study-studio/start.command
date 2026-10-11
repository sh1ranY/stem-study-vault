#!/bin/zsh
set -e
cd -- "$(dirname -- "$0")"
# The launcher never prints environment secrets or installs system-wide packages.
if ! command -v python3 >/dev/null || ! command -v npm >/dev/null; then
  echo 'Learning Studio needs Python 3.10+ and Node.js 20.19+ / 22.12+.'
  echo 'Install them, then open this launcher again.'
  read -r 'reply?Press Return to close. '
  exit 1
fi
if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
fi
if [[ ! -f .venv/.studio-installed ]] || [[ requirements.txt -nt .venv/.studio-installed ]]; then
  .venv/bin/python -m pip install -r requirements.txt
  touch .venv/.studio-installed
fi
if [[ ! -d node_modules ]]; then
  npm ci
fi
.venv/bin/python -m alembic upgrade head
if ! .venv/bin/python - <<'PYIMPORT'
from backend.pilot import store
raise SystemExit(0 if store.fetch('config','shared','current-course') else 1)
PYIMPORT
then
  .venv/bin/python -m backend.pilot.import_course
fi
npm run build
if .venv/bin/python - <<'PY'
import urllib.request,json
try:
    with urllib.request.urlopen('http://127.0.0.1:8765/api/config',timeout=2) as r:
        result=json.load(r)
    raise SystemExit(0 if result.get('mode')=='local-prototype' else 1)
except Exception:
    raise SystemExit(1)
PY
then
  echo 'Learning Studio is already running. Opening it now.'
  open 'http://127.0.0.1:8765'
  exit 0
fi
.venv/bin/python -m uvicorn backend.app:app --host 127.0.0.1 --port 8765 &
studio_server_pid=$!
trap 'kill "$studio_server_pid" 2>/dev/null || true' EXIT INT TERM
for attempt in {1..30}; do
  if curl --fail --silent 'http://127.0.0.1:8765/api/config' >/dev/null; then
    open 'http://127.0.0.1:8765'
    echo 'Keep this window open during your demonstration. Press Control-C to stop.'
    wait "$studio_server_pid"
    exit 0
  fi
  if ! kill -0 "$studio_server_pid" 2>/dev/null; then
    echo 'The server could not start. Check whether port 8765 is occupied.'
    exit 1
  fi
  sleep 0.2
done
echo 'The server did not become ready. See the message above.'
exit 1
