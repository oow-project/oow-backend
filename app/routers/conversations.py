from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.schemas.conversation import (
    ConversationCreate,
    ConversationListResponse,
    ConversationResponse,
    MessagesResponse,
)
from app.services import conversation_service

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

UserDep = Annotated[dict, Depends(get_current_user)]


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    request: ConversationCreate,
    user: UserDep,
):
    """새 채팅방을 생성한다."""
    conversation = await conversation_service.create_conversation(
        user_id=user["id"],
        title=request.title,
        tag=request.tag,
    )
    return conversation


@router.get("", response_model=ConversationListResponse)
async def get_conversations(user: UserDep):
    """채팅방 목록을 조회한다."""
    conversations = await conversation_service.get_conversations(user["id"])
    return {
        "conversations": conversations,
        "total": len(conversations),
    }


@router.get("/{conversation_id}/messages", response_model=MessagesResponse)
async def get_messages(
    conversation_id: UUID,
    user: UserDep,
):
    """채팅방의 메시지를 조회한다."""
    messages = await conversation_service.get_conversation_messages(
        user_id=user["id"],
        conversation_id=conversation_id,
    )
    return {
        "messages": messages,
        "total": len(messages),
    }


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: UUID,
    user: UserDep,
):
    """채팅방을 삭제한다."""
    await conversation_service.delete_conversation(
        user_id=user["id"],
        conversation_id=conversation_id,
    )
