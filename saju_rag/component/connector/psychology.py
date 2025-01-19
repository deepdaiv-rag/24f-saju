import json
from logging import getLogger

from saju_rag.component.repositories.elasticsearch import ElasticsearchRepository
from transformers import AutoTokenizer, AutoModel
from openai import OpenAI

from saju_rag.component.connector.base import BaseConnector
from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput
from typing import List

logger = getLogger(__name__)

EXTRACT_TAG_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "relation": {
            "type": "string",
            "enum": [
                "work",
                "family",
                "school",
                "mental_health",
                "interpersonal",
                "grief",
                "career",
                "love",
                "marriage",
                "leadership",
                "negotiation",
                "management",
                "other",
            ],
        },
        "tag": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "stress",
                    "anxiety",
                    "depression",
                    "burnout",
                    "conflict",
                    "adaptation",
                    "communication",
                    "self_esteem",
                    "worklife_balance",
                    "relationship",
                    "criticism_handling",
                    "appreciation",
                    "influence",
                    "motivation",
                    "leadership_skills",
                    "persuasion",
                    "conflict_resolution",
                    "active_listening",
                    "emotional_intelligence",
                    "positive_attitude",
                    "other",
                ],
            },
        },
    },
}

CARNEGIE_VALID_RELATIONS = {
    "career",
    "family",
    "interpersonal",
    "leadership",
    "love",
    "management",
    "other",
    "school",
    "work",
}


class PsychologyConnector(BaseConnector):
    def __init__(
        self,
        model: AutoModel,
        tokenizer: AutoTokenizer,
        es_repository: ElasticsearchRepository,
        openai_client: OpenAI,
    ):
        super().__init__(model, tokenizer)
        self.es_repository = es_repository
        self.openai_client = openai_client
        self.counseling_data_index_name = "counseling_data_total"
        self.psychology_book_index_name = "psychology_book"
        self.model_name = "gpt-4o-mini"

    def connector_info(self) -> str:
        return '{ "connector" : "PsychologyConnector", "description" : "상담 자료와, 인간관계 대응법 DB에서 정보를 조회합니다." }'

    def extract_relation(self, query: str) -> str:
        """query에서 관계 , tag 추출"""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": f"""사용자 질의를 분석하여 관계 유형과 태그를 추출해주세요.

                    사용자 질의 : {query}
                    """,
                    }
                ],
                functions=[
                    {"name": "extract_tags", "parameters": EXTRACT_TAG_JSON_SCHEMA}
                ],
                function_call={"name": "extract_tags"},
            )
            result = json.loads(response.choices[0].message.function_call.arguments)
            return result["relation"], result["tag"]
        except Exception as e:
            print(f"Error in get_tags: {str(e)}")
            return {"relation": "other", "tag": ["other"]}

    async def get_document(self, input: ConnectorInput) -> List[ConnectorOutput]:
        # 관계 유형 추출
        relation_type, tag = self.extract_relation(input.query)
        input_embedding = self.compute_embedding(input.query)

        # 유사한 문서 조회
        # GPT 카운셀링 검색
        similar_documents1 = await self.es_repository.search_documents(
            embedding=input_embedding,
            index_name=self.counseling_data_index_name,
            use_semantic_search=True,
            filters={"relation": relation_type, "tag": tag},
        )
        # 카네기 도서 검색
        # 고유한 relation 값 집합
        # relation_type이 유효한 경우에만 필터 추가
        carnegie_filters = {}
        if relation_type in CARNEGIE_VALID_RELATIONS:
            carnegie_filters["relation"] = relation_type
        # 카네기 도서 검색
        similar_documents2 = await self.es_repository.search_documents(
            embedding=input_embedding,
            index_name=self.psychology_book_index_name,
            use_semantic_search=True,
            filters=carnegie_filters,
        )
        # 조회한 문서를 ConnectorOutput으로 변환
        results1 = self.es_repository.parse_response(
            response=similar_documents1, target_fields=["question", "answer"]
        )
        results2 = self.es_repository.parse_response(
            response=similar_documents2, target_fields=["text", "chapter_name"]
        )

        return results1 + results2
