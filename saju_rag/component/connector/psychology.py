import json
import os
from saju_rag.component.connector.base import BaseConnector
from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput
from typing import List, Dict, Any

class PsychologyConnector(BaseConnector):
    def __init__(self, model, tokenizer, es_repository, openai_client):
        super().__init__(model, tokenizer)
        self.es_repository = es_repository
        self.openai_client = openai_client
        self.index_name = "counseling_data_total"
        
    def connector_info(self) -> str:
        return '{ "connector" : "PsychologyConnector", "description" : "심리학 정보 DB에서 정보를 조회합니다." }'

    def extract_relation(self, query: str) -> str:
        """ query에서 관계 , tag 추출 """
        try :
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"""사용자 질의를 분석하여 관계 유형과 태그를 추출해주세요.
                    
                    사용자 질의 : {query}
                    """
                }],
                functions=[{
                    "name": "extract_tags",
                    "parameters": EXTRACT_TAG_JSON_SCHEMA
                }],
                function_call={"name": "extract_tags"}
            )
            result = json.loads(response.choices[0].message.function_call.arguments)
            return result["relation"], result["tag"]
        except Exception as e:
            print(f"Error in get_tags: {str(e)}")
            return {"relation": "other", "tag": ["other"]}

    async def get_document(self, input: ConnectorInput) -> List[ConnectorOutput]:
        # 관계 유형 추출
        relation_type , tag = self.extract_relation(input.query)

        # 유사한 문서 조회
        similar_documents = self.es_repository.search_documents(input.query, self.index_name, use_semantic_search=True, filters={"relation": relation_type, "tag": tag})
        # 조회한 문서를 ConnectorOutput으로 변환
        results = self.es_repository.parse_response(similar_documents, target_fields=["question", "answer"])

        return results


EXTRACT_TAG_JSON_SCHEMA ={
            "type": "object",
            "properties": {
                "relation": {
                    "type": "string",
                    "enum": ["work", "family", "school", "mental_health", "interpersonal", 
                            "grief", "career", "love", "marriage", "other"]
                },
                "tag": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["stress", "anxiety", "depression", "burnout", "conflict",
                                "adaptation", "communication", "self_esteem", 
                                "worklife_balance", "relationship", "other"]
                    }
                }
            }
        }