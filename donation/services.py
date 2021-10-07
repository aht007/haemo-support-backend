"""
Service for Email and Sms Notification
"""
import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q

from twilio.rest import Client
import twilio

from haemosupport.settings import (
    DEFAULT_FROM_EMAIL,
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
from accounts.models import User
from .models import DonationRequest, Status


def send_email_to_donor(data):
    """
    Function to send mail to donor
    """
    recepient_email = data.donor.email
    subject = "Donation Request Update"
    sender = DEFAULT_FROM_EMAIL
    html_content = render_to_string('donation/donor.html', {"data": data})
    plain_text = strip_tags(html_content)
    send_mail(subject, plain_text,
              sender,
              [
                  recepient_email,
              ],
              html_message=html_content,
              fail_silently=False
              )


def send_email_to_requestor(data):
    """
    Function to send mail to requestor
    """
    recepient_email = data.created_by.email
    subject = "Donation Request Update"
    sender = DEFAULT_FROM_EMAIL
    html_content = render_to_string(
        'donation/requestor.html', {"data": data})
    plain_text = strip_tags(html_content)
    send_mail(subject, plain_text,
              sender,
              [
                  recepient_email,
              ],
              html_message=html_content,
              fail_silently=False
              )


def send_pending_donations_reminder_to_admins():
    """
    Send donation reminder alerts to admins
    """
    admin_users = User.objects.filter(is_admin=True)
    pending_requests_count = DonationRequest.objects.filter(
        status=Status.PENDING).count()
    for admin in admin_users:
        recepient_email = admin.email
        subject = "Reminder"
        sender = DEFAULT_FROM_EMAIL
        html_content = render_to_string(
            'donation/admin_reminder.html', {
                "username": admin.username,
                "requests_count": pending_requests_count
            })
        plain_text = strip_tags(html_content)
        send_mail(subject, plain_text,
                  sender,
                  [
                      recepient_email,
                  ],
                  html_message=html_content,
                  fail_silently=False
                  )


def send_pending_donations_reminder_to_users():
    """
    Send donation reminder alerts to users
    """
    users = User.objects.filter(is_admin=False)
    pending_requests = DonationRequest.objects.filter(
        status=Status.APPROVED)
    for user in users:
        recepient_email = user.email
        subject = "Reminder"
        sender = DEFAULT_FROM_EMAIL
        html_content = render_to_string(
            'donation/user_reminder.html', {
                "username": user.username,
                "pending_requests": pending_requests
            })
        plain_text = strip_tags(html_content)
        send_mail(subject, plain_text,
                  sender,
                  [
                      recepient_email,
                  ],
                  html_message=html_content,
                  fail_silently=False
                  )


def send_pending_donation_requests_alert():
    """
    Send donation reminder alerts to admins and users
    """
    send_pending_donations_reminder_to_admins()
    send_pending_donations_reminder_to_users()


def send_sms(body, to_number, from_number):
    """
    Function to send sms
    """
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=body,
            from_=from_number,
            to=to_number,
        )
    except twilio.base.exceptions.TwilioRestException as exception:
        print(exception)


def send_awaited_request_notification(donation_request):
    """
    Sends alert for donation request that is due soon
    """
    sender = DEFAULT_FROM_EMAIL
    html_content = render_to_string(
        'donation/donor_reminder.html', {
            "request": donation_request
        })
    plain_text = strip_tags(html_content)
    send_mail("Donation Due Soon", plain_text,
              sender,
              [
                  donation_request.donor.email,
              ],
              html_message=html_content,
              fail_silently=False
              )


def send_soon_due_pending_request_notification():
    """
    Sends alert for donation request that is due soon and is still pending
    """
    users = User.objects.filter(is_admin=False)
    date_today = datetime.date.today()
    date_tomorrow = date_today + datetime.timedelta(days=1)
    pending_requests = DonationRequest.objects.filter(
        Q(date_required__range=[date_today, date_tomorrow]) &
        Q(status=Status.APPROVED))
    for user in users:
        recepient_email = user.email
        subject = "Reminder"
        sender = DEFAULT_FROM_EMAIL
        html_content = render_to_string(
            'donation/user_reminder.html', {
                "username": user.username,
                "pending_requests": pending_requests
            })
        plain_text = strip_tags(html_content)
        send_mail(subject, plain_text,
                  sender,
                  [
                      recepient_email,
                  ],
                  html_message=html_content,
                  fail_silently=False
                  )
