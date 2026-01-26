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


class HeroDetailResponse(BaseModel):
    key: str
    name: str
    portrait: str
    role: str
    description: str | None
    location: str | None
    age: int | None
    hitpoints: Hitpoints
    abilities: list[Ability]
    perks: list[Perk]
    counters: list[HeroItem]
    synergies: list[HeroItem]
