#!/usr/bin/env bash
set -euo pipefail

superset fab create-admin \
  --username "$ADMIN_USERNAME" \
  --firstname Superset \
  --lastname Admin \
  --email "$ADMIN_EMAIL" \
  --password "$ADMIN_PASSWORD"

superset db upgrade
superset init

# replace the shell with the real entrypoint
exec /usr/bin/run-server.sh
