import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TradingNetwork.settings')

app = Celery('TradingNetwork')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every 3h
    'add-debt-every-three-hours': {
        'task': 'coreapp.tasks.celery_raise_debt',
        'schedule': crontab(minute=0, hour='*/3')
    },
    # Executes every day at 6:30 a.m.
    'reduce-debt-every-day': {
        'task': 'coreapp.tasks.celery_raise_debt',
        'schedule': crontab(hour=6, minute=30)
    }
}
