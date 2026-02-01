from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from app.ai.prompts import SYSTEM_PROMPT
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


async def generate_response(
    user_input: str,
    context: dict | None = None,
    chat_history: list | None = None,
) -> str:
    """
    사용자 입력에 대한 AI 응답 생성

    Args:
        user_input: 사용자 질문
        context: 현재 페이지 컨텍스트 (예: {"page": "hero_detail", "heroKey": "ana"})
        chat_history: 이전 대화 기록

    Returns:
        AI 응답 텍스트
    """
    executor = get_agent_executor()

    enhanced_input = user_input

    if context and context.get("heroKey"):
        enhanced_input = f"[현재 {context['heroKey']} 영웅 페이지] {user_input}"

    result = await executor.ainvoke({
        "input": enhanced_input,
        "chat_history": chat_history or [],
    })

    return result["output"]
