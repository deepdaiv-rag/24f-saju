import os

from .job import JobConnector
from .web import WebConnector
from .psychology import PsychologyConnector
from .embedding_utils.load_model import load_model, load_tokenizer
from dotenv import load_dotenv

load_dotenv()

model_name = os.getenv("EMBEDDING_MODEL_NAME").replace("`", "")
tokenizer = load_tokenizer(model_name)
model = load_model(model_name)

connectors = [connector(model, tokenizer)
                for connector in (
                    WebConnector,
                    # JobConnector,
                    # PsychologyConnector
                )
             ]

def get_all_connector_info():
    info = [connector.connector_info() for connector in connectors]
    return f"[ {', '.join(info)} ]"

def select_connector(connector_name: str):
    try:
        for connector in connectors:
            if type(connector).__name__ == connector_name:
                return connector
    except Exception as e:
        print(e)
        return None

__all__ = [
    "get_all_connector_info",
    "select_connector"
]
