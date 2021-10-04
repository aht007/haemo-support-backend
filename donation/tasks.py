"""
Tasks Module for celery tasks
"""
from celery import shared_task

from .services import send_pending_donation_requests_alert


@shared_task
def send_pending_donations_alert():
    """
    Sends email alerts to admins for pending donation requests
    after every 12 hours
    """
    send_pending_donation_requests_alert()
