from django.urls import path
from . import views

app_name = "chatroom"
urlpatterns = [
    path("", views.ChatRoomListAPIView.as_view(), name="chat-room"),
    path(
        "<int:chatroom_id>/messages/",
        views.ChatMessageAPIView.as_view(),
        name="chat-message",
    ),
    path("chat/", views.chat_view, name="chat"),
]
