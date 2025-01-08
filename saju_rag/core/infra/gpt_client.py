from openai import OpenAI


def get_gpt_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key)
