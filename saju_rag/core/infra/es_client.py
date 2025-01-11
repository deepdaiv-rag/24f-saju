from elasticsearch import AsyncElasticsearch


def get_es_client(
    es_url: str,
    es_username: str,
    es_password: str,
    es_n_connections: int = 10,
) -> AsyncElasticsearch:
    return AsyncElasticsearch(
        hosts=[es_url],
        basic_auth=(es_username, es_password),
        connections_per_node=es_n_connections,
    )
