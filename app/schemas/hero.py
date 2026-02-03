from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class HeroItem(BaseModel):
    key: str
    name: str
    portrait: str
    role: Literal["tank", "damage", "support"]


class HeroListResponse(BaseModel):
    heroes: list[HeroItem]
    total: int


class Ability(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    description: str
    icon: str
    ability_type: Literal["skill", "perk_major", "perk_minor"] = Field(
        serialization_alias="abilityType"
    )


class GroupedAbilities(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    skill: list[Ability] = []
    perk_major: list[Ability] = Field(default=[], serialization_alias="perkMajor")
    perk_minor: list[Ability] = Field(default=[], serialization_alias="perkMinor")


class Hitpoints(BaseModel):
    health: int
    armor: int
    shields: int
    total: int


class HeroDetailResponse(HeroItem):
    hitpoints: Hitpoints
    abilities: GroupedAbilities
    counters: list[HeroItem]
    synergies: list[HeroItem]


class HeroStatItem(HeroItem):
    winrate: float
    pickrate: float


class StatsFilters(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    platform: str
    gamemode: str
    region: str
    competitive_division: str = Field(serialization_alias="competitiveDivision")
    role: str


class StatsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    stats: list[HeroStatItem]
    filters: StatsFilters
    total: int
    synced_at: str | None = Field(default=None, serialization_alias="syncedAt")
