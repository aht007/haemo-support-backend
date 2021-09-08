from python_http_client import exceptions
import sendgrid
from sendgrid.helpers.mail import (Mail,
                                   Email,
                                   Personalization
                                   )
from haemosupport.settings import (
    EMAIL_TEMPLATE_ID, SENDGRID_API_KEY, DEFAULT_FROM_EMAIL,
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
from twilio.rest import Client


class MailService:
    @staticmethod
    def send_email_to_donor(data):
        recepient_email = data.donor.email
        subject = "Donation Request Update"

        body = {}
        body['username'] = data.donor.username
        body['donation_role'] = "Requestor"
        body['related_name'] = data.created_by.username
        body['phone_number'] = data.created_by.phone_number
        body['email'] = data.created_by.email
        body['blood_group'] = data.blood_group
        body['quantity'] = data.quantity
        body['priority'] = data.priority
        body['location'] = data.location

        template_id = EMAIL_TEMPLATE_ID
        sender = DEFAULT_FROM_EMAIL
        data_dict = {"subject": subject, "body": body}
        MailService.send_mail(
            template_id, sender, recepient_email, data_dict)

    @staticmethod
    def send_email_to_requestor(data):
        recepient_email = data.created_by.email
        subject = "Donation Request Update"

        body = {}
        body['username'] = data.created_by.username
        body['donation_role'] = "Donor"
        body['related_name'] = data.donor.username
        body['phone_number'] = data.donor.phone_number
        body['email'] = data.donor.email
        body['blood_group'] = data.blood_group
        body['quantity'] = data.quantity
        body['priority'] = data.priority
        body['location'] = data.location

        template_id = EMAIL_TEMPLATE_ID
        sender = DEFAULT_FROM_EMAIL
        data_dict = {"subject": subject, "body": body}
        MailService.send_mail(
            template_id, sender, recepient_email, data_dict)

    @staticmethod
    def send_mail(template_id, sender, recipient, data_dict):
        sendGridClient = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        mail = Mail()
        mail.template_id = template_id

        mail.from_email = Email(sender)
        personalization = Personalization()
        personalization.add_to(Email(recipient))
        personalization.dynamic_template_data = data_dict
        mail.add_personalization(personalization)

        try:
            sendGridClient.client.mail.send.post(
                request_body=mail.get())
        except exceptions.BadRequestsError as e:
            print(e.body)


class SmsService:
    @staticmethod
    def send_sms_to_requestor(body, toNumber, fromNumber):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=body,
            from_=fromNumber,
            to=toNumber,
        )

    @staticmethod
    def send_sms_to_donor(body, toNumber, fromNumber):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=body,
            from_=fromNumber,
            to=toNumber,
        )
