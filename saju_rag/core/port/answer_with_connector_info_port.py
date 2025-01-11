from abc import ABC, abstractmethod

from saju_rag.core.entity.request_entity import SajuRequest


class AnswerWithConnectorInfoPort(ABC):
    @abstractmethod
    async def answer_with_connector_info(
        self, prompt: str, request: SajuRequest
    ) -> str:
        """사주 정보와 외부 정보를 바탕으로 답변을 생성합니다."""
        ...
