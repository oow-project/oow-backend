from typing import Annotated

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel

from app.ai.agent import generate_response
from app.dependencies.rate_limit import check_rate_limit

router = APIRouter(prefix="/api/chat", tags=["chat"])

RateLimitDep = Annotated[dict, Depends(check_rate_limit)]


class ChatRequest(BaseModel):
    message: str
    context: dict | None = None


class ChatResponse(BaseModel):
    response: str


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    response: Response,
    rate_limit: RateLimitDep,
):
    """AI 채팅 응답 생성"""
    response.headers["X-RateLimit-Limit"] = str(rate_limit["limit"])
    response.headers["X-RateLimit-Remaining"] = str(rate_limit["remaining"])
    response.headers["X-RateLimit-Reset"] = str(rate_limit["reset"])

    chat_message = await generate_response(
        user_input=request.message,
        context=request.context,
    )
    return ChatResponse(response=chat_message)
