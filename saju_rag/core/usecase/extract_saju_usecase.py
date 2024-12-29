from saju_rag.core.port.saju_information_extraction_port import SajuInformationExtractionPort
from saju_rag.core.entity.llm_respone import ExtractionSajuInfo
from saju_rag.core.repository.saju_repo import SajuRepository
from saju_rag.core.entity.request_entity import SajuRequest

class ExtractSajuUseCase:
    def __init__(
        self,
        saju_extractor: SajuInformationExtractionPort[ExtractionSajuInfo],
        saju_repository: SajuRepository
    ):
        # 사용자와 대화를 하며 생년월일 등 개인 정보를 추출하는 llm 모델
        self._saju_extractor = saju_extractor
        # 생년월일 등 개인 정보에 따른 사주 정보를 저장하는 레포지토리
        self._saju_repository = saju_repository
        # 사주 정보 추출을 위한 프롬프트
        with open("saju_rag/core/prompt/extract_info.prompty", "r") as file:
            self._extract_info_prompt = file.read()

    async def execute(self, request: SajuRequest) -> SajuRequest:
        """
        사용자와의 대화 기록을 바탕으로 사주 정보를 추출 혹은 추출을 위한 질문을 생성합니다.
        """
        #(1) 사주 정보 추출
        saju_info = self._saju_extractor.extract_saju_information(self._extract_info_prompt, request.conversation_history)

        #(2) 추출 가능 여부 확인
        if saju_info.successful:
            #(3-1) 추출된 사주 정보를 결과 값에 저장
            result = await self._saju_repository.get_by_user_info(saju_info)
            request.saju_info = saju_info
            request.extraction_result = result
            request.successful = True
        else:
            #(3-2) 추출 불가능 시 질문 생성
            request.successful = False
            request.follow_up_prompt = saju_info.follow_up_prompt

        return request