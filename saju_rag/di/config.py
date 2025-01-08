from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    log_level: str | None = None
    environment: str | None = None
    openai_api_key: str | None = None
    zenrows_api_key: str | None = None
    shinhan_saju_host: str | None = None
