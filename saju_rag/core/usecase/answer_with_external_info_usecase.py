from saju_rag.core.port.select_connector_port import SelectConnectorPort
from saju_rag.core.port.answer_with_connector_info_port import AnswerWithConnectorInfoPort
from saju_rag.core.port.connector import ConnectorPort
from saju_rag.core.entity.request_entity import SajuRequest
from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput

class AnswerWithExternalInfoUsecase:
    def __init__(self, 
                 select_connector_port: SelectConnectorPort, 
                 answer_with_connector_info_port: AnswerWithConnectorInfoPort
    ):
        # 사용자의 질문에 따라 외부 정보 레파지토리를 선택하는 모듈
        self.select_connector_port = select_connector_port
        # 외부 정보를 바탕으로 답변을 생성하는 llm 모듈
        self.answer_with_connector_info_port = answer_with_connector_info_port
        # 외부 정보 조회를 위한 커넥터 선정하는 프롬프트
        with open("saju_rag/core/prompt/job_selector.prompty", "r") as file:
            self.job_selector_prompt = file.read()

    async def execute(self, request: SajuRequest):
        """
        외부 정보를 조회하고 사주 정보와 외부 정보를 바탕으로 답변을 생성합니다.
        """
        #(1) 사용자의 질문에 따라 외부 정보 레파지토리를 선택
        job_selector_result = self.select_connector_port.select_connector(request, self.job_selector_prompt)
        connector: ConnectorPort = job_selector_result.get('connector')
        query: str = job_selector_result.get('query')

        #(2) 외부 정보 조회
        connector_input = ConnectorInput(query=query, user_info=str(request.user_detail_info), saju_info=str(request.saju_info))
        documents : ConnectorOutput = await connector.get_document(connector_input)

        #(3) 외부 정보를 바탕으로 답변 생성
        response = await self.answer_with_connector_info_port.generate_response(documents)
        return response