#!/usr/bin/env bash
set -euo pipefail

N=2
PORT=$((8000 + N))
NET="docker-homework-${N}"
VOL="docker-homework-${N}-data"

docker network inspect "$NET" >/dev/null 2>&1 || docker network create "$NET"
docker volume  inspect "$VOL" >/dev/null 2>&1 || docker volume  create "$VOL"

docker build -f backend/Dockerfile  -t "backend:${N}"  .
docker build -f frontend/Dockerfile -t "frontend:${N}" .

docker rm -f "backend-${N}"  >/dev/null 2>&1 || true
docker rm -f "frontend-${N}" >/dev/null 2>&1 || true

docker run -d --name "backend-${N}" \
  --network "$NET" --network-alias backend \
  --cpus="0.5" --memory="256m" \
  -v "${VOL}:/data" \
  "backend:${N}"

docker run -d --name "frontend-${N}" \
  --network "$NET" \
  -p "${PORT}:8080" \
  --cpus="0.5" --memory="256m" \
  -e BACKEND_HOST=backend -e BACKEND_PORT=5000 \
  "frontend:${N}"

echo "Запущено: http://localhost:${PORT}/"