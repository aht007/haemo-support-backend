"""
Celery App Initialization Module
"""
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'haemosupport.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_pending_requests_alert': {
        'task': 'donation.tasks.send_pending_donations_alert',
        'schedule': crontab(hour='*/12'),
    },
}


@app.task(bind=True)
def debug_task(self):
    """
    function to debug celery related task's status˝
    """
    print(f'Request: {self.request!r}')
