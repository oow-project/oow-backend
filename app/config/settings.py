from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    openai_api_key: str
    openai_model: str
    openai_temperature: float
    tavily_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
