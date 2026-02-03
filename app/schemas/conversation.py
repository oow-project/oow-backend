from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreate(BaseModel):
    """채팅방 생성 요청"""
    title: str
    tag: str = "general"


class ConversationResponse(BaseModel):
    """채팅방 응답"""
    model_config = ConfigDict(populate_by_name=True)

    id: UUID
    title: str
    tag: str
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")


class ConversationListResponse(BaseModel):
    """채팅방 목록 응답"""
    conversations: list[ConversationResponse]
    total: int


class MessageResponse(BaseModel):
    """메시지 응답"""
    model_config = ConfigDict(populate_by_name=True)

    id: UUID
    role: str
    content: str
    created_at: datetime = Field(serialization_alias="createdAt")


class MessagesResponse(BaseModel):
    """메시지 목록 응답"""
    messages: list[MessageResponse]
    total: int


class MigrateMessage(BaseModel):
    """마이그레이션용 메시지"""
    role: str
    content: str


class MigrateRequest(BaseModel):
    """비회원 대화 마이그레이션 요청"""
    messages: list[MigrateMessage]
    tag: str = "general"
