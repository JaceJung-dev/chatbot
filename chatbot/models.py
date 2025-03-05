from django.db import models

from chatroom.models import ChatRoom, TimeStampModel


class BotResponse(TimeStampModel):
    chatroom = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="bot_response"
    )
    user_message = models.TextField()
    bot_message = models.TextField()

    def __str__(self):
        return f"{self.chatroom.id}의 대화기록"
