"""
Consumer for Donation App
"""
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class DonationRequestsConsumer(WebsocketConsumer):
    """
    Donation Requests Consumer for communication
    through web sockets
    """

    def connect(self):
        """
        Connect method for web socket
        """

        user = self.scope['user']
        if user.is_anonymous:
            self.close()
        else:
            if user.is_admin:
                self.room_group_name = 'admin_donations'
                # Join room group
                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
                )
                self.accept()
            else:
                self.room_group_name = 'user_donations'
                # Join room group
                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
                )

                self.accept()

    def disconnect(self, close_code):
        """
        Dicconnect method for web socket
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def donation_request(self, event):
        """
        Receive a broadcast message and send it over a websocket
        """

        request = event['request']
        # Send message to WebSocket
        self.send(request)


class NotificationConsumer(WebsocketConsumer):
    """
    Notification Consumer for communication
    through web sockets
    """

    def connect(self):
        """
        Connect method for web socket
        """

        user = self.scope['user']
        if user.is_anonymous:
            self.close()
        else:
            self.room_group_name = f"notification-{user.username}"
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()

    def disconnect(self, close_code):
        """
        Dicconnect method for web socket
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def notification(self, event):
        """
        notification structure for sending notification over web socket
        """
        request = event['request']
        self.send(request)
