from uuid import UUID

from pydantic import BaseModel


class ChatMessage(BaseModel):
    """채팅 메시지"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """AI 채팅 요청"""
    message: str
    conversation_id: UUID | None = None
    tag: str = "general"
    chat_history: list[ChatMessage] | None = None
