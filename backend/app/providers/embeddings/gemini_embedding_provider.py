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
        result = self._client.models.embed_content(
            model=self._model,
            contents=text,
            config=types.EmbedContentConfig(
                outputDimensionality=self._dimensionality,
            ),
        )
        return result.embeddings[0].values
