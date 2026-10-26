#!/usr/bin/env bash
set -euo pipefail
CONF_SRC="$(cd "$(dirname "$0")/.." && pwd)/nginx/bank.windory.xyz.conf"
CONF_DST="/opt/miru/runtime/nginx/conf.d/bank.windory.xyz.conf"
sudo docker network disconnect miru_net bank-nginx 2>/dev/null || true
sudo docker network connect miru_net bank-nginx 2>/dev/null || true
sudo cp "${CONF_SRC}" "${CONF_DST}"
sudo docker exec miru-nginx nginx -t
sudo docker exec miru-nginx nginx -s reload
echo "Exposed: https://bank.windory.xyz/  and  https://bank.windory.xyz/admin/"
