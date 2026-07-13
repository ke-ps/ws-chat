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
        chunks = [c for c in chunks if c]
        if not chunks:
            return []
        if hasattr(self._provider, 'generate_batch'):
            return self._provider.generate_batch(chunks)
        return [self._provider.generate(c) for c in chunks]
