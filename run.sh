#!/usr/bin/env bash
python manage.py migrate  # Применение миграций базы данных
python manage.py runserver 0.0.0.0:8000  # Запуск сервера

