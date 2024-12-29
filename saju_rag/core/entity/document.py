from enum import Enum
from pydantic import BaseModel

class ConnectorInput(BaseModel):
    """
    커넥터의 입력 데이터를 정의한 엔티티
    """
    query: str
    user_info : str
    saju_info : str

class ConnectorOutput(ConnectorInput):
    """
    커넥터의 출력 데이터를 정의한 엔티티
    """
    document: list[str]