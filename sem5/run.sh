#!/bin/bash

# stop if exists
docker stop mysql_db || true

# run mysql_container
docker run \
  --rm \
  --name mysql_db \
  -e MYSQL_ROOT_PASSWORD=root \
  -p 3307:3306 \
  -d \
  mariadb:latest

# run redis cache
docker run \
  --rm \
  --name redis_cache \
  -p 6379:6379 \
  -d \
  redis:latest

# wait for MYSQL is up
sleep 5

# activate virtual environment
source ../.venv/bin/activate

# create database
python ../db_init/create_database.py

# run flask application for internal users
python external_app/app.py