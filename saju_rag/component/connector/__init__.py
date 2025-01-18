from transformers import AutoTokenizer, AutoModel

from .job import JobConnector
from .web import WebConnector
from .psychology import PsychologyConnector
from saju_rag.component.repositories.elasticsearch  import ElasticsearchRepository
from saju_rag.core.port.connector_provider import ConnectorProviderPort
from saju_rag.core.port.connector import ConnectorPort
from openai import OpenAI
from saju_rag.di.config import Settings

class ConnectorProvider(ConnectorProviderPort):
    def __init__(
        self,
        config: Settings , 
        model: AutoModel,
        tokenizer: AutoTokenizer,
        es_repository: ElasticsearchRepository,
        openai_client: OpenAI
    ):
        self.connectors = [
            WebConnector(model, tokenizer),
            # JobConnector(model, tokenizer, es_repository),
            PsychologyConnector(model, tokenizer, es_repository, openai_client(api_key=config.openai_api_key))
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
