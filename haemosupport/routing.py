from haemosupport.channelsmiddleware import TokenAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from donation.consumers import DonationRequestsConsumer



application = ProtocolTypeRouter({
  'websocket': TokenAuthMiddleware(
    URLRouter(
      [
        url("", DonationRequestsConsumer.as_asgi())
      ]
    )
  )
})
