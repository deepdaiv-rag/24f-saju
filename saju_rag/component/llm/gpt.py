import json
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_fixed

from saju_rag.core.port.saju_information_extraction_port import SajuInformationExtractionPort
from saju_rag.core.port.select_connector_port import SelectConnectorPort
from saju_rag.core.port.connector import ConnectorPort
from saju_rag.core.port.answer_with_connector_info_port import AnswerWithConnectorInfoPort

from saju_rag.core.entity.request_entity import SajuRequest
from saju_rag.core.entity.llm_respone import ExtractionSajuInfo

class ChatGptClient(
    SajuInformationExtractionPort[ExtractionSajuInfo],
    SelectConnectorPort,
    AnswerWithConnectorInfoPort
):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    def extract_saju_information(self, get_saju_info_prompt: str,
                                 conversation_history: list[dict] | None = None) -> ExtractionSajuInfo:
        messages = [{"role": "system", "content": get_saju_info_prompt}]
        if conversation_history:
            messages.extend(conversation_history)

        json_data = self._call_llm("gpt-4o-mini", messages)

        if not json_data.get('successful'):
            return ExtractionSajuInfo(
                successful=False,
                follow_up_prompt=json_data.get('follow_up_prompt')
            )
        else:
            return ExtractionSajuInfo(
                successful=True,
                sl_cal=json_data.get('sl_cal'),
                gender=json_data.get('gender'),
                birth_year=json_data.get('birth_year'),
                birth_month=json_data.get('birth_month'),
                birth_day=json_data.get('birth_day'),
                birth_hour=json_data.get('birth_hour')
            )

    def select_connector(self, query: SajuRequest, prompt: str) -> ConnectorPort:
        raise NotImplementedError
        # messages = [{"role": "system", "content": prompt}]
        # if query.conversation_history:
        #     messages.extend(query.conversation_history)

        # json_data = self._call_llm("gpt-4o-mini", messages)
        # return json_data.get('connector'), json_data.get('query')


    def answer_with_connector_info(self, query: SajuRequest, prompt: str) -> str:
        raise NotImplementedError
        # messages = [{"role": "system", "content": prompt}]
        # if query.conversation_history:
        #     messages.extend(query.conversation_history)

        # json_data = self._call_llm("gpt-4o-mini", messages)
        # return json_data.get('answer')

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    def _call_llm(self, model: str, messages: list[dict]) -> dict:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
