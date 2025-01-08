from bs4 import BeautifulSoup
from requests import Response
from zenrows import ZenRowsClient
from tenacity import retry, stop_after_attempt, wait_fixed

from saju_rag.core.repository.saju_repo import SajuRepository

from saju_rag.core.entity.saju_info import SajuInfo
from saju_rag.core.entity.saju_info import SajuExtractionResult


class ShinhanSajuWebApi(SajuRepository):
    def __init__(self, zenrows_client: ZenRowsClient, host: str):
        """
        Shinhan 사주 웹 API 클라이언트
        ==============================
        - 사주 정보 추출 기능
        - 사주 정보 추출 기능 호출 시 필요한 헤더와 URL 정보를 초기화합니다.
        """
        super().__init__(zenrows_client)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        self.url = host

    async def get_by_user_info(self, user_info: SajuInfo) -> SajuExtractionResult:
        try:
            response = self._request_shinhan_saju(user_info)
        except Exception as e:
            raise e

        soup = BeautifulSoup(response.text, "html.parser")

        # 사주 정보를 담을 딕셔너리
        saju_info = {}

        # 사주 표 데이터 추출
        saju_table = soup.select_one(".saju_table table")
        if saju_table:
            rows = saju_table.find_all("tr")[1:]
            saju_info["saju_table"] = []
            for row in rows:
                columns = row.find_all("td")
                saju_row = [col.text.strip() for col in columns]
                saju_info["saju_table"].append(saju_row)

        # 대운 정보 추출
        fortune_paragraph = soup.select_one(".saju_txt_01")
        if fortune_paragraph:
            saju_info["fortune_period"] = fortune_paragraph.text.strip()

        # 운세별 상세 정보 추출
        result_containers = soup.select(".result_cont")
        saju_info["fortunes"] = {}
        for result in result_containers:
            title = result.select_one(".tit_txt").text.strip()
            content = result.select_one(".content").text.strip()
            saju_info["fortunes"][title] = content

        return SajuExtractionResult(
            fortune_period=saju_info["fortune_period"],
            fortunes=saju_info["fortunes"],
            saju_table=saju_info["saju_table"],
        )

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    def _request_shinhan_saju(self, user_info: SajuInfo) -> Response:
        input_data = {
            "unse_code": user_info.unse_code,
            "specific_year": user_info.specific_year,
            "specific_month": user_info.specific_month,
            "specific_day": user_info.specific_day,
            "user_gender": user_info.gender,
            "user_birth_year": user_info.birth_year,
            "gender": user_info.gender,
            "sl_cal": user_info.sl_cal,
            "birth_year": user_info.birth_year,
            "birth_month": user_info.birth_month,
            "birth_day": user_info.birth_day,
            "birth_hour": user_info.birth_hour,
        }

        try:
            response = self.zenrows_client.post(
                self.url, headers=self.headers, data=input_data
            )
            response.raise_for_status()
            return response
        except Exception as e:
            raise e
