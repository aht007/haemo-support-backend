"""
Channels Middleware Class
"""
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
from django.conf import settings
from django.contrib.auth import get_user_model

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode


@database_sync_to_async
def get_user(headers):
    """
    Gets user from token
    """
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
    """
    Middlware class to override default middleware
    """

    def __init__(self, inner):
        """
        Initialize appropriate data
        """
        self.inner = inner

    async def __call__(self, scope, receive, send):
        """
        Attach user to socket request scope
        """
        headers = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        scope['user'] = await get_user(headers)
        return await self.inner(scope, receive, send)


def TokenAuthMiddlewareStack(inner):
    """
    Add our middleware to middlwares stack
    """
    return TokenAuthMiddleware(
        AuthMiddlewareStack(inner)
    )
