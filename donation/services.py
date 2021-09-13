from django.core.mail import send_mail
from haemosupport.settings import (
    DEFAULT_FROM_EMAIL,
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
from twilio.rest import Client
import twilio
from django.template.loader import render_to_string


class MailService:
    @staticmethod
    def send_email_to_donor(data):
        recepient_email = data.donor.email
        subject = "Donation Request Update"
        sender = DEFAULT_FROM_EMAIL
        html_content = render_to_string('donation/donor.html', {"data": data})
        send_mail(subject, html_content,
                  sender,
                  [
                      recepient_email,
                  ],
                  fail_silently=False
                  )

    @staticmethod
    def send_email_to_requestor(data):
        recepient_email = data.created_by.email
        subject = "Donation Request Update"
        sender = DEFAULT_FROM_EMAIL
        html_content = render_to_string(
            'donation/requestor.html', {"data": data})
        print(html_content)
        send_mail(subject, html_content,
                  sender,
                  [
                      recepient_email,
                  ],
                  fail_silently=False
                  )


class SmsService:
    @staticmethod
    def send_sms(body, toNumber, fromNumber):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        try:
            client.messages.create(
                body=body,
                from_=fromNumber,
                to=toNumber,
            )
        except twilio.base.exceptions.TwilioRestException as exception:
            print(exception)
