from uuid import UUID

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """AI 채팅 요청"""
    message: str
    conversation_id: UUID | None = None
    tag: str = "general"


class ChatResponse(BaseModel):
    """AI 채팅 응답"""
    response: str
