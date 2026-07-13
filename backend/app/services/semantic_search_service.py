from typing import List, Tuple

from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.repositories.chunk_repository import ChunkRepository
from app.services.embedding_service import EmbeddingService


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


class SemanticSearchResult:
    def __init__(self, chunk: Chunk, score: float):
        self.chunk = chunk
        self.score = score


class SemanticSearchService:

    def __init__(self, db: Session, embedding_service: EmbeddingService):
        self.chunk_repository = ChunkRepository(db)
        self.embedding_service = embedding_service

    def get_top_score(self, query: str) -> float:
        query_embedding = self.embedding_service.generate(query)
        if not query_embedding:
            return 0.0

        chunks = self.chunk_repository.find_all_with_embedding()
        if not chunks:
            return 0.0

        best = 0.0
        for chunk in chunks:
            if not chunk.embedding:
                continue
            score = _cosine_similarity(query_embedding, chunk.embedding)
            if score > best:
                best = score
        return best

    def search(self, query: str, top_k: int = 5) -> List[SemanticSearchResult]:
        query_embedding = self.embedding_service.generate(query)
        if not query_embedding:
            return []

        chunks = self.chunk_repository.find_all_with_embedding()

        scored: List[Tuple[float, Chunk]] = []
        for chunk in chunks:
            if not chunk.embedding:
                continue
            score = _cosine_similarity(query_embedding, chunk.embedding)
            scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [
            SemanticSearchResult(chunk=chunk, score=score)
            for score, chunk in scored[:top_k]
        ]
