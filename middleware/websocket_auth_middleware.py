import json
from urllib.parse import parse_qs
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from channels.db import database_sync_to_async


class WebSocketJWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        async def error(message):
            await send({"type": "websocket.accept"})
            await send(
                {
                    "type": "websocket.send",
                    "text": json.dumps(
                        {
                            "type": "error",
                            "data": {"message": message},
                        }
                    ),
                }
            )
            await send({"type": "websocket.close", "code": 4000})

        token = self.get_token_from_scope(scope)

        if not token:
            await error("Authorization token required")
            return

        try:
            scope["user"] = await self.get_user_from_token(token)
        except AuthenticationFailed:
            await error("Invalid token")
            return

        return await self.inner(scope, receive, send)

    def get_token_from_scope(self, scope):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        if "token" in query_params:
            return query_params["token"][0]

        headers = dict(scope.get("headers", {}))
        if b"authorization" in headers:
            auth_header = headers[b"authorization"].decode()
            if auth_header.startswith("Bearer "):
                return auth_header.split(" ")[1]
        return None

    @database_sync_to_async
    def get_user_from_token(self, token):
        authenticator = JWTAuthentication()
        validated_token = authenticator.get_validated_token(token)
        return authenticator.get_user(validated_token)
