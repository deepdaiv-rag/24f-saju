from elasticsearch import AsyncElasticsearch


def get_es_client(
    es_url: str,
    es_username: str,
    es_password: str,
    es_n_connections: int = 10,
) -> AsyncElasticsearch:
    return AsyncElasticsearch(es_url, http_auth=(es_username, es_password))
