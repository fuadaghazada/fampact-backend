from urllib.parse import parse_qs

from django.db import close_old_connections
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

from channels.auth import AuthMiddleware
from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware, SessionMiddleware

User = get_user_model()


@database_sync_to_async
def get_user_from_scope(scope):
    """
        Accessing the user from token coming from
        websocket connection in url query parameter
    """
    close_old_connections()

    # Getting the queryset from connect url & extracting the token
    query_string = parse_qs(scope['query_string'].decode())
    token = query_string.get('token')
    if not token or not len(token):
        return AnonymousUser()
    token = token[0]

    # Extracting the user from the token
    try:
        token_instance = Token.objects.get(key=token)
        return token_instance.user

    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(AuthMiddleware):

    async def resolve_scope(self, scope):
        scope['user']._wrapped = await get_user_from_scope(scope)


def TokenAuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(TokenAuthMiddleware(inner)))
