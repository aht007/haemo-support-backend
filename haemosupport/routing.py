from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from channels.security.websocket import AllowedHostsOriginValidator
from donation.consumers import DonationRequestsConsumer


application = ProtocolTypeRouter({
  'websocket': AllowedHostsOriginValidator(
    URLRouter(
      [
        url("", DonationRequestsConsumer.as_asgi())
      ]
    )
  )
})