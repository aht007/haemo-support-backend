"""
Service for Email and Sms Notification
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from twilio.rest import Client
import twilio

from haemosupport.settings import (
    DEFAULT_FROM_EMAIL,
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


class MailService:
    """
    Mail Service for donation request
    """
    @staticmethod
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

    @staticmethod
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


class SmsService:
    """
    Sms servcice for donation request
    """
    @staticmethod
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
