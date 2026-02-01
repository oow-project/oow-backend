from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.agent import generate_response

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    context: dict | None = None


class ChatResponse(BaseModel):
    response: str


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """AI 채팅 응답 생성"""
    response = await generate_response(
        user_input=request.message,
        context=request.context,
    )
    return ChatResponse(response=response)
