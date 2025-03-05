from django.urls import path

from . import views

app_name = "chatbot"
urlpatterns = [
    path("<int:chatroom_id>/", views.ChatBotAPIView.as_view(), name="chatbot"),
]
