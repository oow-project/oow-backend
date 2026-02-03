import json
from collections.abc import AsyncGenerator

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from app.ai.prompts import SYSTEM_PROMPT, TITLE_GENERATION_PROMPT
from app.ai.tools import tools
from app.config.settings import settings

_llm: ChatOpenAI | None = None


def get_llm() -> ChatOpenAI:
    """
    ChatOpenAI 인스턴스를 반환

    최초 호출 시 인스턴스를 생성하고, 이후에는 동일한 인스턴스를 재사용
    """
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=settings.openai_temperature,
            openai_api_key=settings.openai_api_key,
        )
    return _llm


def get_agent_executor() -> AgentExecutor:
    """에이전트 실행기 생성"""
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )

    return executor


def convert_to_langchain_messages(history: list | None) -> list:
    """채팅 기록을 LangChain 메시지 형식으로 변환"""
    if not history:
        return []

    messages = []
    for msg in history:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        else:
            messages.append(AIMessage(content=msg.content))
    return messages


async def generate_response_stream(
    user_input: str,
    tag: str = "general",
    chat_history: list | None = None,
) -> AsyncGenerator[str, None]:
    """
    사용자 입력에 대한 AI 응답을 스트리밍으로 생성

    Args:
        user_input: 사용자 질문
        tag: 대화 태그 (영웅 이름 or "general")
        chat_history: 이전 대화 기록

    Yields:
        SSE 형식의 데이터 청크
    """
    executor = get_agent_executor()

    enhanced_input = user_input
    if tag != "general":
        enhanced_input = f"[현재 {tag} 영웅 관련] {user_input}"

    langchain_history = convert_to_langchain_messages(chat_history)

    async for event in executor.astream_events(
        {"input": enhanced_input, "chat_history": langchain_history},
        version="v2",
    ):
        kind = event["event"]

        if kind == "on_tool_start":
            tool_name = event["name"]
            status_data = {"type": "status", "content": f"{tool_name} 실행 중..."}
            yield f"data: {json.dumps(status_data, ensure_ascii=False)}\n\n"

        chunk = event.get("data", {}).get("chunk")

        is_valid_content = (
            kind == "on_chat_model_stream"
            and chunk
            and hasattr(chunk, "content")
            and chunk.content
        )

        if is_valid_content:
            content_data = {"type": "content", "content": chunk.content}
            yield f"data: {json.dumps(content_data, ensure_ascii=False)}\n\n"

    yield f"data: {json.dumps({'type': 'done'})}\n\n"


async def generate_title(user_message: str, ai_response: str) -> str:
    """사용자 메시지와 AI 응답을 기반으로 대화 제목 생성"""

    cheap_llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=50,
        openai_api_key=settings.openai_api_key,
    )

    prompt = TITLE_GENERATION_PROMPT.format(
        user_message=user_message,
        ai_response=ai_response[:200],
    )

    response = await cheap_llm.ainvoke(prompt)

    return response.content.strip()[:20]
