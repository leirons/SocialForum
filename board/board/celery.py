import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'board.settings')

app = Celery('board')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

app.conf.update(
    result_expires=3600,
    enable_utc = True,
    timezone = 'Europe/London'
)

app.conf.beat_schedule = {
    "see-you-in-ten-seconds-task": {
        "task": 'mysite.tasks.send_logs',
        "schedule":120.0
    }
}