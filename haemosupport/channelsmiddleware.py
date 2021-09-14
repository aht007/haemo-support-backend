"""
Middleware for attaching user to socket request through token
"""
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from jwt import decode as jwt_decode

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(headers):
    """
    Extract user from token
    """
    try:
        UntypedToken(headers)
    except (InvalidToken, TokenError) as err:
        # Token is invalid
        print(err)
        return AnonymousUser
    else:
        #  Then token is valid, decode it
        decoded_data = jwt_decode(
            headers, settings.SECRET_KEY, algorithms=["HS256"])
        # Get the user using ID
        user = get_user_model().objects.get(id=decoded_data["user_id"])
        return user


class TokenAuthMiddleware(BaseMiddleware):
    """
    Middleware Class
    """

    def __init__(self, inner):
        """
        Initialize Instance properly
        """
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        """
        Get token and attach user to request
        """
        try:
            token_key = (dict((x.split('=') for x in scope['query_string']
                               .decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = get_user(token_key)
        return await super().__call__(scope, receive, send)
