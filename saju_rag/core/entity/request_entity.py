from enum import Enum
from pydantic import BaseModel
from saju_rag.core.entity.saju_info import SajuInfo
from saju_rag.core.entity.saju_info import SajuExtractionResult

class SajuRequestType(Enum):
    EXTRACT = "extract"
    ANSWER = "answer"

class SajuRequest(BaseModel):
    """
    api 통신시 사용할 엔티티
    =========================
    - saju_info : 사주 정보
    - extraction_result : 사주 정보 추출 결과
    - user_detail_info : 사용자 상세 정보
    - conversation_history : 대화 기록
    """
    type: SajuRequestType = SajuRequestType.EXTRACT

    successful: bool = False
    follow_up_prompt: str | None = None

    conversation_history: list[dict] | None = None

    saju_info: SajuInfo | None = None
    extraction_result: SajuExtractionResult | None = None
