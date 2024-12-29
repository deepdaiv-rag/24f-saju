from saju_rag.core.entity.saju_info import SajuInfo

class ExtractionSajuInfo(SajuInfo):
    """
    사주 정보 추출 결과 모델
    =========================
    추출 목록
    - successful : 성공 여부
    - follow_up_prompt : 추가 정보 요청 프롬프트
    """
    successful: bool
    follow_up_prompt: str | None = None
