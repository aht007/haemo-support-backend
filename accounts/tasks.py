"""
Tasks Module for celery tasks
"""
from celery import shared_task

from .services import send_mail_to_new_users


@shared_task
def send_email_for_password_creation(data):
    """
    Queues the execution of sending mail to new users and
    sends them when a worker is available
    """
    send_mail_to_new_users(data)
