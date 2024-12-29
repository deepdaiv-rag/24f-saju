from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class Gender(Enum):
    MALE = "M"
    FEMALE = "F"

class SajuInfo(BaseModel):
    """
    사주 정보 모델
    =========================
    추출 목록
    - unse_code : 사주 타입
    - specific_year : 추출 년도
    - specific_month : 추출 월
    - specific_day : 추출 일
    - sl_cal : 음력 양력 여부
    - gender : 성별
    - birth_year : 출생 년도
    - birth_month : 출생 월
    - birth_day : 출생 일
    - birth_hour : 출생 시간
    """
    unse_code: str | None = "A042"
    specific_year: str | None = datetime.now().year
    specific_month: str | None = datetime.now().month
    specific_day: str | None = datetime.now().day
    sl_cal: str | None = None #"S"
    gender: str | None = None #"M"
    birth_year: str | None = None #"1999"
    birth_month: str | None = None #"03"
    birth_day: str | None = None #"30"
    birth_hour: str | None = None #"02"



class SajuExtractionResult(BaseModel):
    """
    사주 정보 추출 결과 모델
    =========================
    추출 목록
    - fortune_period : 운세 기간
    - fortunes : 운세 정보
    - name : 이름
    - saju_table : 사주 테이블
    """
    fortune_period: str | None = None
    fortunes: dict[str, str] | None = None
    saju_table: list[list[str]] | None = None

class UserDetailInfo(BaseModel):
    """
    사용자 상세 정보 모델
    =========================
    """
    detail_info_list: dict[str, str] | None = None
    additional_question: str | None = None