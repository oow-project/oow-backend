from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ChatMessage(BaseModel):
    """채팅 메시지"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """AI 채팅 요청"""
    model_config = ConfigDict(populate_by_name=True)

    message: str
    conversation_id: UUID | None = Field(default=None, alias="conversationId")
    tag: str = "general"
    chat_history: list[ChatMessage] | None = Field(default=None, alias="chatHistory")


class ChatMetaEvent(BaseModel):
    """채팅 메타 이벤트"""
    model_config = ConfigDict(populate_by_name=True)

    type: str = "meta"
    conversation_id: str = Field(serialization_alias="conversationId")
