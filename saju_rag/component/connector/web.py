from saju_rag.core.port.connector import ConnectorPort
from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput

class WebConnector(ConnectorPort):
    def connector_info(self) -> str:
        return "WebConnector : 웹 커넥터는 구글, 네이버에서 정보를 조회합니다."

    async def get_document(self, input: ConnectorInput) -> ConnectorOutput:
        raise NotImplementedError
