from typing import List

from saju_rag.component.connector.base import BaseConnector
from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput
from transformers import AutoTokenizer, AutoModel
from saju_rag.component.repositories.elasticsearch import ElasticsearchRepository


class JobConnector(BaseConnector):
    def __init__(
        self,
        model: AutoModel,
        tokenizer: AutoTokenizer,
        es_repository: ElasticsearchRepository,
    ):
        super().__init__(model, tokenizer)
        self.es_repository = es_repository
        self.index_name = "careernet_job"

    def connector_info(self) -> str:
        return (
            '{ "connector" : "JobConnector", "description" : "직업 정보 DB에서 정보를 조회합니다." }'
        )

    async def get_document(self, input: ConnectorInput) -> ConnectorOutput:
        job_info = self.parse_job_info(input.extraction_result)

        embedding = self.compute_embedding(job_info)

        documents = await self.es_repository.search_documents(
            embedding=embedding,
            index_name=self.index_name,
            use_semantic_search=True,
            filters=None,
        )

        results = self.es_repository.parse_response(
            response=documents, target_fields=["text"]
        )

        return results

    def parse_job_info(self, extraction_result: str):
        # '직업운' 정보를 문자열에서 직접 추출
        try:
            # '직업운' 키워드로 시작하는 부분을 찾습니다.
            start_index = extraction_result.find("'직업운'")
            if start_index == -1:
                print("직업운 정보가 없습니다.")
                return None

            # '직업운' 이후의 내용을 추출합니다.
            job_info_start = extraction_result[start_index:]
            # 다음 운세 정보가 시작되기 전까지의 내용을 추출합니다.
            end_index = job_info_start.find("}")  # 다음 운세 정보의 시작을 찾습니다.
            if end_index == -1:
                job_info = job_info_start
            else:
                job_info = job_info_start[:end_index]
            job_info = job_info.replace("'직업운': '", "")
            job_info = job_info.replace("'", "")
            return job_info
        except Exception as e:
            print(f"오류 발생: {e}")
            return None
