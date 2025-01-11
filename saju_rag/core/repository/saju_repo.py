from abc import ABC, abstractmethod
from zenrows import ZenRowsClient

from saju_rag.core.entity.saju_info import SajuInfo
from saju_rag.core.entity.saju_info import SajuExtractionResult


class SajuRepository(ABC):
    def __init__(self, zenrows_client: ZenRowsClient):
        self.zenrows_client = zenrows_client

    @abstractmethod
    async def get_by_user_info(self, user_info: SajuInfo) -> SajuExtractionResult:
        """사용자 정보로 사주 정보를 조회합니다."""
        ...
