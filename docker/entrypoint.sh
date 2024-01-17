#!/usr/bin/env sh

set -e

# Ожидаем запуска postgres
dockerize -wait tcp://psql:${PSQL_PORT}

# Миграция и синхронизация
python model/engine.py

# Запуск команды
python app.py
