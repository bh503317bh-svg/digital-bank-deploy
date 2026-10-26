#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
DEPLOY_HOST="${DEPLOY_HOST:-101.36.108.141}"
DEPLOY_USER="${DEPLOY_USER:-ubuntu}"
DEPLOY_PORT="${DEPLOY_PORT:-22}"
REMOTE_DIR="${REMOTE_DIR:-/home/ubuntu/digital-bank}"

echo "Sync to ${DEPLOY_USER}@${DEPLOY_HOST}:${REMOTE_DIR}"
ssh -p "${DEPLOY_PORT}" "${DEPLOY_USER}@${DEPLOY_HOST}" "mkdir -p '${REMOTE_DIR}'"
rsync -az --delete \
  -e "ssh -p ${DEPLOY_PORT}" \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude 'dist' \
  --exclude '**/__pycache__' \
  --exclude '.env' \
  "${ROOT_DIR}/" "${DEPLOY_USER}@${DEPLOY_HOST}:${REMOTE_DIR}/"

ssh -p "${DEPLOY_PORT}" "${DEPLOY_USER}@${DEPLOY_HOST}" bash -s <<EOF
set -euo pipefail
if [ -d /home/ubuntu/finance-demo ]; then
  sudo docker compose -f /home/ubuntu/finance-demo/docker-compose.yml down -v || true
fi
cd '${REMOTE_DIR}/digital-bank-deploy'
sudo docker compose up -d --build
sudo docker network connect miru_net bank-nginx || true
EOF
echo "Deploy done. https://bank.windory.xyz/"
