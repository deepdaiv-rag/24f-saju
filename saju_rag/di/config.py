from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    log_level: str | None = None
    environment: str | None = None

    openai_api_key: str | None = None
    zenrows_api_key: str | None = None
    shinhan_saju_host: str | None = None

    embedding_model_name: str | None = None

    elasticsearch_url: str | None = None
    elasticsearch_username: str | None = None
    elasticsearch_password: str | None = None
