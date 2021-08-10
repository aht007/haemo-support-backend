from donation.models import DonationRequest
import json
import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


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

    def receive(self, text_data):
        """
        Receive a message and broadcast it to a room group
        """

        text_data_json = json.loads(text_data)
        request = text_data_json['request']
        donationReq = DonationRequest.objects.create(**request)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'donation_request',
                'request': json.dumps(donationReq.as_dict(), default=self.myDateConvertor)
            }
        )

    def donation_request(self, event):
        """
        Receive a broadcast message and send it over a websocket
        """

        request = event['request']
        # Send message to WebSocket
        self.send(request)
