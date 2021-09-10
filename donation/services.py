from python_http_client import exceptions
import sendgrid
from haemosupport.settings import (
    SENDGRID_API_KEY, DEFAULT_FROM_EMAIL,
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

        MailService.send_mail(
            sender, subject, recepient_email, htmlContent)

    @staticmethod
    def send_email_to_requestor(data):
        recepient_email = data.created_by.email
        subject = "Donation Request Update"
        sender = DEFAULT_FROM_EMAIL
        htmlContent = render_to_string('donation/requestor.html', {data: data})
        MailService.send_mail(
            sender, subject, recepient_email, htmlContent)

    @staticmethod
    def send_mail(from_email, subject, to_email, content):
        sendGridClient = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": to_email
                        }
                    ],
                    "subject": subject
                }
            ],
            "from": {
                "email": from_email
            },
            "content": [
                {
                    "type": "text/plain",
                    "value": content
                }
            ]
        }
        try:
            sendGridClient.client.mail.send.post(
                request_body=data)
        except exceptions.BadRequestsError as e:
            print(e.body)


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
