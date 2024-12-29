from abc import ABC, abstractmethod
from saju_rag.core.entity.document import ConnectorOutput

class AnswerWithConnectorInfoPort(ABC):
    @abstractmethod
    async def generate_response(self, documents: ConnectorOutput):
        """사주 정보와 외부 정보를 바탕으로 답변을 생성합니다."""
        ...
