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
        htmlContent = render_to_string('donation/donor.html', {data: data})

        MailService.send_email(
            sender, subject, recepient_email, htmlContent)

    @staticmethod
    def send_email_to_requestor(data):
        recepient_email = data.created_by.email
        subject = "Donation Request Update"
        sender = DEFAULT_FROM_EMAIL
        htmlContent = render_to_string('donation/requestor.html', {data: data})
        print(htmlContent)
        MailService.send_email(
            sender, subject, recepient_email, htmlContent)

    @staticmethod
    def send_email(from_email, subject, to_email, content):
        send_mail(subject, content,
                  from_email,
                  [
                      to_email
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
