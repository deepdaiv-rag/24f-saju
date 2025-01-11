from openai import OpenAI
from logging import getLogger

logger = getLogger(__name__)


def get_gpt_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key)
