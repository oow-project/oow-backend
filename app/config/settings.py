from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    openai_api_key: str
    openai_model: str
    openai_temperature: float
    tavily_api_key: str
    redis_url: str
    allowed_origins: str

    @property
    def cors_origins(self) -> list[str]:
        """ALLOWED_ORIGINS 환경 변수를 파싱하여 CORS 허용 목록을 반환한다."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()
