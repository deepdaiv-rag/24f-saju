from abc import ABC, abstractmethod

from saju_rag.core.port.connector import ConnectorPort


class ConnectorProviderPort(ABC):
    @abstractmethod
    def get_all_connector_info(self) -> str:
        """모든 커넥터의 정보를 반환"""
        ...

    @abstractmethod
    def select_connector(self, connector_name: str) -> ConnectorPort:
        """커넥터 이름을 받아 커넥터를 반환"""
        ...
