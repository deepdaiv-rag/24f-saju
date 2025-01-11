from typing import List
from abc import ABC, abstractmethod

from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput


class ConnectorPort(ABC):
    @abstractmethod
    def connector_info(self) -> str:
        """프롬프트에 들어갈 커넥터의 설명문을 str로 반환합니다."""
        ...

    @abstractmethod
    async def get_document(self, input: ConnectorInput) -> List[ConnectorOutput]:
        """사용자의 질문에 따라 외부 정보를 조회합니다."""
        ...
