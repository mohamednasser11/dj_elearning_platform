"""
ASGI config for e_learning_platform project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.urls import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_learning_platform.settings")


def get_websocket_application():
    from middleware.websocket_auth_middleware import WebSocketJWTAuthMiddleware

    return WebSocketJWTAuthMiddleware(URLRouter(websocket_urlpatterns))


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": get_websocket_application(),
    }
)
