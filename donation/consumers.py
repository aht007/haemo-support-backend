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


    def receive(self, text_data):
        """
        Receive a message and broadcast it to a room group
        """
        
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        utc_time = datetime.datetime.now(datetime.timezone.utc)
        utc_time = utc_time.isoformat()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'donation_request',
                'message': message,
                'utc_time': utc_time,
            }
        )

    def donation_request(self, event):
        """
        Receive a broadcast message and send it over a websocket
        """
        
        message = event['message']
        utc_time = event['utc_time']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'utc_time': utc_time,
        }))