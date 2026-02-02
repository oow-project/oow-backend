from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app.ai.agent import generate_response
from app.dependencies.auth import get_current_user_or_none
from app.dependencies.rate_limit import check_rate_limit
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import conversation_service

router = APIRouter(prefix="/api/chat", tags=["chat"])

RateLimitDep = Annotated[dict, Depends(check_rate_limit)]
OptionalUserDep = Annotated[dict | None, Depends(get_current_user_or_none)]

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    response: Response,
    rate_limit: RateLimitDep,
    user: OptionalUserDep,
):
    """AI 채팅 응답 생성"""
    response.headers["X-RateLimit-Limit"] = str(rate_limit["limit"])
    response.headers["X-RateLimit-Remaining"] = str(rate_limit["remaining"])
    response.headers["X-RateLimit-Reset"] = str(rate_limit["reset"])

    is_logged_in = user is not None
    has_conversation = request.conversation_id is not None

    chat_message = await generate_response(
        user_input=request.message,
        tag=request.tag,
    )
    if is_logged_in and has_conversation:
        await conversation_service.add_message(
            conversation_id=request.conversation_id,
            role="user",
            content=request.message,
        )

        await conversation_service.add_message(
            conversation_id=request.conversation_id,
            role="assistant",
            content=chat_message,
        )

    return ChatResponse(response=chat_message)
