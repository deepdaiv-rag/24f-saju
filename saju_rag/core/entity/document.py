from enum import Enum
from pydantic import BaseModel


class ConnectorInput(BaseModel):
    """
    커넥터의 입력 데이터를 정의한 엔티티
    """

    query: str
    extraction_result: str
    saju_info: str
    conversation_history: list[dict] | None = None


class ConnectorOutput(BaseModel):
    """
    커넥터의 출력 데이터를 정의한 엔티티
    """

    content: str
    similarity: float
