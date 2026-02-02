from uuid import UUID

from app.config.supabase import get_supabase
from app.exceptions import NotFoundError

MAX_CONVERSATIONS = 30


async def create_conversation(
    user_id: UUID,
    title: str,
    tag: str = "general",
) -> dict:
    """새 채팅방을 생성한다."""
    supabase = get_supabase()

    response = await supabase.table("conversations").insert({
        "user_id": str(user_id),
        "title": title,
        "tag": tag,
    }).execute()

    return response.data[0]


async def get_conversations(user_id: UUID) -> list[dict]:
    """사용자의 채팅방 목록을 조회한다. (최신순, 최대 30개)"""
    supabase = get_supabase()

    response = await (
        supabase.table("conversations")
        .select("id, title, tag, created_at, updated_at")
        .eq("user_id", str(user_id))
        .order("updated_at", desc=True)
        .limit(MAX_CONVERSATIONS)
        .execute()
    )

    return response.data


async def get_conversation_messages(
    user_id: UUID,
    conversation_id: UUID,
) -> list[dict]:
    """채팅방의 메시지를 조회한다."""
    supabase = get_supabase()

    conv_response = await (
        supabase.table("conversations")
        .select("id")
        .eq("id", str(conversation_id))
        .eq("user_id", str(user_id))
        .execute()
    )

    if not conv_response.data:
        raise NotFoundError("채팅방을 찾을 수 없습니다")

    msg_response = await (
        supabase.table("chat_messages")
        .select("id, role, content, created_at")
        .eq("conversation_id", str(conversation_id))
        .order("created_at", desc=False)
        .execute()
    )

    return msg_response.data


async def delete_conversation(user_id: UUID, conversation_id: UUID) -> bool:
    """채팅방을 삭제한다."""
    supabase = get_supabase()

    response = await (
        supabase.table("conversations")
        .delete()
        .eq("id", str(conversation_id))
        .eq("user_id", str(user_id))
        .execute()
    )

    if not response.data:
        raise NotFoundError("채팅방을 찾을 수 없습니다")

    return True


async def add_message(
    conversation_id: UUID,
    role: str,
    content: str,
) -> dict:
    """채팅방에 메시지를 추가한다."""
    supabase = get_supabase()

    response = await supabase.table("chat_messages").insert({
        "conversation_id": str(conversation_id),
        "role": role,
        "content": content,
    }).execute()

    return response.data[0]
