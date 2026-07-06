from groq import Groq

from app.core.config import settings
from app.providers.ai import AIProvider


class GroqProvider(AIProvider):
    def __init__(self) -> None:
        self._client = Groq(api_key=settings.GROQ_API_KEY)
        self._model = settings.GROQ_MODEL

    def ask(self, prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
