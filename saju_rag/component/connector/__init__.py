from transformers import AutoTokenizer, AutoModel

from .job import JobConnector
from .web import WebConnector
from .psychology import PsychologyConnector
from saju_rag.component.repositories.elasticsearch import ElasticsearchRepository
from saju_rag.core.port.connector_provider import ConnectorProviderPort
from saju_rag.core.port.connector import ConnectorPort


class ConnectorProvider(ConnectorProviderPort):
    def __init__(
        self,
        model: AutoModel,
        tokenizer: AutoTokenizer,
        es_repository: ElasticsearchRepository,
    ):
        self.connectors = [
            WebConnector(model, tokenizer),
            # JobConnector(model, tokenizer, es_repository),
            # PsychologyConnector(model, tokenizer, es_repository)
        ]

    def get_all_connector_info(self) -> str:
        info = [connector.connector_info() for connector in self.connectors]
        return f"[ {', '.join(info)} ]"

    def select_connector(self, connector_name: str) -> ConnectorPort:
        try:
            for connector in self.connectors:
                if type(connector).__name__ == connector_name:
                    return connector
        except Exception as e:
            print(e)
            return None
