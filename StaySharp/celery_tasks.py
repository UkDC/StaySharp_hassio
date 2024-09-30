from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

# Задаем переменную окружения, содержащую название файла настроек нашего проекта.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StaySharp.settings')
app = Celery('StaySharp')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # Executes every Monday morning at 6:30 a.m.
    'report_of_week': {
        'task': 'report',
        'schedule': crontab(minute=30, hour=6, day_of_week=1),
        # 'schedule': crontab(minute=30, hour=6),
    },
    # Executes every day at 6:30 a.m.
    'check-registration': {
        'task': 'check_registration',
        'schedule': crontab(minute=30, hour=6)
    },
    # Executes every 2 min
    'Test': {
        'task': 'report',
        'schedule': 120,
    },
}

app.conf.timezone = "Europe/Kiev"


