from donation.serializers import DonationSerializer
from donation.models import DonationRequest
import json
import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import signals
from django.dispatch import receiver
import channels.layers


class DonationRequestsConsumer(WebsocketConsumer):
    def connect(self):

        self.room_group_name = 'donations'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def myDateConvertor(self, d):
        if isinstance(d, datetime.datetime):
            return d.__str__()

    @staticmethod
    @receiver(signals.post_save, sender=DonationRequest)
    def donation_request_observer(sender, instance, created, **kwrags):
        data = DonationSerializer(instance).data
        print(data)
        if(instance.is_approved):
            layer = channels.layers.get_channel_layer()
            async_to_sync(layer.group_send)('donations', {
                                            'type': 'donation_request',
                                            'request': json.dumps(data)
                                            }
                                            )

    def donation_request(self, event):
        """
        Receive a broadcast message and send it over a websocket
        """

        request = event['request']
        # Send message to WebSocket
        self.send(request)
