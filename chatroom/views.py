from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chatbot.views import ChatBotAPIView

from .models import ChatMessage, ChatRoom
from .serializers import ChatRoomSerializer


def chat_view(request):
    return render(request, "chatroom/chat.html")


class ChatRoomListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        chatrooms = ChatRoom.objects.filter(user=request.user)
        serializer = ChatRoomSerializer(chatrooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatMessageAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, chatroom_id):

        user_message = request.data.get("message")
        if not user_message:
            return Response(
                {"error": "질문을 입력해주세요!"}, status=status.HTTP_400_BAD_REQUEST
            )

        chatroom = get_object_or_404(ChatRoom, pk=chatroom_id)

        user_chat = ChatMessage.objects.create(
            chatroom=chatroom, user_or_bot=True, messages=user_message
        )

        chatbot_api = ChatBotAPIView()
        bot_response = chatbot_api.post(request, chatroom_id).data

        bot_chat = ChatMessage.objects.create(
            chatroom=chatroom, user_or_bot=False, messages=bot_response["bot_message"]
        )

        return Response(
            {"user_message": user_chat.messages, "bot_message": bot_chat.messages},
            status=status.HTTP_201_CREATED,
        )
