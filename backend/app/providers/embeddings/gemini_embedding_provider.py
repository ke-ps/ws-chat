from typing import List

from google import genai
from google.genai import types

from app.core.config import settings
from app.providers.embeddings import EmbeddingProvider


class GeminiEmbeddingProvider(EmbeddingProvider):

    def __init__(self) -> None:
        self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self._model = settings.GEMINI_EMBEDDING_MODEL
        self._dimensionality = settings.GEMINI_EMBEDDING_DIMENSIONALITY

    def generate(self, text: str) -> List[float]:
        return self.generate_batch([text])[0]

    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        texts = [t for t in texts if t]
        if not texts:
            return []

        result = self._client.models.embed_content(
            model=self._model,
            contents=texts,
            config=types.EmbedContentConfig(
                outputDimensionality=self._dimensionality,
            ),
        )
        return [e.values for e in result.embeddings]
