from typing import List
from saju_rag.core.entity.saju_info import SajuInfo, UserDetailInfo

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


class ExtractionQuestionList(UserDetailInfo):
    """
    사주 관련 질문 추출 결과 모델
    =========================
    추출 목록
    - successful : 성공 여부
    - follow_up_prompt : 추가 정보 요청 프롬프트
    - question_list : 질문 리스트
    """
    successful: bool
    follow_up_prompt: str | None = None
