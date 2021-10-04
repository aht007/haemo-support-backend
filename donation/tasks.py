from celery import shared_task

from .services import MailService


@shared_task
def send_pending_donations_alert():
    """
    Sends email alerts to admins for pending donation requests
    after every 12 hours
    """
    MailService.send_pending_donation_requests_alert()
