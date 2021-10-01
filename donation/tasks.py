from celery.task.schedules import crontab
from celery.decorators import periodic_task


@periodic_task(run_every=(crontab(minute='*/15')),
               name="send_pending_donations_alert", ignore_result=True)
def send_pending_donations_alert():
    """
    Sends email alerts to admins for pending donation requests
    after every 12 hours
    """
    pass
