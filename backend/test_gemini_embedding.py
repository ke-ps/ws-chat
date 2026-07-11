from google import genai
from google.genai import types

from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

result = client.models.embed_content(
    model="gemini-embedding-2",
    contents="Hola mundo",
    config=types.EmbedContentConfig(
        output_dimensionality=768
    )
)

print(len(result.embeddings[0].values))