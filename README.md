
# oow.gg

<div align="center">
  <p>
    <b>오버워치 인게임 승률과 픽률을 제공하고 </b><br/>
    <b>AI 챗봇에게 질문하여 필요한 정보를 바로 얻을 수 있는 서비스입니다.</b>
    <br/>
    <br/>
    <a href="https://github.com/oow-project/oow-frontend" rel="noopener noreferrer" target="_blank">프론트엔드</a> | <a href="https://github.com/oow-project/oow-backend" rel="noopener noreferrer" target="_blank">백엔드</a>
  </p>
  <a href="https://www.oowgg.com/" rel="noopener noreferrer" target="_blank">
    <img width="1280" height="640" alt="OOW GG main" src="https://github.com/user-attachments/assets/aa4fb97b-2055-4195-aa35-7d822b5a4a87" />
  </a>
</div>

<br/>
<br/>

# 목차

- [프로젝트 기획 동기](#프로젝트-기획-동기)
- [미리보기](#미리보기)
  - [메인 페이지 (영웅 통계)](#메인-페이지-영웅-통계)
  - [영웅 정보 페이지](#영웅-정보-페이지)
  - [영웅 상세 페이지](#영웅-정보-페이지)
  - [AI 코치 (챗봇)](#ai-코치-챗봇)
- [기술 스택](#기술-스택)
- [개발 과정](#개발-과정)
  - [오버워치 데이터 확보 전략](#오버워치-데이터-확보-전략)
  - [AI 챗봇 구현](#ai-챗봇-구현)
    - [LLM은 오버워치를 얼마나 알고 있을까 ?](#llm은-오버워치를-얼마나-알고-있을까-)
    - [해결 방안: Tool Calling 기반 설계](#해결-방안-tool-calling-기반-설계)
    - [RAG: 오버워치 공략 문서 기반 답변 보강](#rag-오버워치-공략-문서-기반-답변-보강)
    - [Tavily API: 최신 정보 실시간 검색](#tavily-api-최신-정보-실시간-검색)
      - [웹 검색](#웹-검색)
      - [패치노트 조회](#패치노트-조회) 
    - [DB 조회:영웅 정보 직접 조회](#db-조회-영웅-정보-직접-조회)
    - [스트리밍 응답 화면](#스트리밍-응답-화면)
  - [응답을 사용자에게 전달하기까지](#응답을-사용자에게-전달하기까지)
    - [스트리밍 응답을 화면에 그리기](#스트리밍-응답을-화면에-그리기)
    - [상태를 나눈 기준](#상태를-나눈-기준)
    - [비회원에서 회원으로 대화를 이어가기](#비회원에서-회원으로-대화-이어가기)
      - [비회원 대화를 어디에 저장할까](#비회원-대화를-어디에-저장할까-)
      - [로그인 시 보관된 대화를 서버로 어떻게 이관할 것인가 ?](#로그인-시-보관된-대화를-서버로-어떻게-이관할-것인가-)
        - [이 과정에서 생겼던 문제](#이과정에서-생겼던-문제)
        - [해결 방법](#해결-방법)  
  

<br/>
<br/>

# 프로젝트 기획 동기

오버워치의 승률, 픽률, 공략 정보는 이미 여러 곳에 존재합니다. 하지만 원하는 정보를 얻으려면 통계 사이트, 유튜브, 커뮤니티를 일일이 검색하고 찾아다녀야 합니다.AI에게 물어보는 방법도 있지만, AI 모델은 과거 데이터로 학습되어 있어 실시간 통계나 최신 패치 정보에 대해 정확한 답변을 하기 어렵습니다. 

그래서 **"흩어진 오버워치 정보를 한곳에 모으고, 궁금한 건 AI에게 바로 질문하면 최신 데이터를 기반으로 답변해주면 어떨까?"** 라는 생각에서 OOW.GG를 기획하게 되었습니다.

<br/>

# 미리보기

<table>
  <tr>
    <td width="50%">
      <h3>메인 페이지 (영웅 통계)</h3>
    </td>
    <td width="50%">
      <h3></h3>
    </td>
  </tr>
    <tr>
    <td width="50%">
      <img width="1275" height="855" alt="스크린샷 2026-02-17 오후 9 25 13" src="https://github.com/user-attachments/assets/b4086818-1d4a-4524-a3fd-026f4d41e00c" />
    </td>
      <td width="50%">
        <ul>
            <li>
              실시간 통계 데이터를 제공
            <ul>
              <li>승률, 픽률 정렬을 통해 현재 강세 영웅을 파악할 수 있습니다.</li>
              <li>역할, 지역, 티어를 기준으로 통계를 확인할 수 있습니다.</li>
            </ul>
          </li>
          <li>
            영웅 분석
            <ul>
              <li>테이블 내 분석 버튼 클릭 시 사이드 패널이 열립니다.</li>
              <li>선택한 영웅의 분석 카드가 자동으로 생성됩니다.</li>
              <li>추천 질문을 선택하거나 직접 질문을 입력해 AI 답변을 받을 수 있습니다.</li>
            </ul>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
    <td width="50%">
      <h3>영웅 정보 페이지</h3>
    </td>
    <td width="50%">
      <h3></h3>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img width="1275" height="855" alt="스크린샷 2026-02-17 오후 9 26 18" src="https://github.com/user-attachments/assets/ffdb2024-a8f5-42b2-8101-65dfbd298730" />
    </td>
      <td width="50%">
        <ul>
            <li>
               전체 영웅 정보 제공
            <ul>
              <li>모든 영웅을 카드 형태의 목록으로 제공합니다.</li>
              <li>역할 기준으로 영웅을 확인할 수 있습니다.</li>
              <li>카드 클릭시 해당 영웅의 "상세 정보 페이지"로 이동합니다.</li>
            </ul>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
    <td width="50%">
      <h3>영웅 상세 페이지</h3>
    </td>
    <td width="50%">
      <h3></h3>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img width="1275" height="855" alt="스크린샷 2026-02-17 오후 9 26 01" src="https://github.com/user-attachments/assets/3f7c962f-68a1-4151-8381-dd467616e4b9" />
    </td>
      <td width="50%">
        <ul>
            <li>
               영웅 상세 정보 제공
            <ul>
              <li>기본 능력치를 제공합니다.</li>
              <li>스킬과 특전 구성을 확인할 수 있습니다.</li>
              <li>시너지가 좋은 영웅과 카운터 영웅을 제공합니다.</li>
            </ul>
          </li>
        </ul>
      </td>
    </tr>
      <tr>
    <td width="50%">
      <h3>AI 코치 (챗봇)</h3>
    </td>
    <td width="50%">
      <h3></h3>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img width="1275" height="855" alt="제목 없는 디자인 (2)" src="https://github.com/user-attachments/assets/c4804bf3-2b26-4a61-a851-1fbc7116fd51" />
    </td>
      <td width="50%">
        <ul>                                                                                           
         <li>오버워치 관련 질문을 입력하면 실시간으로 답변합니다.</li>
          <ul>
            <li>
              비회원
              <ul>
              <li>6시간당 최대 3회 질문할 수 있습니다.</li>
                <li>회원으로 로그인 할 경우 기존 대화 내용에 이어 대화를 이어갈 수 있습니다.</li>
              </ul>
            </li>
            <li>
              회원
              <ul>
                <li> 6시간당 최대 15회 질문할 수 있습니다.</li>
                <li>대화 내용이 자동 저장됩니다.</li>
                <li>대화 기록을 관리할 수 있습니다.</li>
              </ul>
            </li>
          </ul>
        </ul>
      </td>
    </tr>
  </table>

  
<br/>
<br/>

# 기술 스택

### 프론트엔드
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![TanStack Query](https://img.shields.io/badge/TanStack_Query-FF4154?style=for-the-badge&logo=reactquery&logoColor=white)
![Zustand](https://img.shields.io/badge/Zustand-433E38?style=for-the-badge&logo=react&logoColor=white)
![React Router](https://img.shields.io/badge/React_Router-CA4245?style=for-the-badge&logo=react-router&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)


### 백엔드
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-000000?style=for-the-badge)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)


### 테스트
![Vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white)
![React Testing Library](https://img.shields.io/badge/React_Testing_Library-E33332?style=for-the-badge&logo=testing-library&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)


### 배포
![AWS EC2](https://img.shields.io/badge/AWS_EC2-FF9900?style=for-the-badge&logo=amazon-ec2&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

<br/>
<br/>


# 개발 과정
## 오버워치 데이터 확보 전략
오버워치는 다른 게임과 달리 공식 API를 제공하지 않기 때문에 영웅 정보와 실시간 통계 데이터를 어떻게 확보할지가 가장 먼저 해결해야 할 문제였습니다. 데이터를 확보하는 방법으로 **공식 홈페이지를 직접 크롤링**하거나 **외부 API를 활용하는 방식**을 고민했습니다. 
<br/>

먼저 공식 홈페이지를 직접 크롤링하는 방식을 고려했습니다. 하지만 오버워치에는 40명 이상의 영웅이 있고, 각 영웅의 이미지와 스킬, 설명, 통계를 직접 수집해야 했기 때문에 많은 시간을 투자할 경우 AI 챗봇 기능 구현이 지연될 수 있다고 판단했습니다.
이에 따라, 데이터를 빠르게 확보할 수 있는 외부 API를 찾기로 했습니다.<br/>

OverFast API는 오버워치 공식 사이트 기반 데이터를 REST API 형태로 제공하는 오픈 소스입니다. 영웅 이미지와 스킬 정보 등을 JSON으로 받아올 수 있어 바로 서버에 연동할 수 있었고, 초기 구현에 필요한 데이터를 빠르게 확보할 수 있었습니다.
다만 외부 API에 의존하는 구조이기 때문에, OverFast API 서버에 장애가 발생할 경우 oow.gg 서비스에도 영향을 줄 수 있다는 한계가 있습니다.
<br/>

**해결방안** <br/>
이 문제를 해결하기 위해 oow.gg DB에 OverFast API 서버의 데이터를 주기적으로 동기화하는 구조를 설계했습니다.

<img width="1200" height="800" alt="APScheduler to OverFast API-2026-02-18-154529" src="https://github.com/user-attachments/assets/3e8b4669-d2a9-432c-b991-2895a9b79dc9" />

`APScheduler`라는 스케줄링 라이브러리를 사용하여 영웅 정보는 1일 1회, 경쟁전 통계는 12시간마다 자동으로 동기화되도록 구현했습니다. OverFast API 서버에 일시적인 장애가 발생하더라도, 사용자 요청은 마지막으로 동기화된 데이터를 기반으로 정상 응답됩니다.

<br/>
<br/>
<br/>

## AI 챗봇 구현
### LLM은 오버워치를 얼마나 알고 있을까 ? 

AI 챗봇 기능을 만들기 전에 먼저 확인한 것은 “LLM이 오버워치를 어느 정도까지 알고 있는가”였습니다. LLM은 학습 시점까지의 데이터만 기반으로 답변하기 때문에, LLM이 이해하고 있는 범위를 먼저 점검할 필요가 있었습니다. 아래는 LLM에게 오버워치 관련 질문을 했을 때의 답변입니다.

<table>
  <tr>
    <td><h3>잘 답변한 예시</h3></td>
  </tr>
  <tr>
    <td>
       <img width="1280" height="513" alt="test-2" src="https://github.com/user-attachments/assets/d6dbb489-45cf-4534-ba09-a24beef8b05e" />
    </td>
  </tr>
    <tr>
    <td><h4>영웅 역할, 기본 운영법, 조합 설명처럼 변동이 적은 정보는 큰 문제 없이 답변할 수 있었습니다.</h4></td>
  </tr>
</table>

<table>
  <tr>
    <td><h3>할루시네이션이 발생한 예시</h3></td>
  </tr>
  <tr>
    <td>
        <img width="1280" height="513" alt="test-1" src="https://github.com/user-attachments/assets/75977aac-2fd9-41c2-bd0d-4125c6676fad" />
    </td>
  </tr>
    <tr>
    <td><h4>최신 패치 내용이나 실시간 통계처럼 시간에 따라 변하는 정보에는 정확한 답변을 기대하기 어려웠습니다.</h4></td>
  </tr>
</table>

이 결과를 바탕으로 LLM이 부족한 영역을 데이터 소스별로 보완하는 방식을 생각했습니다. 

<br/>

### 해결 방안: Tool Calling 기반 설계
> `Tool Calling`이란, LLM이 답변 중 필요한 도구(검색, DB 조회 등)를 호출해, 그 결과를 반영해 답변하는 방식입니다.

검증 결과를 바탕으로, LLM이 부족한 영역을 보완하기 위해 외부 데이터를 조회하는 도구들을 직접 설계했습니다. 예를 들어 통계가 필요한 질문에는 DB 조회 도구를, 최신 패치 정보가 필요한 질문에는 웹 검색 도구를 호출하는 방식입니다.

핵심 문제는 질문마다 필요한 도구가 달라, 고정 규칙으로 도구를 선택하기 어려웠다는 점이었습니다. "겐지 정보 알려줘"라는 질문만 해도 스킬 정보(DB 조회)가 필요한지, 공략 문서(RAG 검색)가 필요한지, 최신 너프 내용(웹 검색)이 필요한지 질문 문장만 보고 결정하기는 어려웠습니다. 따라서 질문과 각 도구의 설명을 함께 보고 LLM이 호출 대상을 직접 판단하도록 했습니다.

각 도구는 `LangChain`의 `@tool` 데코레이터로 정의했으며, `docstring`에 "이 도구를 언제, 어떤 질문에 사용해야 하는지"를 작성해 LLM이 판단 기준으로 활용하도록 했습니다.

사용자 질문이 들어오면 아래 순서로 처리됩니다.
1. LLM이 질문과 도구 설명을 보고 사용할 도구를 선택합니다.  
2. 백엔드가 선택된 도구를 실행해 데이터를 조회합니다.  
3. 조회 결과를 LLM에 다시 전달합니다.  
4. LLM이 결과를 반영해 최종 답변을 생성합니다.

이 구조에 맞춰 질문 종류에 따라 도구 세 가지를 구현했습니다.

| 도구 | 역할 | 구현 방식 |
|---|---|---|
| 공략 문서 검색 | 영웅 조합, 경쟁전 팁 등 | RAG (벡터 유사도 검색) |
| 웹 검색 | 패치노트, 대회 정보 등 | `Tavily API` |
| 통계 조회 | 승률, 픽률, 카운터 | oow.gg DB 직접 조회 |

<br/>

### RAG: 오버워치 공략 문서 기반 답변 보강
> RAG란, LLM이 답변을 생성하기 전에 관련 문서를 먼저 검색해 참고하는 방식입니다. LLM이 직접 학습하지 않은 내용도 제공된 자료를 바탕으로 답변을 생성할 수 있습니다.

LLM은 오버워치 기본 지식은 갖추고 있지만, 경쟁전 팁이나 신규 영웅 정보 같은 게임 특화 내용은 충분히 학습되어 있지 않습니다. 이를 보완하기 위해 해당 내용을 별도 문서로 정리하고, 사용자가 관련 질문을 하면 AI가 해당 문서를 먼저 검색해 참고한 뒤 답변하도록 구현했습니다.

사용자의 질문이 들어오면 벡터로 변환한 뒤, 저장된 문서들과 유사도를 비교해 관련성이 높은 문서를 가져와 LLM에 함께 전달합니다. `match_threshold`(유사도 임계값)는 0.5 이상에서 관련 문서가 누락되는 경우가 있고, 0.3 이하에서는 관련 없는 문서가 다수 포함되어 테스트를 거쳐 0.4로 설정했습니다.


```python
@tool
async def search_rag(query: str) -> str:
    """오버워치 전략, 조합, 팁 등의 질문에 사용하세요."""

    query_embedding = await embeddings.aembed_query(query)

    result = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_threshold": 0.4,
            "match_count": 5,
        },
    ).execute()
```

<br/>

### Tavily API: 최신 정보 실시간 검색
LLM의 학습 데이터는 특정 시점까지만 반영되기 때문에, 최신 패치노트나 대회 일정처럼 계속 변하는 정보는 실시간으로 외부에서 가져와야 했습니다. 이를 위해 `Tavily API`를 사용해 두 가지 도구를 구현했습니다.

#### 웹 검색 

대회 일정, 프로 선수/팀 정보 검색 결과의 정확도를 높이기 위해 두 가지 처리를 했습니다. 먼저 `include_domains`옵션으로 검색 대상을 오버워치 관련 정보가 정확하고 최신으로 유지되는 사이트(Liquipedia, 오버워치 공식 사이트, 오버워치 인벤, 나무위키)로 제한했습니다.

또한 `query`에 "오버워치"를 접두어로 붙여 무관한 검색 결과가 포함되지 않도록 했습니다.

```python
@tool
async def search_web(query: str) -> str:
    """
    최신 패치노트, 대회 일정, 프로 선수/팀 정보 등
    최신성이 중요한 정보를 검색합니다.
    """

    result = await asyncio.to_thread(
        tavily.search,
        query=f"오버워치 {query}",  
        include_domains=ALLOWED_DOMAINS, 
        max_results=5,
    )
```

#### 패치노트 조회
패치노트는 웹 검색 결과에 의존하면 오래된 정보가 섞일 수 있습니다. 이를 방지하기 위해 오버워치 공식 패치노트 페이지에서 직접 내용을 추출하는 방식을 사용했습니다.
`tavily.extract()`는 특정 URL의 콘텐츠를 그대로 가져오기 때문에, 검색 결과를 거치지 않고 항상 최신 패치노트를 제공할 수 있습니다.

```python
PATCH_NOTES_URL = "https://overwatch.blizza
rd.com/ko-kr/news/patch-notes/"

@tool
async def get_patch_notes() -> str:
    """오버워치 공식 최신 패치노트를
조회합니다."""

    result = await asyncio.to_thread(
        tavily.extract,
        urls=[PATCH_NOTES_URL],
    )
```
<br/>


### DB 조회: 영웅 정보 직접 조회

영웅 데이터(픽률, 승률, 카운터, 스킬)가 필요한 질문이 들어오면 AI가 직접 DB를 조회해 반환합니다. 이 데이터는 `APScheduler`를 통해 주기적으로 동기화되고 있기 때문에 항상 최신 값을 제공할 수 있습니다.

```python
@tool
def get_hero_stats(hero_key: str) -> str:
    """특정 영웅의 통계 정보(픽률, 승률 등)를 조회합니다."""
    result = supabase.table("hero_stats") \
        .select("*") \
        .eq("hero_key", hero_key) \
        .order("synced_at", desc=True) \
        .limit(1) \
        .execute()
```

### 실제 답변 화면
<img width="1376" height="567" alt="aaa1" src="https://github.com/user-attachments/assets/5693e811-99f0-41a5-8e39-e73a7747873c" />

다음과 같이 사용자의 질문 내용에 따라 RAG 검색, 웹 검색, DB 조회 중 적절한 도구가 자동으로 선택되어 답변이 생성됩니다.


<br/>

## 응답을 사용자에게 전달하기까지

AI가 만든 답변이 사용자 화면에 도달하기까지, 그 사이에서 해결해야 할 문제들이 있었습니다. 응답이 실시간으로 화면에 나타나야 했고, 종류가 다른 상태들이 한 화면에서 함께 동작해야 했습니다. 또한 비회원이 로그인해도 대화가 끊기지 않아야 했습니다.


### 스트리밍 응답을 화면에 그리기
<img width="1269" height="585" alt="ex1111" src="https://github.com/user-attachments/assets/f39a99f6-7a3f-4f55-ae49-249d95052439" />
<br/>
<br/>

처음 구현했을 때는 AI 응답을 완성된 형태로 한번에 전달했습니다. 하지만 AI가 답변을 생성하는 동안 사용자는 아무런 피드백 없이 빈 화면을 마주하게 되어, 응답이 오고 있는지 알 수 없는 문제가 있었습니다. 이 문제를 해결하기 위해 응답을 실시간으로 전달하는 방식을 검토했습니다.

#### 방법1. Polling
일정 간격으로 서버에 반복 요청하는 방식입니다. 응답이 준비가 되지 않았는데도 서버에 계속 요청을 보내야해서 서버에 불필요한 부하가 발생하고 실시간성이 떨어진다고 판단했습니다.

#### 방법2. WebSocket
클라이언트와 서버가 양방향으로 통신하는 방식입니다. 실시간성은 좋지만 AI 챗봇처럼 서버가 일방적으로 응답을 보내는 구조에서는 양방향 연결 관리가 불필요했습니다. 또한 연결유지, 재연결 처리, 서버 인프라 구성 등 추가로 개발 시간이 소요된다고 판단했습니다.

#### 방법3. SSE(Server Sent Events) ✓
HTTP 기반으로 서버 → 클라이언트 단방향 스트리밍을 지원하는 방식입니다. AI챗봇은 서버가 응답을 한 방향으로 보내는 구조이므로 SSE가 가장 적합했습니다.

> ReadableStream API란 서버에서 도착하는 데이터를 한번에 기다리지 않고, 청크 단위로 순차적으로 읽어들이는 브라우저 API입니다.

SSE를 적용하면서 어려웠던 점은 청크 경계 문제였습니다. ReadableStream이 전달하는 청크는 하나의 완성된 메시지 단위로 잘려서 오지 않습니다. 버퍼링 없이 청크를 바로 파싱하면 메시지가 중간에 잘린 채로 들어와 파싱 에러가 발생합니다. 

이를 해결하기 위해 불완전한 청크를 버퍼에 보관하고, 다음 청크와 합쳐서 완전한 메시지가 되었을 때 파싱하는 방식을 적용했습니다.

| 순서 | 수신 데이터 | 동작 |
|---|---|---|
| 청크1(불완전한 데이터) 도착 | `data: {"type":"con` | 버퍼에 보관 |
| 청크2 도착 | `tent","content":"겐지는"}\n` | 버퍼와 합침 |
| 합친 결과 | `data: {"type":"content","content":"겐지는"}` | 완전한 메시지 → 파싱 |

또한 SSE 이벤트를 content, meta, error 세 가지 타입으로 구분했습니다. 
```javascript
switch (data.type) {
  case "content":
    onChunk(data.content);
    break;

  case "meta":
    await onMeta.({ conversationId: data.conversationId });
    break;

  case "error":
    onError(new Error(data.content));
    return;
}
```
- `content`: AI 응답 텍스트를 청크 단위로 전달합니다.
- `meta`: 비회원의 첫 메시지 시 새로 생성된 대화 ID를 프론트엔드에 전달합니다.
- `error`: 스트림 도중 발생한 에러를 전파하여, 사용자가 멈춘 화면을 보지 않도록 처리합니다.

#### 스트리밍 응답 화면
<img width="1280" alt="ex" src="https://github.com/user-attachments/assets/c784af55-cb75-45ad-ad91-2e1ff343ccb3" />
<br/>
<br/>


### 상태를 나눈 기준
AI 챗봇에는 성격이 다른 여러 종류의 데이터가 존재합니다.
- 서버에서 받아온 대화 기록
- 실시간 스트리밍 텍스트
- 패널 열림/닫힘 같은 UI 상태
- 사용자가 입력 중인 텍스트

이 데이터들을 하나의 방식으로 관리하자 불필요한 리렌더링이 발생하거나, 캐싱이 필요 없는 데이터까지 캐시에 들어가는 문제가 생겼습니다.

처음에는 "서버에서 오면 TanStack Query", 아니면 "로컬 상태"로 나눴습니다. 하지만 스트리밍 응답처럼 서버에서 오지만 캐싱할 수 없는 데이터가 있어서 이 기준만으로는 부족했습니다.
그래서 다음과 같은 판단 흐름으로 상태를 나눴습니다.

```
같은 쿼리 키로 재요청했을 때 동일한 데이터를 받을 수 있는가?
├─ YES → TanStack Query (서버 상태 캐싱)
└─ NO  → 여러 컴포넌트가 공유하는가?
         ├─ YES → Zustand (전역 상태)
         └─ NO  → useState (컴포넌트 로컬 상태)
```

  | 상태 관리 방식 | 판단 기준 | 예시 |
  |---|---|---|
  | TanStack Query | 같은 키로 다시 요청하면 같은 데이터를 받을 수 있음 | 대화 메시지, 영웅 목록 |
  | Zustand | 재요청할 수 없지만, 여러 컴포넌트가 함께 사용함 | 스트리밍 중간 텍스트, 현재 대화 ID
  | useState | 해당 컴포넌트 안에서만 사용됨 | 입력값, 정렬 옵션 |

  예를 들어 스트리밍 중인 텍스트는 SSE를 통해 서버에서 오는 데이터지만, `TanStack Query`가 아닌 `Zustand`에 저장합니다. SSE 스트리밍 응답은 한번 완료되면 사라지고, 같은 스트리밍 응답을 다시 요청할 수 없기 때문입니다. 반면 대화 메시지는 페이지를 새로고침해도 서버에서 동일한 데이터를 다시 받을 수 있으므로 `TanStack Query`로 관리했습니다.

<br/>

### 비회원에서 회원으로, 대화 이어가기                                                            
                                                                                                    
사용자가 로그인 없이도 AI 챗봇을 바로 사용할 수 있고, 이후 로그인하더라도 대화가 자연스럽게 이어지는 것을 목표로 했습니다. 
이를 위해 두 가지를 설계해야 했습니다.                             
                                                                                                    
- 비회원 대화를 어디에 보관할 것인가
- 로그인 시 보관된 대화를 서버로 어떻게 이관할 것인가
<br/>  

### 비회원 대화를 어디에 저장할까 ?  

**방법1. localStorage** <br/>
브라우저를 닫아도 데이터가 유지됩니다. 하지만 비회원 대화는 로그인 시 서버로 이관하면 더 이상 보관할 필요가 없어, 영구 저장은 불필요하다고 판단했습니다.

**방법2. IndexedDB** <br/>
대용량의 구조화된 데이터를 저장할 수 있습니다. 하지만 비회원 대화는 로그인 전까지의 짧은 대화를 임시로 보관하는 것이 전부여서, `IndexedDB`의 기능이 필요하지 않았습니다.

**방법3. sessionStorage ✓** <br/>
탭을 닫으면 데이터가 자동으로 정리됩니다. 비회원 대화는 로그인 전까지만 유지하면 되므로, 탭 단위로 생명주기가 끝나는 `sessionStorage`가 가장 적합했습니다
<br/>
<br/>

### 로그인 시 보관된 대화를 서버로 어떻게 이관할 것인가 ?
비회원이 로그인하면 `sessionStorage`에 보관된 대화를 서버로 이관해야 합니다. 이관 흐름은 다음과 같습니다.
1. 비회원이 로그인합니다.
2. `sessionStorage`에 저장된 대화가 있는지 확인합니다.
3. 대화가 있으면 서버로 전송합니다.
4. 서버 저장이 완료되면 `sessionStorage`를 비웁니다.

#### 이과정에서 생겼던 문제
아래 이미지와 같이 서버 저장이 완료되기 전까지 같은 메시지가 서버와 로컬에 동시에 존재하게 되어, 화면에 동일한 메시지가 두 번 표시되었습니다.

<img width="1280" height="569" alt="ex221" src="https://github.com/user-attachments/assets/629e5148-33ac-484b-84af-793ae0f699de" />


<br/>

#### 해결 방법
이를 해결하기 위해 서버 메시지와 로컬 메시지를 1:1로 매칭하여, 서버에 이미 존재하는 메시지는 로컬에서 제거하는 병합 로직을 구현했습니다.

  ```typescript                                                                                                              
  const remainingServerMessages = [...serverMessages];

  return localMessages.filter((local) => {
    const matchIndex = remainingServerMessages.findIndex(
      (server) => server.content === local.content && server.role === local.role,
    );

    if (matchIndex >= 0) {
      remainingServerMessages.splice(matchIndex, 1);

      return false;
    }
    return true;
  });
```
# oow.gg

<div align="center">
  <p>
    <b>오버워치 인게임 승률과 픽률을 제공하고 </b><br/>
    <b>AI 챗봇에게 질문하여 필요한 정보를 바로 얻을 수 있는 서비스입니다.</b>
    <br/>
    <br/>
    <a href="https://github.com/oow-project/oow-frontend" rel="noopener noreferrer" target="_blank">프론트엔드</a> | <a href="https://github.com/oow-project/oow-backend" rel="noopener noreferrer" target="_blank">백엔드</a>
  </p>
  <a href="https://www.oowgg.com/" rel="noopener noreferrer" target="_blank">
    <img width="1280" height="640" alt="OOW GG main" src="https://github.com/user-attachments/assets/aa4fb97b-2055-4195-aa35-7d822b5a4a87" />
  </a>
</div>

<br/>
<br/>

# 목차

- [프로젝트 기획 동기](#프로젝트-기획-동기)
- [미리보기](#미리보기)
  - [메인 페이지 (영웅 통계)](#메인-페이지-영웅-통계)
  - [영웅 정보 페이지](#영웅-정보-페이지)
  - [영웅 상세 페이지](#영웅-정보-페이지)
  - [AI 코치 (챗봇)](#ai-코치-챗봇)
- [기술 스택](#기술-스택)
- [개발 과정](#개발-과정)
  - [오버워치 데이터 확보 전략](#오버워치-데이터-확보-전략)
  - [AI 챗봇 구현](#ai-챗봇-구현)
    - [LLM은 오버워치를 얼마나 알고 있을까 ?](#llm은-오버워치를-얼마나-알고-있을까-)
    - [해결 방안: Tool Calling 기반 설계](#해결-방안-tool-calling-기반-설계)
    - [RAG: 오버워치 공략 문서 기반 답변 보강](#rag-오버워치-공략-문서-기반-답변-보강)
    - [Tavily API: 최신 정보 실시간 검색](#tavily-api-최신-정보-실시간-검색)
      - [웹 검색](#웹-검색)
      - [패치노트 조회](#패치노트-조회) 
    - [DB 조회:영웅 정보 직접 조회](#db-조회-영웅-정보-직접-조회)
    - [스트리밍 응답 화면](#스트리밍-응답-화면)
  - [응답을 사용자에게 전달하기까지](#응답을-사용자에게-전달하기까지)
    - [스트리밍 응답을 화면에 그리기](#스트리밍-응답을-화면에-그리기)
    - [상태를 나눈 기준](#상태를-나눈-기준)
    - [비회원에서 회원으로 대화를 이어가기](#비회원에서-회원으로-대화-이어가기)
      - [비회원 대화를 어디에 저장할까](#비회원-대화를-어디에-저장할까-)
      - [로그인 시 보관된 대화를 서버로 어떻게 이관할 것인가 ?](#로그인-시-보관된-대화를-서버로-어떻게-이관할-것인가-)
        - [이 과정에서 생겼던 문제](#이과정에서-생겼던-문제)
        - [해결 방법](#해결-방법)  
- [회고](#회고)
  

<br/>
<br/>

# 프로젝트 기획 동기

오버워치의 승률, 픽률, 공략 정보는 이미 여러 곳에 존재합니다. 하지만 원하는 정보를 얻으려면 통계 사이트, 유튜브, 커뮤니티를 일일이 검색하고 찾아다녀야 합니다.AI에게 물어보는 방법도 있지만, AI 모델은 과거 데이터로 학습되어 있어 실시간 통계나 최신 패치 정보에 대해 정확한 답변을 하기 어렵습니다. 

그래서 **"흩어진 오버워치 정보를 한곳에 모으고, 궁금한 건 AI에게 바로 질문하면 최신 데이터를 기반으로 답변해주면 어떨까?"** 라는 생각에서 OOW.GG를 기획하게 되었습니다.

<br/>

# 미리보기

<table>
  <tr>
    <td width="50%">
      <h3>메인 페이지 (영웅 통계)</h3>
    </td>
    <td width="50%">
      <h3></h3>
    </td>
  </tr>
    <tr>
    <td width="50%">
      <img width="1275" height="855" alt="스크린샷 2026-02-17 오후 9 25 13" src="https://github.com/user-attachments/assets/b4086818-1d4a-4524-a3fd-026f4d41e00c" />
    </td>
      <td width="50%">
        <ul>
            <li>
              실시간 통계 데이터를 제공
            <ul>
              <li>승률, 픽률 정렬을 통해 현재 강세 영웅을 파악할 수 있습니다.</li>
              <li>역할, 지역, 티어를 기준으로 통계를 확인할 수 있습니다.</li>
            </ul>
          </li>
          <li>
            영웅 분석
            <ul>
              <li>테이블 내 분석 버튼 클릭 시 사이드 패널이 열립니다.</li>
              <li>선택한 영웅의 분석 카드가 자동으로 생성됩니다.</li>
              <li>추천 질문을 선택하거나 직접 질문을 입력해 AI 답변을 받을 수 있습니다.</li>
            </ul>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
    <td width="50%">
      <h3>영웅 정보 페이지</h3>
    </td>
    <td width="50%">
      <h3></h3>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img width="1275" height="855" alt="스크린샷 2026-02-17 오후 9 26 18" src="https://github.com/user-attachments/assets/ffdb2024-a8f5-42b2-8101-65dfbd298730" />
    </td>
      <td width="50%">
        <ul>
            <li>
               전체 영웅 정보 제공
            <ul>
              <li>모든 영웅을 카드 형태의 목록으로 제공합니다.</li>
              <li>역할 기준으로 영웅을 확인할 수 있습니다.</li>
              <li>카드 클릭시 해당 영웅의 "상세 정보 페이지"로 이동합니다.</li>
            </ul>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
    <td width="50%">
      <h3>영웅 상세 페이지</h3>
    </td>
    <td width="50%">
      <h3></h3>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img width="1275" height="855" alt="스크린샷 2026-02-17 오후 9 26 01" src="https://github.com/user-attachments/assets/3f7c962f-68a1-4151-8381-dd467616e4b9" />
    </td>
      <td width="50%">
        <ul>
            <li>
               영웅 상세 정보 제공
            <ul>
              <li>기본 능력치를 제공합니다.</li>
              <li>스킬과 특전 구성을 확인할 수 있습니다.</li>
              <li>시너지가 좋은 영웅과 카운터 영웅을 제공합니다.</li>
            </ul>
          </li>
        </ul>
      </td>
    </tr>
      <tr>
    <td width="50%">
      <h3>AI 코치 (챗봇)</h3>
    </td>
    <td width="50%">
      <h3></h3>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img width="1275" height="855" alt="제목 없는 디자인 (2)" src="https://github.com/user-attachments/assets/c4804bf3-2b26-4a61-a851-1fbc7116fd51" />
    </td>
      <td width="50%">
        <ul>                                                                                           
         <li>오버워치 관련 질문을 입력하면 실시간으로 답변합니다.</li>
          <ul>
            <li>
              비회원
              <ul>
              <li>6시간당 최대 3회 질문할 수 있습니다.</li>
                <li>회원으로 로그인 할 경우 기존 대화 내용에 이어 대화를 이어갈 수 있습니다.</li>
              </ul>
            </li>
            <li>
              회원
              <ul>
                <li> 6시간당 최대 15회 질문할 수 있습니다.</li>
                <li>대화 내용이 자동 저장됩니다.</li>
                <li>대화 기록을 관리할 수 있습니다.</li>
              </ul>
            </li>
          </ul>
        </ul>
      </td>
    </tr>
  </table>

  
<br/>
<br/>

# 기술 스택

### 프론트엔드
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![TanStack Query](https://img.shields.io/badge/TanStack_Query-FF4154?style=for-the-badge&logo=reactquery&logoColor=white)
![Zustand](https://img.shields.io/badge/Zustand-433E38?style=for-the-badge&logo=react&logoColor=white)
![React Router](https://img.shields.io/badge/React_Router-CA4245?style=for-the-badge&logo=react-router&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)


### 백엔드
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-000000?style=for-the-badge)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)


### 테스트
![Vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white)
![React Testing Library](https://img.shields.io/badge/React_Testing_Library-E33332?style=for-the-badge&logo=testing-library&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)


### 배포
![AWS EC2](https://img.shields.io/badge/AWS_EC2-FF9900?style=for-the-badge&logo=amazon-ec2&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

<br/>
<br/>


# 개발 과정
## 오버워치 데이터 확보 전략
오버워치는 다른 게임과 달리 공식 API를 제공하지 않기 때문에 영웅 정보와 실시간 통계 데이터를 어떻게 확보할지가 가장 먼저 해결해야 할 문제였습니다. 데이터를 확보하는 방법으로 **공식 홈페이지를 직접 크롤링**하거나 **외부 API를 활용하는 방식**을 고민했습니다. 
<br/>

먼저 공식 홈페이지를 직접 크롤링하는 방식을 고려했습니다. 하지만 오버워치에는 40명 이상의 영웅이 있고, 각 영웅의 이미지와 스킬, 설명, 통계를 직접 수집해야 했기 때문에 많은 시간을 투자할 경우 AI 챗봇 기능 구현이 지연될 수 있다고 판단했습니다.
이에 따라, 데이터를 빠르게 확보할 수 있는 외부 API를 찾기로 했습니다.<br/>

OverFast API는 오버워치 공식 사이트 기반 데이터를 REST API 형태로 제공하는 오픈 소스입니다. 영웅 이미지와 스킬 정보 등을 JSON으로 받아올 수 있어 바로 서버에 연동할 수 있었고, 초기 구현에 필요한 데이터를 빠르게 확보할 수 있었습니다.
다만 외부 API에 의존하는 구조이기 때문에, OverFast API 서버에 장애가 발생할 경우 oow.gg 서비스에도 영향을 줄 수 있다는 한계가 있습니다.
<br/>

**해결방안** <br/>
이 문제를 해결하기 위해 oow.gg DB에 OverFast API 서버의 데이터를 주기적으로 동기화하는 구조를 설계했습니다.

<img width="1200" height="800" alt="APScheduler to OverFast API-2026-02-18-154529" src="https://github.com/user-attachments/assets/3e8b4669-d2a9-432c-b991-2895a9b79dc9" />

`APScheduler`라는 스케줄링 라이브러리를 사용하여 영웅 정보는 1일 1회, 경쟁전 통계는 12시간마다 자동으로 동기화되도록 구현했습니다. OverFast API 서버에 일시적인 장애가 발생하더라도, 사용자 요청은 마지막으로 동기화된 데이터를 기반으로 정상 응답됩니다.

<br/>
<br/>
<br/>

## AI 챗봇 구현
### LLM은 오버워치를 얼마나 알고 있을까 ? 

AI 챗봇 기능을 만들기 전에 먼저 확인한 것은 “LLM이 오버워치를 어느 정도까지 알고 있는가”였습니다. LLM은 학습 시점까지의 데이터만 기반으로 답변하기 때문에, LLM이 이해하고 있는 범위를 먼저 점검할 필요가 있었습니다. 아래는 LLM에게 오버워치 관련 질문을 했을 때의 답변입니다.

<table>
  <tr>
    <td><h3>잘 답변한 예시</h3></td>
  </tr>
  <tr>
    <td>
       <img width="1280" height="513" alt="test-2" src="https://github.com/user-attachments/assets/d6dbb489-45cf-4534-ba09-a24beef8b05e" />
    </td>
  </tr>
    <tr>
    <td><h4>영웅 역할, 기본 운영법, 조합 설명처럼 변동이 적은 정보는 큰 문제 없이 답변할 수 있었습니다.</h4></td>
  </tr>
</table>

<table>
  <tr>
    <td><h3>할루시네이션이 발생한 예시</h3></td>
  </tr>
  <tr>
    <td>
        <img width="1280" height="513" alt="test-1" src="https://github.com/user-attachments/assets/75977aac-2fd9-41c2-bd0d-4125c6676fad" />
    </td>
  </tr>
    <tr>
    <td><h4>최신 패치 내용이나 실시간 통계처럼 시간에 따라 변하는 정보에는 정확한 답변을 기대하기 어려웠습니다.</h4></td>
  </tr>
</table>

이 결과를 바탕으로 LLM이 부족한 영역을 데이터 소스별로 보완하는 방식을 생각했습니다. 

<br/>

### 해결 방안: Tool Calling 기반 설계
> `Tool Calling`이란, LLM이 답변 중 필요한 도구(검색, DB 조회 등)를 호출해, 그 결과를 반영해 답변하는 방식입니다.

검증 결과를 바탕으로, LLM이 부족한 영역을 보완하기 위해 외부 데이터를 조회하는 도구들을 직접 설계했습니다. 예를 들어 통계가 필요한 질문에는 DB 조회 도구를, 최신 패치 정보가 필요한 질문에는 웹 검색 도구를 호출하는 방식입니다.

핵심 문제는 질문마다 필요한 도구가 달라, 고정 규칙으로 도구를 선택하기 어려웠다는 점이었습니다. "겐지 정보 알려줘"라는 질문만 해도 스킬 정보(DB 조회)가 필요한지, 공략 문서(RAG 검색)가 필요한지, 최신 너프 내용(웹 검색)이 필요한지 질문 문장만 보고 결정하기는 어려웠습니다. 따라서 질문과 각 도구의 설명을 함께 보고 LLM이 호출 대상을 직접 판단하도록 했습니다.

각 도구는 `LangChain`의 `@tool` 데코레이터로 정의했으며, `docstring`에 "이 도구를 언제, 어떤 질문에 사용해야 하는지"를 작성해 LLM이 판단 기준으로 활용하도록 했습니다.

사용자 질문이 들어오면 아래 순서로 처리됩니다.
1. LLM이 질문과 도구 설명을 보고 사용할 도구를 선택합니다.  
2. 백엔드가 선택된 도구를 실행해 데이터를 조회합니다.  
3. 조회 결과를 LLM에 다시 전달합니다.  
4. LLM이 결과를 반영해 최종 답변을 생성합니다.

이 구조에 맞춰 질문 종류에 따라 도구 세 가지를 구현했습니다.

| 도구 | 역할 | 구현 방식 |
|---|---|---|
| 공략 문서 검색 | 영웅 조합, 경쟁전 팁 등 | RAG (벡터 유사도 검색) |
| 웹 검색 | 패치노트, 대회 정보 등 | `Tavily API` |
| 통계 조회 | 승률, 픽률, 카운터 | oow.gg DB 직접 조회 |

<br/>

### RAG: 오버워치 공략 문서 기반 답변 보강
> RAG란, LLM이 답변을 생성하기 전에 관련 문서를 먼저 검색해 참고하는 방식입니다. LLM이 직접 학습하지 않은 내용도 제공된 자료를 바탕으로 답변을 생성할 수 있습니다.

LLM은 오버워치 기본 지식은 갖추고 있지만, 경쟁전 팁이나 신규 영웅 정보 같은 게임 특화 내용은 충분히 학습되어 있지 않습니다. 이를 보완하기 위해 해당 내용을 별도 문서로 정리하고, 사용자가 관련 질문을 하면 AI가 해당 문서를 먼저 검색해 참고한 뒤 답변하도록 구현했습니다.

사용자의 질문이 들어오면 벡터로 변환한 뒤, 저장된 문서들과 유사도를 비교해 관련성이 높은 문서를 가져와 LLM에 함께 전달합니다. `match_threshold`(유사도 임계값)는 0.5 이상에서 관련 문서가 누락되는 경우가 있고, 0.3 이하에서는 관련 없는 문서가 다수 포함되어 테스트를 거쳐 0.4로 설정했습니다.


```python
@tool
async def search_rag(query: str) -> str:
    """오버워치 전략, 조합, 팁 등의 질문에 사용하세요."""

    query_embedding = await embeddings.aembed_query(query)

    result = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_threshold": 0.4,
            "match_count": 5,
        },
    ).execute()
```

<br/>

### Tavily API: 최신 정보 실시간 검색
LLM의 학습 데이터는 특정 시점까지만 반영되기 때문에, 최신 패치노트나 대회 일정처럼 계속 변하는 정보는 실시간으로 외부에서 가져와야 했습니다. 이를 위해 `Tavily API`를 사용해 두 가지 도구를 구현했습니다.

#### 웹 검색 

대회 일정, 프로 선수/팀 정보 검색 결과의 정확도를 높이기 위해 두 가지 처리를 했습니다. 먼저 `include_domains`옵션으로 검색 대상을 오버워치 관련 정보가 정확하고 최신으로 유지되는 사이트(Liquipedia, 오버워치 공식 사이트, 오버워치 인벤, 나무위키)로 제한했습니다.

또한 `query`에 "오버워치"를 접두어로 붙여 무관한 검색 결과가 포함되지 않도록 했습니다.

```python
@tool
async def search_web(query: str) -> str:
    """
    최신 패치노트, 대회 일정, 프로 선수/팀 정보 등
    최신성이 중요한 정보를 검색합니다.
    """

    result = await asyncio.to_thread(
        tavily.search,
        query=f"오버워치 {query}",  
        include_domains=ALLOWED_DOMAINS, 
        max_results=5,
    )
```

#### 패치노트 조회
패치노트는 웹 검색 결과에 의존하면 오래된 정보가 섞일 수 있습니다. 이를 방지하기 위해 오버워치 공식 패치노트 페이지에서 직접 내용을 추출하는 방식을 사용했습니다.
`tavily.extract()`는 특정 URL의 콘텐츠를 그대로 가져오기 때문에, 검색 결과를 거치지 않고 항상 최신 패치노트를 제공할 수 있습니다.

```python
PATCH_NOTES_URL = "https://overwatch.blizza
rd.com/ko-kr/news/patch-notes/"

@tool
async def get_patch_notes() -> str:
    """오버워치 공식 최신 패치노트를
조회합니다."""

    result = await asyncio.to_thread(
        tavily.extract,
        urls=[PATCH_NOTES_URL],
    )
```
<br/>


### DB 조회: 영웅 정보 직접 조회

영웅 데이터(픽률, 승률, 카운터, 스킬)가 필요한 질문이 들어오면 AI가 직접 DB를 조회해 반환합니다. 이 데이터는 `APScheduler`를 통해 주기적으로 동기화되고 있기 때문에 항상 최신 값을 제공할 수 있습니다.

```python
@tool
def get_hero_stats(hero_key: str) -> str:
    """특정 영웅의 통계 정보(픽률, 승률 등)를 조회합니다."""
    result = supabase.table("hero_stats") \
        .select("*") \
        .eq("hero_key", hero_key) \
        .order("synced_at", desc=True) \
        .limit(1) \
        .execute()
```

### 실제 답변 화면
<img width="1376" height="567" alt="aaa1" src="https://github.com/user-attachments/assets/5693e811-99f0-41a5-8e39-e73a7747873c" />

다음과 같이 사용자의 질문 내용에 따라 RAG 검색, 웹 검색, DB 조회 중 적절한 도구가 자동으로 선택되어 답변이 생성됩니다.


<br/>

## 응답을 사용자에게 전달하기까지

AI가 만든 답변이 사용자 화면에 도달하기까지, 그 사이에서 해결해야 할 문제들이 있었습니다. 응답이 실시간으로 화면에 나타나야 했고, 종류가 다른 상태들이 한 화면에서 함께 동작해야 했습니다. 또한 비회원이 로그인해도 대화가 끊기지 않아야 했습니다.


### 스트리밍 응답을 화면에 그리기
<img width="1269" height="585" alt="ex1111" src="https://github.com/user-attachments/assets/f39a99f6-7a3f-4f55-ae49-249d95052439" />
<br/>
<br/>

처음 구현했을 때는 AI 응답을 완성된 형태로 한번에 전달했습니다. 하지만 AI가 답변을 생성하는 동안 사용자는 아무런 피드백 없이 빈 화면을 마주하게 되어, 응답이 오고 있는지 알 수 없는 문제가 있었습니다. 이 문제를 해결하기 위해 응답을 실시간으로 전달하는 방식을 검토했습니다.

#### 방법1. Polling
일정 간격으로 서버에 반복 요청하는 방식입니다. 응답이 준비가 되지 않았는데도 서버에 계속 요청을 보내야해서 서버에 불필요한 부하가 발생하고 실시간성이 떨어진다고 판단했습니다.

#### 방법2. WebSocket
클라이언트와 서버가 양방향으로 통신하는 방식입니다. 실시간성은 좋지만 AI 챗봇처럼 서버가 일방적으로 응답을 보내는 구조에서는 양방향 연결 관리가 불필요했습니다. 또한 연결유지, 재연결 처리, 서버 인프라 구성 등 추가로 개발 시간이 소요된다고 판단했습니다.

#### 방법3. SSE(Server Sent Events) ✓
HTTP 기반으로 서버 → 클라이언트 단방향 스트리밍을 지원하는 방식입니다. AI챗봇은 서버가 응답을 한 방향으로 보내는 구조이므로 SSE가 가장 적합했습니다.

> ReadableStream API란 서버에서 도착하는 데이터를 한번에 기다리지 않고, 청크 단위로 순차적으로 읽어들이는 브라우저 API입니다.

SSE를 적용하면서 어려웠던 점은 청크 경계 문제였습니다. ReadableStream이 전달하는 청크는 하나의 완성된 메시지 단위로 잘려서 오지 않습니다. 버퍼링 없이 청크를 바로 파싱하면 메시지가 중간에 잘린 채로 들어와 파싱 에러가 발생합니다. 

이를 해결하기 위해 불완전한 청크를 버퍼에 보관하고, 다음 청크와 합쳐서 완전한 메시지가 되었을 때 파싱하는 방식을 적용했습니다.

| 순서 | 수신 데이터 | 동작 |
|---|---|---|
| 청크1(불완전한 데이터) 도착 | `data: {"type":"con` | 버퍼에 보관 |
| 청크2 도착 | `tent","content":"겐지는"}\n` | 버퍼와 합침 |
| 합친 결과 | `data: {"type":"content","content":"겐지는"}` | 완전한 메시지 → 파싱 |

또한 SSE 이벤트를 content, meta, error 세 가지 타입으로 구분했습니다. 
```javascript
switch (data.type) {
  case "content":
    onChunk(data.content);
    break;

  case "meta":
    await onMeta.({ conversationId: data.conversationId });
    break;

  case "error":
    onError(new Error(data.content));
    return;
}
```
- `content`: AI 응답 텍스트를 청크 단위로 전달합니다.
- `meta`: 비회원의 첫 메시지 시 새로 생성된 대화 ID를 프론트엔드에 전달합니다.
- `error`: 스트림 도중 발생한 에러를 전파하여, 사용자가 멈춘 화면을 보지 않도록 처리합니다.

#### 스트리밍 응답 화면
<img width="1280" alt="ex" src="https://github.com/user-attachments/assets/c784af55-cb75-45ad-ad91-2e1ff343ccb3" />
<br/>
<br/>


### 상태를 나눈 기준
AI 챗봇에는 성격이 다른 여러 종류의 데이터가 존재합니다.
- 서버에서 받아온 대화 기록
- 실시간 스트리밍 텍스트
- 패널 열림/닫힘 같은 UI 상태
- 사용자가 입력 중인 텍스트

이 데이터들을 하나의 방식으로 관리하자 불필요한 리렌더링이 발생하거나, 캐싱이 필요 없는 데이터까지 캐시에 들어가는 문제가 생겼습니다.

처음에는 "서버에서 오면 TanStack Query", 아니면 "로컬 상태"로 나눴습니다. 하지만 스트리밍 응답처럼 서버에서 오지만 캐싱할 수 없는 데이터가 있어서 이 기준만으로는 부족했습니다.
그래서 다음과 같은 판단 흐름으로 상태를 나눴습니다.

```
같은 쿼리 키로 재요청했을 때 동일한 데이터를 받을 수 있는가?
├─ YES → TanStack Query (서버 상태 캐싱)
└─ NO  → 여러 컴포넌트가 공유하는가?
         ├─ YES → Zustand (전역 상태)
         └─ NO  → useState (컴포넌트 로컬 상태)
```

  | 상태 관리 방식 | 판단 기준 | 예시 |
  |---|---|---|
  | TanStack Query | 같은 키로 다시 요청하면 같은 데이터를 받을 수 있음 | 대화 메시지, 영웅 목록 |
  | Zustand | 재요청할 수 없지만, 여러 컴포넌트가 함께 사용함 | 스트리밍 중간 텍스트, 현재 대화 ID
  | useState | 해당 컴포넌트 안에서만 사용됨 | 입력값, 정렬 옵션 |

  예를 들어 스트리밍 중인 텍스트는 SSE를 통해 서버에서 오는 데이터지만, `TanStack Query`가 아닌 `Zustand`에 저장합니다. SSE 스트리밍 응답은 한번 완료되면 사라지고, 같은 스트리밍 응답을 다시 요청할 수 없기 때문입니다. 반면 대화 메시지는 페이지를 새로고침해도 서버에서 동일한 데이터를 다시 받을 수 있으므로 `TanStack Query`로 관리했습니다.

<br/>

### 비회원에서 회원으로, 대화 이어가기                                                            
                                                                                                    
사용자가 로그인 없이도 AI 챗봇을 바로 사용할 수 있고, 이후 로그인하더라도 대화가 자연스럽게 이어지는 것을 목표로 했습니다. 
이를 위해 두 가지를 설계해야 했습니다.                             
                                                                                                    
- 비회원 대화를 어디에 보관할 것인가
- 로그인 시 보관된 대화를 서버로 어떻게 이관할 것인가
<br/>  

### 비회원 대화를 어디에 저장할까 ?  

**방법1. localStorage** <br/>
브라우저를 닫아도 데이터가 유지됩니다. 하지만 비회원 대화는 로그인 시 서버로 이관하면 더 이상 보관할 필요가 없어, 영구 저장은 불필요하다고 판단했습니다.

**방법2. IndexedDB** <br/>
대용량의 구조화된 데이터를 저장할 수 있습니다. 하지만 비회원 대화는 로그인 전까지의 짧은 대화를 임시로 보관하는 것이 전부여서, `IndexedDB`의 기능이 필요하지 않았습니다.

**방법3. sessionStorage ✓** <br/>
탭을 닫으면 데이터가 자동으로 정리됩니다. 비회원 대화는 로그인 전까지만 유지하면 되므로, 탭 단위로 생명주기가 끝나는 `sessionStorage`가 가장 적합했습니다
<br/>
<br/>

### 로그인 시 보관된 대화를 서버로 어떻게 이관할 것인가 ?
비회원이 로그인하면 `sessionStorage`에 보관된 대화를 서버로 이관해야 합니다. 이관 흐름은 다음과 같습니다.
1. 비회원이 로그인합니다.
2. `sessionStorage`에 저장된 대화가 있는지 확인합니다.
3. 대화가 있으면 서버로 전송합니다.
4. 서버 저장이 완료되면 `sessionStorage`를 비웁니다.

#### 이과정에서 생겼던 문제
아래 이미지와 같이 서버 저장이 완료되기 전까지 같은 메시지가 서버와 로컬에 동시에 존재하게 되어, 화면에 동일한 메시지가 두 번 표시되었습니다.

<img width="1280" height="569" alt="ex221" src="https://github.com/user-attachments/assets/629e5148-33ac-484b-84af-793ae0f699de" />


<br/>

#### 해결 방법
이를 해결하기 위해 서버 메시지와 로컬 메시지를 1:1로 매칭하여, 서버에 이미 존재하는 메시지는 로컬에서 제거하는 병합 로직을 구현했습니다.

  ```typescript                                                                                                              
  const remainingServerMessages = [...serverMessages];

  return localMessages.filter((local) => {
    const matchIndex = remainingServerMessages.findIndex(
      (server) => server.content === local.content && server.role === local.role,
    );

    if (matchIndex >= 0) {
      remainingServerMessages.splice(matchIndex, 1);

      return false;
    }
    return true;
  });
```

<br/>
<br/>

