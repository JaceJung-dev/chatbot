from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chatroom/<int:chatroom_id>/", ChatConsumer.as_asgi()),
]
