from typing import List
from saju_rag.core.port.select_connector_port import SelectConnectorPort
from saju_rag.core.port.answer_with_connector_info_port import AnswerWithConnectorInfoPort
from saju_rag.core.port.connector import ConnectorPort
from saju_rag.core.entity.request_entity import SajuRequest
from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput
from saju_rag.component.connector import get_all_connector_info, select_connector

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
        # 외부 정보를 바탕으로 답변을 생성하는 프롬프트
        with open("saju_rag/core/prompt/generate_answer.prompty", "r") as file:
            self.generate_answer_prompt = file.read()

    async def execute(self, request: SajuRequest) -> str:
        """
        외부 정보를 조회하고 사주 정보와 외부 정보를 바탕으로 답변을 생성합니다.
        """
        #(1) 사용자의 질문에 따라 외부 정보 레파지토리를 선택
        prompt = self.job_selector_prompt + get_all_connector_info()
        job_selector_result = self.select_connector_port.select_connector(request, prompt)
        connector: ConnectorPort = select_connector(job_selector_result.get('connector'))
        query: str = job_selector_result.get('query')
        connector_input = ConnectorInput(query=query, extraction_result=str(request.extraction_result), saju_info=str(request.saju_info))

        #(2) 외부 정보 조회
        documents : List[ConnectorOutput] = await connector.get_document(connector_input)
        prompt = self.generate_answer_prompt + \
            f"사용자 정보 : {str(request.saju_info)}" + \
            f"사주 정보 : {str(request.extraction_result)}" + \
            f"외부 정보 : {str(documents)}"

        response = await self.answer_with_connector_info_port.answer_with_connector_info(prompt, request)
        return response
