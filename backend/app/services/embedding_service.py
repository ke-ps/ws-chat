from typing import List

from app.providers.embeddings import EmbeddingProvider


class EmbeddingService:

    def __init__(self, provider: EmbeddingProvider) -> None:
        self._provider = provider

    def generate(self, text: str) -> List[float]:
        if not text:
            return []
        return self._provider.generate(text)

    def generate_batch(self, chunks: List[str]) -> List[List[float]]:
        return [self.generate(chunk) for chunk in chunks if chunk]
