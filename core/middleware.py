import os
import django
django.setup()  # ⚠️ Django iloji boricha erta yuklansin

from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from jwt import decode as jwt_decode
from django.conf import settings

User = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        token = parse_qs(query_string).get("token", [None])[0]
        scope["user"] = AnonymousUser()

        if token:
            try:
                UntypedToken(token)
                payload = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get("user_id")

                # Debug
                print("✅ JWT:", token)
                print("👤 Payload:", payload)

                scope["user"] = await get_user(user_id)
                print("👤 User loaded:", scope["user"])

            except Exception as e:
                print("❌ JWT Error:", e)

        return await self.inner(scope, receive, send) 

class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.scope = dict(scope)
        self.middleware = middleware

    async def __call__(self, receive, send):
        qs = self.scope.get("query_string", b"").decode()
        token = parse_qs(qs).get("token", [None])[0]
        self.scope["user"] = AnonymousUser()
        if token:
            try:
                UntypedToken(token)
                payload = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get("user_id")
                self.scope["user"] = await get_user(user_id)
            except Exception as e:
                print("TokenAuthMiddleware error:", e)
        return await self.inner(self.scope)(receive, send)
