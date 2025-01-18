from typing import Any, Dict, List, Optional
from venv import logger
from elasticsearch import AsyncElasticsearch
from sentence_transformers import SentenceTransformer
from saju_rag.core.entity.document import ConnectorOutput

class ElasticsearchRepository:
    def __init__(self, es_client: AsyncElasticsearch, embedding_model: Optional[SentenceTransformer] = None):
        self.es_client = es_client
        self.embedding_model = embedding_model or SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    async def search_documents(
        self, 
        search_query: str, 
        index_name: str, 
        use_semantic_search: bool = True,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 5,
        sources: Optional[List[str]] = None
    ):
        """
        하이브리드 검색 수행 (시맨틱 검색 + 키워드 기반 필터링)
        
        Args:
            search_query (str): 검색할 텍스트
            index_name (str): 검색할 인덱스 이름
            use_semantic_search (bool): 시맨틱 검색 사용 여부
            filters (Optional[Dict[str, Any]]): 필터링 조건 (예: {"relation": "work", "tags": ["stress"]})
            top_k (int): 반환할 결과 수
            sources (Optional[List[str]]): 반환받을 필드 리스트
        """
        try:
            # 기본 bool 쿼리 구성
            query = {
                "bool": {
                    "must": [],
                    "should": []
                }
            }

            # 텍스트 매칭 쿼리 추가
            query["bool"]["should"].append({
                "match": {
                    "question": search_query
                }
            })

            # 시맨틱 검색 사용 시 임베딩 생성 및 쿼리 추가
            if use_semantic_search:
                query_embedding = self.embedding_model.encode(search_query).tolist()
                query["bool"]["should"].append({
                    "script_score": {
                        "query": {"match_all": {}},
                        "script": {
                            "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                            "params": {"query_vector": query_embedding}
                        }
                    }
                })

            # 필터 조건 추가
            if filters:
                for field, value in filters.items():
                    if isinstance(value, list):
                        query["bool"]["must"].append({
                            "terms": {
                                field: value
                            }
                        })
                    else:
                        query["bool"]["must"].append({
                            "term": {
                                field: value
                            }
                        })

            # 검색 파라미터 구성
            search_params = {
                "index": index_name,
                "query": query,
                "size": top_k
            }
            
            if sources:
                search_params["_source"] = sources

            response = await self.es_client.search(**search_params)
            return response["hits"]["hits"]

        except Exception as e:
            logger.error(f"Elasticsearch 검색 중 오류 발생: {str(e)}")
            print(f"검색 실패: {str(e)}")
            return []

    def parse_response(self, response: List[Dict[str, Any]], target_fields : List[str]) -> ConnectorOutput:
        """
        Elasticsearch 검색 결과를 ConnectorOutput으로 변환
        """
        if not response:
            return [ConnectorOutput(content="", similarity=0.0)]
        
        results = []
        content = ""
        for hit in response:
            # 질문과 답변을 합쳐서 content 생성
            if target_fields : 
                for field in target_fields: 
                    content += f"{field}: {hit['_source'][field]}\n"
            else : 
                content =  f"{hit['_source']}\n"
                
            # _score를 similarity로 사용
            similarity = float(hit['_score'])
            
            results.append(
                ConnectorOutput(
                    content=content,
                    similarity=similarity
                )
            )
        return results
