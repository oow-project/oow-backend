"""
heroes API 통합 테스트

라우터 → 서비스 → 캐시 전체 흐름을 TestClient로 검증한다:
1. GET /api/heroes → 200 정상 응답
2. GET /api/heroes?role=tank → 필터링
3. GET /api/heroes?role=invalid → 400
4. GET /api/heroes/{heroKey} → 200
5. GET /api/heroes/{heroKey} → 404
6. GET /health → 200
"""

import json
from unittest.mock import MagicMock

MOCK_HEROES = [
    {"key": "ana", "name": "Ana", "portrait": "ana.png", "role": "support"},
    {"key": "reinhardt", "name": "Reinhardt", "portrait": "rein.png", "role": "tank"},
]


class TestGetHeroesAPI:
    """GET /api/heroes 통합 테스트"""

    async def test_영웅_목록을_정상_반환한다(self, client, mock_redis):
        mock_redis.get.return_value = json.dumps(MOCK_HEROES)

        response = await client.get("/api/heroes")

        assert response.status_code == 200
        data = response.json()
        assert "heroes" in data
        assert "total" in data

    async def test_role_필터가_적용된다(self, client, mock_redis):
        tank_only = [h for h in MOCK_HEROES if h["role"] == "tank"]
        mock_redis.get.return_value = json.dumps(tank_only)

        response = await client.get("/api/heroes", params={"role": "tank"})

        assert response.status_code == 200

    async def test_유효하지_않은_role이면_400을_반환한다(self, client, mock_redis):
        mock_redis.get.return_value = None
        mock_redis.set.return_value = True

        response = await client.get("/api/heroes", params={"role": "invalid"})

        assert response.status_code == 400


class TestGetHeroDetailAPI:
    """GET /api/heroes/{heroKey} 통합 테스트"""

    async def test_존재하는_영웅이면_200을_반환한다(self, client, mock_redis):
        hero_detail = {
            "key": "ana",
            "name": "Ana",
            "portrait": "ana.png",
            "role": "support",
            "hitpoints": {"health": 200, "armor": 0, "shields": 0, "total": 200},
            "abilities": {"skill": [], "perk_major": [], "perk_minor": []},
            "counters": [],
            "synergies": [],
        }
        mock_redis.get.return_value = json.dumps(hero_detail)

        response = await client.get("/api/heroes/ana")

        assert response.status_code == 200
        assert response.json()["key"] == "ana"

    async def test_존재하지_않는_영웅이면_404를_반환한다(self, client, mock_redis, mock_supabase):
        mock_redis.get.return_value = None
        mock_redis.set.return_value = True
        mock_supabase.execute.return_value = MagicMock(data=[])

        response = await client.get("/api/heroes/nonexistent")

        assert response.status_code == 404


class TestHealthAPI:
    """GET /health 통합 테스트"""

    async def test_헬스체크가_정상_응답한다(self, client):
        response = await client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "ok"
