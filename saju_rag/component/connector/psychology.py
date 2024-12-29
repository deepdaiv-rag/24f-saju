from saju_rag.component.connector.base import BaseConnector
from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput

class PsychologyConnector(BaseConnector):
    def connector_info(self) -> str:
        return "{ \"connector\" : \"PsychologyConnector\", \"description\" : \"심리학 정보 DB에서 정보를 조회합니다.\" }"

    async def get_document(self, input: ConnectorInput) -> ConnectorOutput:
        raise NotImplementedError
