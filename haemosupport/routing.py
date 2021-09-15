"""
Routing File for ASGI
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from donation.consumers import DonationRequestsConsumer

from haemosupport.channelsmiddleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter(
            [
                url("", DonationRequestsConsumer.as_asgi())
            ]
        )
    )
})
