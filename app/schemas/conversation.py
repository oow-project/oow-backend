from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ConversationCreate(BaseModel):
    """채팅방 생성 요청"""
    title: str
    tag: str = "general"


class ConversationResponse(BaseModel):
    """채팅방 응답"""
    id: UUID
    title: str
    tag: str
    created_at: datetime
    updated_at: datetime


class ConversationListResponse(BaseModel):
    """채팅방 목록 응답"""
    conversations: list[ConversationResponse]
    total: int


class MessageResponse(BaseModel):
    """메시지 응답"""
    id: UUID
    role: str
    content: str
    created_at: datetime


class MessagesResponse(BaseModel):
    """메시지 목록 응답"""
    messages: list[MessageResponse]
    total: int
