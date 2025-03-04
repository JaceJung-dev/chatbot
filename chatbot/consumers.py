import json  # 웹소켓에서 데이터를 JSON으로 주고 받기 위해 사용

import markdown  # markdown 형식을 HTML로 변환
from asgiref.sync import sync_to_async  # ORM을 비동기 방식으로 호출하기 위해 사용
from channels.generic.websocket import \
    AsyncWebsocketConsumer  # 비동기 처리를 위한 기본 클래스

from chatroom.models import ChatMessage, ChatRoom

from .utils import ChatBotService


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """클라이언트가 WebSocket에 연결되었을 때 실행"""

        self.chatroom_id = self.scope["url_route"]["kwargs"]["chatroom_id"]
        # 채팅방 그룹 이름 설정
        self.room_group_name = f"chatroom_{self.chatroom_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """클라이언트가 WebSocket 연결을 종료했을 때 실행"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """클라이언트로부터 메시지를 받았을 때 실행"""
        # JSON으로 받은 웹소켓 메시지를 Python 딕셔너리로 변환
        data = json.loads(text_data)
        user_message = data.get("message")

        if not user_message:
            await self.send(text_data=json.dumps({"error": "메시지가 비어 있습니다."}))
            return

        # print(f"메세지 수신 확인 >>>> {user_message}")

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

            bot_response_html = markdown.markdown(bot_response_text)

            await self.send(
                text_data=json.dumps(
                    {
                        "user_message": user_message,
                        "bot_message": bot_response_html,
                        "is_streaming": True,
                    }
                )
            )

        # 데이터베이스에 챗봇 응답 저장
        await sync_to_async(ChatMessage.objects.create)(
            chatroom=chatroom, user_or_bot=False, messages=bot_response_text
        )

        final_bot_response_html = markdown.markdown(bot_response_text)

        # 최종 챗봇 응답을 클라이언트에 전송
        await self.send(
            text_data=json.dumps(
                {
                    "user_message": user_message,
                    "bot_message": final_bot_response_html,
                    "is_streaming": False,
                },
                ensure_ascii=False,
            )
        )
