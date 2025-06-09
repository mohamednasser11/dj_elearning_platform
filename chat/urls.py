from django.urls import path

from chat.views import ChatView
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/", ChatConsumer.as_asgi()),
]

urlpatterns = [
    path("<int:courseId>/", ChatView.as_view(), name="get-chats-for-course"),
]
