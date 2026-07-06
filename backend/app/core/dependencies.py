from app.providers.ai import GroqProvider
from app.services.ai_service import AIService


def get_ai_service() -> AIService:
    provider = GroqProvider()
    return AIService(provider)
