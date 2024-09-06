# Инструкции для запуска контейнеров

Сбор образа микросервиса для внешних клиентов
```
cd external_app/
docker build -t external_app:v0.1 -f Dockerfile .
```

Сбор образа микросервиса для внутренних клиентов
```
cd main_app/
docker build -t main_app:v0.1 -f Dockerfile .
```

Проверка образов
```
docker images | grep external_app
dokcer images | grep main_app
```

Запуск контейнера с mysql
```
docker run \
  --rm \
  --name mysql_db \
  -e MYSQL_ROOT_PASSWORD=root \
  -p 3307:3306 \
  -d \
  mariadb:latest
```

Запуск контейнера с redis
```
docker run \
  --rm \
  --name redis_cache \
  -p 6379:6379 \
  -d \
  redis:latest
```

Запуск контейнера с микросервисом для внешних клиентов
```
docker run \
  --rm \
  --name external_app \
  -p 8082:8081 \
  -v $(pwd)/configs/db.json:/app/configs/db.json \
  -d \
  external_app:v0.1
```

Запуск контейнера с микросервисом для внутренних клиентов
```
docker run \
  --rm \
  --name main_app \
  -p 8083:8080 \
  -v $(pwd)/configs/db.json:/app/configs/db.json \
  -d \
  main_app:v0.1
```