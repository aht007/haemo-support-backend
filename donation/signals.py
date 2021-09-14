"""
Signals for Donation App
"""
import json
import requests
from django.db.models import signals
from django.dispatch import receiver

from asgiref.sync import async_to_sync
import channels.layers

from donation.services import MailService, SmsService
from donation.serializers import DonationUserSerializer
from donation.models import DonationRequest, Status


@receiver(signals.post_save, sender=DonationRequest)
def donation_request_observer(sender, instance, created, **kwargs):
    """
    Pushes New donation requests to frontend
    """
    data = DonationUserSerializer(instance).data
    layer = channels.layers.get_channel_layer()
    if(instance.status == Status.PENDING):
        async_to_sync(layer.group_send)('admin_donations', {
            'type': 'donation_request',
            'request': json.dumps(data)
        }
        )
    else:
        async_to_sync(layer.group_send)('user_donations', {
            'type': 'donation_request',
            'request': json.dumps(data)
        }
        )


@receiver(signals.post_save, sender=DonationRequest)
def donation_request_approve_observer(sender, instance, created, **kwargs):
    """
    This method will send an email and sms to both donor and requestor
    when a donation request becomes in progress
    """
    if created is False:
        if instance.status == Status.IN_PROGRESS:
            try:

                MailService.send_email_to_donor(
                    instance)

                MailService.send_email_to_requestor(
                    instance)
                body = format_donor_data_for_message(instance)
                SmsService.send_sms(
                    body, instance.donor.phone_number, +12248084101)
                body = format_requestor_data_for_message(instance)
                SmsService.send_sms(
                    body, instance.created_by.phone_number, +12248084101)

            except requests.HTTPError as exception:
                print(exception)


def format_requestor_data_for_message(instance):
    """
    Formats Requestor data in a format to send through sms
    """
    body = ("Donor {donor_name} having Phone Number{phone_number} has"
            " accepted your request and will be"
            " in contact with you soon".format(
                donor_name=instance.donor.username,
                phone_number=instance.donor.phone_number))
    return body


def format_donor_data_for_message(instance):
    """
    Formats Donor data in a format to send through sms
    """
    body = ("Requestor {requestor_name} having Phone Number{phone_number}"
            " awaits a call from you".format(
                requestor_name=instance.created_by.username,
                phone_number=instance.created_by.phone_number))

    return body
