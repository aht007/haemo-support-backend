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
        self.user = self.scope["user"]
        self.room_group_name = 'donations' + str(self.user.id)

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

    # def receive(self, text_data):
    #     """
    #     Receive a message and broadcast it to a room group
    #     """

    #     text_data_json = json.loads(text_data)
    #     request = text_data_json['request']
    #     donationReq = DonationRequest.objects.create(**request)

    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'donation_request',
    #             'request': json.dumps(donationReq.as_dict(), default=self.myDateConvertor)
    #         }
    #     )

    @staticmethod
    @receiver(signals.post_save, sender=DonationRequest)
    def donation_request_observer(sender, instance, created, **kwrags):
        if(created):
            data = DonationSerializer(instance).data
            layer = channels.layers.get_channel_layer()
            async_to_sync(layer.group_send)(
            'donations'+ str(instance.created_by.id),
                {
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
