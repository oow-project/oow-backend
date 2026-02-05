from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from supabase import create_client
from tavily import TavilyClient

from app.config.settings import settings

supabase = create_client(settings.supabase_url, settings.supabase_key)
tavily = TavilyClient(api_key=settings.tavily_api_key)
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=settings.openai_api_key,
)

ALLOWED_DOMAINS = [
    "liquipedia.net",
    "playoverwatch.com",
    "overwatch.inven.co.kr",
    "namu.wiki",
]


@tool
async def search_rag(query: str) -> str:
    """
    오버워치 전략, 조합, 팁, 경쟁전 시스템, 스타디움, 채널 정보를 검색합니다.
    영웅 운영법, 조합 추천, 티어 정보, 게임 팁 등의 질문에 사용하세요.
    관련 정보를 찾지 못하면 search_web 도구를 사용합니다.
    """

    query_embedding = await embeddings.aembed_query(query)

    result = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_threshold": 0.4,
            "match_count": 5,
        },
    ).execute()

    if not result.data:
        return "관련 정보를 찾지 못했습니다."

    contents = []
    for doc in result.data:
        source = doc.get("metadata", {}).get("title", "알 수 없음")
        contents.append(f"[출처: {source}]\n{doc['content']}")

    return "\n\n---\n\n".join(contents)


@tool
def search_web(query: str) -> str:
    """
    최신 패치노트, 대회 일정, 프로 선수/팀 정보 등 시의성이 중요한 정보를 검색합니다.
    검색 결과를 요약하고 출처 링크를 반드시 포함하세요.
    """
    try:
        result = tavily.search(
            query=f"오버워치 2 {query}",
            include_domains=ALLOWED_DOMAINS,
            max_results=5,
        )

        if not result.get("results"):
            return "검색 결과가 없습니다."

        contents = []
        for item in result["results"]:
            contents.append(
                f"제목: {item['title']}\n"
                f"내용: {item['content']}\n"
                f"출처: {item['url']}"
            )

        return "\n\n---\n\n".join(contents)

    except Exception as e:
        return f"검색 중 오류가 발생했습니다: {e}"


@tool
def get_hero_stats(hero_key: str) -> str:
    """
    특정 영웅의 통계 정보(픽률, 승률 등)를 조회합니다.
    영웅 키는 영어 소문자입니다 (예: ana, genji, reinhardt)
    """
    result = supabase.table("hero_stats").select("*").eq(
        "hero_key", hero_key
    ).order("synced_at", desc=True).limit(1).execute()

    if not result.data:
        return f"{hero_key} 영웅의 통계 정보를 찾지 못했습니다."

    stats = result.data[0]
    return (
        f"영웅: {hero_key}\n"
        f"픽률: {stats.get('pickrate', 'N/A')}%\n"
        f"승률: {stats.get('winrate', 'N/A')}%\n"
    )


@tool
def get_hero_counters(hero_key: str) -> str:
    """
    특정 영웅의 카운터와 시너지 영웅을 조회합니다.
    영웅 키는 영어 소문자입니다 (예: ana, genji, reinhardt)
    """
    result = supabase.table("heroes").select(
        "name, counters, synergies"
    ).eq("key", hero_key).execute()

    if not result.data:
        return f"{hero_key} 영웅 정보를 찾지 못했습니다."

    hero = result.data[0]
    counters = hero.get("counters", [])
    synergies = hero.get("synergies", [])

    return (
        f"영웅: {hero.get('name', hero_key)}\n\n"
        f"카운터 (이 영웅을 상대하기 좋은 영웅):\n"
        f"{', '.join(counters) if counters else '정보 없음'}\n\n"
        f"시너지 (이 영웅과 함께하면 좋은 영웅):\n"
        f"{', '.join(synergies) if synergies else '정보 없음'}"
    )


@tool
def get_hero_abilities(hero_key: str) -> str:
    """
    특정 영웅의 스킬 정보를 조회합니다.
    영웅 키는 영어 소문자입니다 (예: ana, genji, wuyang, freja, vendetta)
    신규 영웅(우양, 프레야, 벤데타)도 조회 가능합니다.
    """
    hero_result = supabase.table("heroes").select(
        "name, role"
    ).eq("key", hero_key).execute()

    if not hero_result.data:
        return f"{hero_key} 영웅 정보를 찾지 못했습니다."

    hero = hero_result.data[0]

    abilities_result = supabase.table("hero_abilities").select(
        "name, description, ability_type"
    ).eq("hero_key", hero_key).execute()

    if not abilities_result.data:
        return f"{hero_key} 영웅의 스킬 정보를 찾지 못했습니다."

    abilities_grouped = {"skill": [], "perk_major": [], "perk_minor": []}
    for ability in abilities_result.data:
        ability_type = ability.get("ability_type", "skill")
        if ability_type in abilities_grouped:
            abilities_grouped[ability_type].append(ability)

    output = f"영웅: {hero.get('name', hero_key)} ({hero.get('role', 'N/A')})\n\n"

    skills = abilities_grouped.get("skill", [])
    if skills:
        output += "## 스킬\n"
        for skill in skills:
            output += f"- **{skill.get('name', 'N/A')}**: {skill.get('description', 'N/A')}\n"
        output += "\n"

    major_perks = abilities_grouped.get("perk_major", [])
    if major_perks:
        output += "## 주요 특전\n"
        for perk in major_perks:
            output += f"- **{perk.get('name', 'N/A')}**: {perk.get('description', 'N/A')}\n"
        output += "\n"

    minor_perks = abilities_grouped.get("perk_minor", [])
    if minor_perks:
        output += "## 보조 특전\n"
        for perk in minor_perks:
            output += f"- **{perk.get('name', 'N/A')}**: {perk.get('description', 'N/A')}\n"

    return output


tools = [search_rag, search_web, get_hero_stats, get_hero_counters, get_hero_abilities]
