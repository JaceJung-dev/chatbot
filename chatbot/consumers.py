import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import ChatBotService
from chatroom.models import ChatRoom, ChatMessage
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """클라이언트가 WebSocket에 연결되었을 때 실행"""
        self.chatroom_id = self.scope["url_route"]["kwargs"]["chatroom_id"]
        self.room_group_name = f"chatroom_{self.chatroom_id}"

        # WebSocket 그룹에 추가
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """클라이언트가 WebSocket 연결을 종료했을 때 실행"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """클라이언트로부터 메시지를 받았을 때 실행"""
        data = json.loads(text_data)
        user_message = data.get("message")

        if not user_message:
            await self.send(text_data=json.dumps({"error": "메시지가 비어 있습니다."}))
            return

        # 데이터베이스에 사용자 메시지 저장
        chatroom = await sync_to_async(ChatRoom.objects.get)(id=self.chatroom_id)
        await sync_to_async(ChatMessage.objects.create)(
            chatroom=chatroom, user_or_bot=True, messages=user_message
        )

        # "⌛ 답변을 생성 중입니다..." 메시지를 클라이언트에게 먼저 전송
        await self.send(
            text_data=json.dumps(
                {
                    "user_message": user_message,
                    "bot_message": "⌛ 답변을 생성 중입니다...",
                }
            )
        )

        # 챗봇 응답 스트리밍 출력
        chatbot_service = ChatBotService()
        bot_response_text = ""

        async for chunk in chatbot_service.get_recommendation(user_message):
            bot_response_text += chunk
            await self.send(
                text_data=json.dumps(
                    {
                        "user_message": user_message,
                        "bot_message": bot_response_text,
                        "is_streaming": True,
                    }
                )
            )

        # 데이터베이스에 챗봇 응답 저장
        await sync_to_async(ChatMessage.objects.create)(
            chatroom=chatroom, user_or_bot=False, messages=bot_response_text
        )

        # 최종 챗봇 응답을 클라이언트에 전송
        await self.send(
            text_data=json.dumps(
                {
                    "user_message": user_message,
                    "bot_message": bot_response_text,
                    "is_streaming": False,
                }
            )
        )
