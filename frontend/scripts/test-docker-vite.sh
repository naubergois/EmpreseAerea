#!/usr/bin/env bash
# Verifica que a imagem Docker do frontend instala Vite corretamente
# e não sofre do erro: Cannot find module '.../dep-D-7KCb9p.js'
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-skyagent-frontend-test}"
FRONTEND_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Building Docker image: ${IMAGE_NAME}"
docker build -t "${IMAGE_NAME}" "${FRONTEND_DIR}"

echo "==> Checking Vite chunk integrity inside container"
docker run --rm "${IMAGE_NAME}" sh -c '
  CHUNKS_DIR="node_modules/vite/dist/node/chunks"
  if [ ! -d "$CHUNKS_DIR" ]; then
    echo "FAIL: $CHUNKS_DIR does not exist"
    exit 1
  fi
  COUNT=$(find "$CHUNKS_DIR" -name "dep-*.js" | wc -l | tr -d " ")
  if [ "$COUNT" -lt 2 ]; then
    echo "FAIL: expected multiple vite dep-*.js chunks, found $COUNT"
    exit 1
  fi
  echo "OK: found $COUNT vite chunk files"
'

echo "==> Running production build inside container"
docker run --rm "${IMAGE_NAME}" npm run build

echo "==> Starting dev server and checking HTTP response"
HOST_PORT="${HOST_PORT:-5174}"
CONTAINER_ID=$(docker run -d -p "${HOST_PORT}:5173" "${IMAGE_NAME}")
trap 'docker rm -f "${CONTAINER_ID}" >/dev/null 2>&1 || true' EXIT

for i in $(seq 1 30); do
  if curl -sf "http://localhost:${HOST_PORT}/" >/dev/null 2>&1; then
    BODY=$(curl -s "http://localhost:${HOST_PORT}/")
    if echo "${BODY}" | grep -q "SkyAgent"; then
      echo "OK: dev server responded with SkyAgent page"
      echo "All Docker Vite checks passed."
      exit 0
    fi
  fi
  sleep 1
done

echo "FAIL: dev server did not respond in time"
docker logs "${CONTAINER_ID}" 2>&1 | tail -30
exit 1
