from pydantic import BaseModel


class HeroItem(BaseModel):
    key: str
    name: str
    portrait: str
    role: str


class HeroListResponse(BaseModel):
    heroes: list[HeroItem]
    total: int
