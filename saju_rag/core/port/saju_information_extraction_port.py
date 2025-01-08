from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ExtractionResult = TypeVar("ExtractionResult")


class SajuInformationExtractionPort(ABC, Generic[ExtractionResult]):
    @abstractmethod
    async def extract_saju_information(
        self, get_saju_info_prompt: str, conversation_history: list[dict] | None = None
    ) -> ExtractionResult | None:
        """대화 기록을 바탕으로 사주 정보를 추출합니다."""
        ...
