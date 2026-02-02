from typing import Literal

from pydantic import BaseModel


class HeroItem(BaseModel):
    key: str
    name: str
    portrait: str
    role: Literal["tank", "damage", "support"]


class HeroListResponse(BaseModel):
    heroes: list[HeroItem]
    total: int


class Ability(BaseModel):
    name: str
    description: str
    icon: str
    ability_type: Literal["skill", "perk_major", "perk_minor"]


class Hitpoints(BaseModel):
    health: int
    armor: int
    shields: int
    total: int


class HeroDetailResponse(HeroItem):
    hitpoints: Hitpoints
    abilities: dict[str, list[Ability]]
    counters: list[HeroItem]
    synergies: list[HeroItem]


class HeroStatItem(HeroItem):
    winrate: float
    pickrate: float


class StatsFilters(BaseModel):
    platform: str
    gamemode: str
    region: str
    competitive_division: str
    role: str


class StatsResponse(BaseModel):
    stats: list[HeroStatItem]
    filters: StatsFilters
    total: int
    synced_at: str | None
