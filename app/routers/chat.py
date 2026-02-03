import json
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.ai.agent import generate_response_stream
from app.dependencies.auth import get_current_user_or_none
from app.dependencies.rate_limit import check_rate_limit
from app.schemas.chat import ChatRequest
from app.services import conversation_service

router = APIRouter(prefix="/api/chat", tags=["chat"])

RateLimitDep = Annotated[dict, Depends(check_rate_limit)]
OptionalUserDep = Annotated[dict | None, Depends(get_current_user_or_none)]


@router.post("")
async def chat(
    request: ChatRequest,
    rate_limit: RateLimitDep,
    user: OptionalUserDep,
):
    """AI 채팅 응답 생성 (스트리밍)"""

    is_logged_in = user is not None
    has_conversation = request.conversation_id is not None

    async def event_generator():
        full_response = ""

        async for chunk in generate_response_stream(
            user_input=request.message,
            tag=request.tag,
            chat_history=request.chat_history
        ):
            yield chunk

            if '"type": "content"' in chunk:
                data = json.loads(chunk.replace("data: ", "").strip())
                full_response += data["content"]

        if is_logged_in and has_conversation:
            await conversation_service.add_message(
                conversation_id=request.conversation_id,
                role="user",
                content=request.message,
            )
            await conversation_service.add_message(
                conversation_id=request.conversation_id,
                role="assistant",
                content=full_response,
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-RateLimit-Limit": str(rate_limit["limit"]),
            "X-RateLimit-Remaining": str(rate_limit["remaining"]),
            "X-RateLimit-Reset": str(rate_limit["reset"]),
        },
    )
