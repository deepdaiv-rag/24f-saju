from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from saju_rag.component.connector.base import BaseConnector
from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput
import asyncio

# Elasticsearch Repository
class ElasticsearchRepository:
    def __init__(self, es_client):
        self.es_client = es_client

    def search(self, index: str, query: dict, size: int = 10):
        return self.es_client.search(index=index, query=query, size=size)

class JobConnector(BaseConnector):
    def __init__(self, model, tokenizer, es_repository):
        #super().__init__(model=model, tokenizer=tokenizer)
        #self.es_repository = es_repository
        super().__init__()
        self.model=model
        self.tokenizer = tokenizer
        self.es_repository = es_repository

    def connector_info(self) -> str:
        return (
            '{ "connector" : "JobConnector", "description" : "직업 정보 DB에서 정보를 조회합니다." }'
        )

    def get_document(self, input: ConnectorInput) -> ConnectorOutput:
        query_text = input.query
        top_k = input.top_k
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        query_embedding = model.encode(query_text).tolist()

        es_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_embedding},
                },
            },
        }

        response = self.es_repository.search(index="job_postings", query=es_query, size=top_k)

        results = [
            {
                "직무": hit["_source"].get("직무", "N/A"),
                "회사명": hit["_source"].get("회사명", "N/A"),
                "공고명": hit["_source"].get("공고명", "N/A"),
                "URL": hit["_source"].get("URL", "N/A"),
                "score": hit.get("_score", 0),
            }
            for hit in response["hits"]["hits"]
        ]

        metadata = {
            "query": query_text,
            "total_results": response["hits"].get("total", {}).get("value", 0),
            "top_k": top_k,
        }
        
        return ConnectorOutput(
        results=results,          
        similarity=0.85,          
        metadata=metadata         
    )