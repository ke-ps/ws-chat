from app.services.context_service import ContextService
from app.services.semantic_search_service import SemanticSearchService


_RELEVANCE_THRESHOLD = 0.5

_NO_CONTEXT_MESSAGE = (
    "No hay información suficiente en la documentación "
    "para responder a esta pregunta."
)

_PROMPT_TEMPLATE = (
    "Eres un asistente de preguntas y respuestas. "
    "Tu conocimiento está limitado EXCLUSIVAMENTE "
    "a la documentación que se te proporciona a continuación. "
    "NO puedes usar tu conocimiento previo para responder.\n\n"
    "Documentación:\n{context}\n\n"
    "Pregunta: {query}\n\n"
    "Instrucciones estrictas:\n"
    "- Si la documentación contiene información para responder, "
    "responde usando SOLO esa información.\n"
    "- Si la documentación NO contiene la respuesta, "
    "responde exactamente:\n"
    "  \"No hay información suficiente en la documentación "
    "para responder a esta pregunta.\"\n"
    "- NO inventes información.\n"
    "- NO uses tu conocimiento general.\n"
    "- Responde en el mismo idioma de la pregunta."
)


class RAGService:

    def __init__(
        self,
        context_service: ContextService,
        search_service: SemanticSearchService,
    ):
        self._context_service = context_service
        self._search_service = search_service

    def no_context_message(self) -> str:
        return _NO_CONTEXT_MESSAGE

    def has_relevant_context(self, query: str) -> bool:
        top_score = self._search_service.get_top_score(query)
        return top_score >= _RELEVANCE_THRESHOLD

    def generate(self, query: str, top_k: int = 5) -> str:
        context = self._context_service.retrieve_context(query, top_k=top_k)
        if not context:
            return _PROMPT_TEMPLATE.format(
                context="(No se encontró documentación relevante)",
                query=query,
            )
        return _PROMPT_TEMPLATE.format(context=context, query=query)
