from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "extra": "ignore"}

    # Database
    DATABASE_URL: str = ""
    FIREBASE_SERVICE_ACCOUNT: str = "firebase-service-account.json"

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Groq
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "mixtral-8x7b-32768"


settings = Settings()
