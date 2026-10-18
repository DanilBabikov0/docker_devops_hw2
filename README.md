# docker-homework-2

Бабиков Данил Александрович

Контейнерный стенд для домашнего задания по Docker.

## Параметры варианта

| Параметр | Значение |
|---|---|
| N (номер варианта) | 2 |
| Проект | docker-homework-2 |
| Внешний порт | 8002 |
| Персональный идентификатор | `1E34A93D` |
| Теги образов | `backend:2`, `frontend:2` |
| Сеть | `docker-homework-2` (bridge, 172.20.0.0/16) |
| Volume | `docker-homework-2-data` |
| Неисправность (N % 4 = 2) | неверное имя backend во frontend |

## Состав

- `backend/` — Flask-сервис, отдаёт JSON с именем, вариантом, ID, hostname, темой и содержимым volume-файла.
- `frontend/` — Flask-сервис, отдаёт стартовую страницу и проксирует `/api` на backend по имени контейнера.
- `scripts/start.sh` — создаёт сеть и volume, собирает образы, запускает контейнеры (идемпотентен).
- `scripts/stop.sh` — удаляет контейнеры, volume сохраняет.

## Запуск

```bash
chmod +x scripts/start.sh scripts/stop.sh
./scripts/start.sh
```

## Остановка

```bash
chmod +x scripts/start.sh scripts/stop.sh
./scripts/stop.sh
```

## Проверки

```bash
curl http://localhost:8002/                # стартовая страница
curl http://localhost:8002/api             # JSON от backend через frontend
docker ps                                  # оба Up (healthy)
docker port backend-2                      # пусто backend не публикуется
docker network inspect docker-homework-2   # оба контейнера в сети
docker stats --no-stream                   # лимиты видны
docker inspect backend-2 frontend-2 \
  --format '{{.Name}} cpus={{.HostConfig.NanoCpus}} mem={{.HostConfig.Memory}}'
```

Ожидаемые лимиты: cpus=500000000 (0.5 CPU), mem=268435456 (256 MiB) у обоих.

## Неисправности

```bash
docker rm -f frontend-2
docker run -d --name frontend-2 \
  --network docker-homework-2 \
  -p 8002:8080 \
  --cpus="0.5" --memory="256m" \
  -e BACKEND_HOST=wrong-backend -e BACKEND_PORT=5000 \
  frontend:2

curl -i http://localhost:8002/        # 200
curl -i http://localhost:8002/api     # 502
```

Исправление просто перезапустить

```bash
./scripts/start.sh
curl -i http://localhost:8002/api    # 200
```

