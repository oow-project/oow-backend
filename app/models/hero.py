from pydantic import BaseModel


class HeroItem(BaseModel):
    key: str
    name: str
    portrait: str
    role: str


class HeroListResponse(BaseModel):
    heroes: list[HeroItem]
    total: int


class Ability(BaseModel):
    name: str
    description: str
    icon: str


class Perk(BaseModel):
    name: str
    description: str
    icon: str
    type: str


class Hitpoints(BaseModel):
    health: int
    armor: int
    shields: int
    total: int


class HeroDetailResponse(HeroItem):
    hitpoints: Hitpoints
    abilities: list[Ability]
    perks: list[Perk]
    counters: list[HeroItem]
    synergies: list[HeroItem]


class HeroStatItem(HeroItem):
    winrate: float | None
    pickrate: float | None


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
