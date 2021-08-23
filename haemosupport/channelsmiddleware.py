from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model


@database_sync_to_async
def get_user(headers):
    try:
        UntypedToken(headers)
    except (InvalidToken, TokenError) as e:
        # Token is invalid
        print(e)
        return AnonymousUser
    else:
        #  Then token is valid, decode it
        decoded_data = jwt_decode(
            headers, settings.SECRET_KEY, algorithms=["HS256"])
        # Get the user using ID
        user = get_user_model().objects.get(id=decoded_data["user_id"])
        return user


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        scope['user'] = await get_user(headers)
        return await self.inner(scope, receive, send)


class TokenAuthMiddlewareInstance:

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        headers = dict(self.scope['headers'])
        if b'authorization' in headers:
            self.scope['user'] = await get_user(headers)
        inner = self.inner(self.scope)
        return await inner(receive, send)


def TokenAuthMiddlewareStack(inner): return TokenAuthMiddleware(
    AuthMiddlewareStack(inner))
