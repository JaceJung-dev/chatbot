from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class ChatBotService:

    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, streaming=True)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    """
                    당신은 전문적인 도서 추천 AI입니다.
                    사용자의 질문을 기반으로 적절한 도서 2권을 추천하세요.
                    
                    반드시 다음 정보를 포함하세요:
                    - 책 제목
                    - 저자
                    - 출판사
                    - 출판일자
                    - 추천 이유
                    """
                ),
                HumanMessagePromptTemplate.from_template(
                    "사용자의 질문: {user_question}"
                ),
            ]
        )

    async def get_recommendation(self, user_question):
        chain = self.prompt | self.model
        async for chunk in chain.astream({"user_question": user_question}):
            yield chunk.content
