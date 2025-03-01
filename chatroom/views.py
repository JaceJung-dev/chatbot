from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer


class ChatRoomListAPIView(APIView):
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
