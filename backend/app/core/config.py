from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "extra": "ignore"}

    # Database
    DATABASE_URL: str = ""
    FIREBASE_SERVICE_ACCOUNT: str = "firebase-service-account.json"

    # OpenAI
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Embeddings
    GEMINI_API_KEY: str = ""
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-2"
    GEMINI_EMBEDDING_DIMENSIONALITY: int = 768

    # Groq
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "mixtral-8x7b-32768"


settings = Settings()
