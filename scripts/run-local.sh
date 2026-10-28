#!/bin/sh
set -eu
DEPLOY_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
ROOT_DIR=$(CDPATH= cd -- "$DEPLOY_DIR/.." && pwd)
LOCAL_DIR=/tmp/digital-bank-local
LOCAL_COMPOSE=/tmp/digital-bank-local-compose.yml
if [ ! -f "$DEPLOY_DIR/.env" ]; then
  echo "Create $DEPLOY_DIR/.env from .env.example and configure the API key first." >&2
  exit 1
fi
mkdir -p "$LOCAL_DIR"
rsync -a --exclude=.git --exclude=.env --exclude=node_modules --exclude=__pycache__ \
  "$ROOT_DIR/digital-bank-core" "$ROOT_DIR/digital-bank-backend" "$ROOT_DIR/digital-bank-h5-app" \
  "$ROOT_DIR/digital-bank-h5-admin" "$DEPLOY_DIR" "$LOCAL_DIR/"
python3 - "$LOCAL_DIR/digital-bank-deploy/docker-compose.yml" "$LOCAL_COMPOSE" <<'PY'
from pathlib import Path
import sys
text = Path(sys.argv[1]).read_text()
text = text.replace('    networks:\n      - default\n      - miru_net\n', '')
text = text.replace('\nnetworks:\n  miru_net:\n    external: true\n    name: miru_net\n', '\n')
text = text.replace('8088:80', '127.0.0.1:18088:80')
Path(sys.argv[2]).write_text(text)
PY
docker compose --project-directory "$LOCAL_DIR/digital-bank-deploy" --env-file "$DEPLOY_DIR/.env" -f "$LOCAL_COMPOSE" up -d --build
printf 'Open http://127.0.0.1:18088/\n'
