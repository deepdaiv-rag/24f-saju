from typing import List, Tuple
from abc import abstractmethod
from saju_rag.core.port.connector import ConnectorPort
from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput
from transformers import AutoModel, AutoTokenizer
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class BaseConnector(ConnectorPort):
    def __init__(self, embedding_model, embedding_tokenizer):
        self.embedding_model = embedding_model
        self.embedding_tokenizer = embedding_tokenizer

    def compute_embedding(self, text: str):
        inputs = self.embedding_tokenizer(
            text, return_tensors="pt", padding=True, truncation=True
        )
        with torch.no_grad():
            outputs = self.embedding_model(**inputs)

        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.squeeze(0)

    def chunk_text(self, text: str, chunk_size: int = 1024) -> List[str]:
        """주어진 텍스트를 청크로 나누는 함수."""
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    def find_similar_chunks(
        self, query: str, text_list: List[str], top_n: int = 5, chunk_size: int = 1024
    ) -> List[Tuple[str, float]]:
        """쿼리와 가장 유사한 청크를 찾는 함수."""
        # 각 텍스트를 청크로 나누기
        chunks = [
            self.chunk_text(text, chunk_size=chunk_size) for text in text_list
        ]  # 각 문서별로 청크 나누기
        chunks = [chunk for sublist in chunks for chunk in sublist]  # 리스트로 합치기

        # 쿼리 임베딩 계산
        query_embedding = self.compute_embedding(query).reshape(1, -1)

        # 청크 임베딩 계산
        chunk_embeddings = np.array(
            [self.compute_embedding(chunk) for chunk in chunks]
        ).reshape(-1, self.embedding_model.config.hidden_size)

        # 유사도 계산
        similarities = cosine_similarity(query_embedding, chunk_embeddings).flatten()

        # 가장 유사한 청크 선택
        top_indices = similarities.argsort()[-top_n:][::-1]
        return [(chunks[i], similarities[i]) for i in top_indices]  # 청크 텍스트와 유사도 반환

    @abstractmethod
    def connector_info(self) -> str:
        ...

    @abstractmethod
    async def get_document(self, input: ConnectorInput) -> List[ConnectorOutput]:
        ...
