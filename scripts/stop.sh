#!/usr/bin/env bash
set -euo pipefail

N=2
docker rm -f "frontend-${N}" >/dev/null 2>&1 || true
docker rm -f "backend-${N}"  >/dev/null 2>&1 || true
echo "Контейнеры остановлены. Volume docker-homework-${N}-data сохранён."