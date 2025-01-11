from abc import ABC, abstractmethod

from saju_rag.core.entity.request_entity import SajuRequest


class SelectConnectorPort(ABC):
    @abstractmethod
    def select_connector(self, query: SajuRequest, prompt: str) -> dict:
        """사용자의 질문에 따라 외부 정보 레파지토리를 선택합니다."""
        ...
