from functools import lru_cache
from zenrows import ZenRowsClient


@lru_cache
def get_zenrows_client(api_key: str, retries: int = 3) -> ZenRowsClient:
    return ZenRowsClient(api_key, retries=retries)
