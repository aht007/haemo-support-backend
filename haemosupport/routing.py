"""
Routing File for ASGI
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from donation.consumers import DonationRequestsConsumer, NotificationConsumer

from haemosupport.channelsmiddleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter(
            [
                url("ws/donations/", DonationRequestsConsumer.as_asgi()),
                url("ws/notification-service/", NotificationConsumer.as_asgi())
            ]
        )
    )
})
