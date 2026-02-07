"""
hero_service.py 단위 테스트

6가지 파라미터 유효성 검증과 데이터 변환 로직을 테스트한다:
1. 역할(role) 필터링 — all/tank/damage/support/invalid
2. 영웅 상세 조회 — 정상 / 존재하지 않는 영웅
3. 통계 조회 — 6개 파라미터 검증 + order_by 파싱
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.exceptions import InvalidParameterError, NotFoundError
from app.services.hero_service import get_hero_detail, get_hero_stats, get_heroes


MOCK_HEROES = [
    {"key": "ana", "name": "Ana", "portrait": "ana.png", "role": "support"},
    {"key": "reinhardt", "name": "Reinhardt", "portrait": "rein.png", "role": "tank"},
    {"key": "tracer", "name": "Tracer", "portrait": "tracer.png", "role": "damage"},
]


class TestGetHeroes:
    """영웅 목록 조회 테스트"""

    async def test_all이면_전체_목록을_반환한다(self, mock_supabase):
        mock_supabase.execute.return_value = MagicMock(data=MOCK_HEROES)

        result = await get_heroes("all")

        assert len(result) == 3

    async def test_tank이면_탱커만_반환한다(self, mock_supabase):
        tank_heroes = [h for h in MOCK_HEROES if h["role"] == "tank"]
        mock_supabase.execute.return_value = MagicMock(data=tank_heroes)

        result = await get_heroes("tank")

        assert all(h["role"] == "tank" for h in result)

    async def test_유효하지_않은_role이면_에러가_발생한다(self, mock_supabase):
        with pytest.raises(InvalidParameterError):
            await get_heroes("invalid")


class TestGetHeroDetail:
    """영웅 상세 조회 테스트"""

    async def test_존재하는_영웅이면_상세_정보를_반환한다(self, mock_supabase):
        hero_data = {
            "key": "ana",
            "name": "Ana",
            "portrait": "ana.png",
            "role": "support",
            "hitpoints_health": 200,
            "hitpoints_armor": 0,
            "hitpoints_shields": 0,
            "counters": [],
            "synergies": [],
        }
        mock_supabase.execute.side_effect = [
            MagicMock(data=[hero_data]),
            MagicMock(data=[]),
        ]

        result = await get_hero_detail("ana")

        assert result["key"] == "ana"
        assert result["hitpoints"]["health"] == 200
        assert result["hitpoints"]["total"] == 200
        assert "abilities" in result
        assert "counters" in result
        assert "synergies" in result

    async def test_존재하지_않는_영웅이면_NotFoundError가_발생한다(self, mock_supabase):
        mock_supabase.execute.return_value = MagicMock(data=[])

        with pytest.raises(NotFoundError):
            await get_hero_detail("nonexistent")


class TestGetHeroStats:
    """영웅 통계 조회 파라미터 검증 테스트"""

    async def test_기본_파라미터로_정상_응답을_반환한다(self, mock_supabase):
        mock_supabase.execute.return_value = MagicMock(data=[
            {
                "hero_key": "ana",
                "winrate": 52.5,
                "pickrate": 8.3,
                "synced_at": "2026-02-07T00:00:00",
                "heroes": {"name": "Ana", "portrait": "ana.png", "role": "support"},
            }
        ])

        result = await get_hero_stats()

        assert result["total"] == 1
        assert result["stats"][0]["winrate"] == 52.5
        assert result["filters"]["platform"] == "pc"

    async def test_유효하지_않은_platform이면_에러가_발생한다(self, mock_supabase):
        with pytest.raises(InvalidParameterError):
            await get_hero_stats(platform="mobile")

    async def test_유효하지_않은_gamemode이면_에러가_발생한다(self, mock_supabase):
        with pytest.raises(InvalidParameterError):
            await get_hero_stats(gamemode="arcade")

    async def test_유효하지_않은_region이면_에러가_발생한다(self, mock_supabase):
        with pytest.raises(InvalidParameterError):
            await get_hero_stats(region="africa")

    async def test_유효하지_않은_division이면_에러가_발생한다(self, mock_supabase):
        with pytest.raises(InvalidParameterError):
            await get_hero_stats(competitive_division="challenger")

    async def test_유효하지_않은_order_by이면_에러가_발생한다(self, mock_supabase):
        with pytest.raises(InvalidParameterError):
            await get_hero_stats(order_by="invalid")

    async def test_order_by_콜론이_없으면_에러가_발생한다(self, mock_supabase):
        with pytest.raises(InvalidParameterError):
            await get_hero_stats(order_by="winrate")

    async def test_heroes가_null인_row는_결과에서_제외된다(self, mock_supabase):
        """Supabase 조인 시 role 필터에 의해 heroes가 null인 row가 올 수 있다"""
        mock_supabase.execute.return_value = MagicMock(data=[
            {
                "hero_key": "ana",
                "winrate": 52.5,
                "pickrate": 8.3,
                "synced_at": "2026-02-07T00:00:00",
                "heroes": {"name": "Ana", "portrait": "ana.png", "role": "support"},
            },
            {
                "hero_key": "reinhardt",
                "winrate": 55.0,
                "pickrate": 6.0,
                "synced_at": None,
                "heroes": None,
            },
        ])

        result = await get_hero_stats()

        assert result["total"] == 1
