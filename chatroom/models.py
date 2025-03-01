from django.db import models
from django.conf import settings


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ChatRoom(TimeStampModel):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chatrooms"
    )
    title = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.user.username}의 '{self.title}' 세션"


class ChatMessage(TimeStampModel):
    chatroom = models.ForeignKey(
        to=ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    user_or_bot = models.BooleanField()
    messages = models.TextField()

    def __str__(self):
        return
