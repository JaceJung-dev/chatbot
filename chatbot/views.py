from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from chatroom.models import ChatRoom
from .models import BotResponse
from .serializers import BotResponseSerializer
from .utils import ChatBotService
from rest_framework.permissions import IsAuthenticated, AllowAny


class ChatBotAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chatroom_id):
        user_message = request.data.get("message")
        if not user_message:
            return Response(
                {"error": "message 필드가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        chatroom = get_object_or_404(ChatRoom, id=chatroom_id)

        # 챗봇 응답 생성
        chatbot_service = ChatBotService()
        bot_response_text = chatbot_service.get_recommendation(user_message)

        # 응답을 DB에 저장
        bot_response = BotResponse.objects.create(
            chatroom=chatroom, user_message=user_message, bot_message=bot_response_text
        )

        serializer = BotResponseSerializer(bot_response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
