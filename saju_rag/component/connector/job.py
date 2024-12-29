from saju_rag.core.port.connector import ConnectorPort
from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput

class JobConnector(ConnectorPort):
    def connector_info(self) -> str:
        return "{ \"connector\" : \"JobConnector\", \"description\" : \"직업 정보 DB에서 정보를 조회합니다.\" }"

    async def get_document(self, input: ConnectorInput) -> ConnectorOutput:
        raise NotImplementedError
