from app.providers.ai import AIProvider


class AIService:
    def __init__(self, provider: AIProvider) -> None:
        self._provider: AIProvider = provider

    def ask(self, prompt: str) -> str:
        return self._provider.ask(prompt)
