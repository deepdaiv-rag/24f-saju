from transformers import AutoTokenizer, AutoModel

from .job import JobConnector
from .web import WebConnector
from .psychology import PsychologyConnector
from saju_rag.component.repositories.elasticsearch import ElasticsearchRepository
from saju_rag.core.port.connector_provider import ConnectorProviderPort
from saju_rag.core.port.connector import ConnectorPort
from openai import OpenAI


class ConnectorProvider(ConnectorProviderPort):
    def __init__(
        self,
        model: AutoModel,
        tokenizer: AutoTokenizer,
        es_repository: ElasticsearchRepository,
        openai_client: OpenAI,
    ):
        self.connectors = [
            WebConnector(model=model, tokenizer=tokenizer),
            JobConnector(model=model, tokenizer=tokenizer, es_repository=es_repository),
            PsychologyConnector(
                model=model,
                tokenizer=tokenizer,
                es_repository=es_repository,
                openai_client=openai_client,
            ),
        ]

    # 모든 커넥터의 정보를 반환하는 함수
    def get_all_connector_info(self) -> str:
        info = [connector.connector_info() for connector in self.connectors]
        return f"[ {', '.join(info)} ]"

    # 사용자가 선택한 커넥터를 반환하는 함수
    def select_connector(self, connector_name: str) -> ConnectorPort:
        try:
            for connector in self.connectors:
                if type(connector).__name__ == connector_name:
                    return connector
        except Exception as e:
            print(e)
            return None
