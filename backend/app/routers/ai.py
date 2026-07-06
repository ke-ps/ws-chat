from fastapi import APIRouter, Depends, HTTPException
from groq import GroqError
from pydantic import BaseModel

from app.core.dependencies import get_ai_service
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])


class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    response: str


@router.post("/test", response_model=PromptResponse)
def ai_test(
    body: PromptRequest,
    service: AIService = Depends(get_ai_service),
) -> PromptResponse:
    try:
        result = service.ask(body.prompt)
        return PromptResponse(response=result)
    except GroqError:
        raise HTTPException(status_code=502, detail="AI service unavailable")
