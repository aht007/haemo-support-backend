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

    def donation_request(self, event):
        """
        Receive a broadcast message and send it over a websocket
        """

        request = event['request']
        # Send message to WebSocket
        self.send(request)
