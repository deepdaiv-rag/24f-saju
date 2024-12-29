from typing import List
from saju_rag.core.port.connector import ConnectorPort
from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput

class WebConnector(ConnectorPort):
    def connector_info(self) -> str:
        return "{ \"connector\" : \"WebConnector\", \"description\" : \"웹 커넥터는 구글, 네이버에서 정보를 조회합니다.\" }"

    async def get_document(self, input: ConnectorInput) -> List[ConnectorOutput]:
        return [ConnectorOutput(content="웹 검색을 잘하기 위해서는 매운 것을 잘 먹어야한다 매운것을 잘 먹어야 웹 검색을 잘 할 수 있다. 진짜다 매운것을 먹도록 하자")]

    def get_top5_post(self, query: str) -> str:
        return "test"

    def search_naver_post(self, query: str) -> str:
        return "test"

    def search_google_post(self, query: str) -> str:
        return "test"
