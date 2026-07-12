from app.services.context_service import ContextService


_PROMPT_TEMPLATE = (
    "Eres un asistente especializado en responder preguntas "
    "basándote exclusivamente en la documentación proporcionada.\n\n"
    "Documentación:\n{context}\n\n"
    "Pregunta: {query}\n\n"
    "Instrucciones:\n"
    "- Responde únicamente con la información de la documentación.\n"
    "- Si la documentación no contiene la respuesta, "
    "indica que no hay información suficiente.\n"
    "- No utilices conocimiento general.\n"
    "- Responde en el mismo idioma de la pregunta."
)


class RAGService:

    def __init__(self, context_service: ContextService):
        self._context_service = context_service

    def generate(self, query: str, top_k: int = 5) -> str:
        context = self._context_service.retrieve_context(query, top_k=top_k)
        if not context:
            return _PROMPT_TEMPLATE.format(
                context="(No se encontró documentación relevante)",
                query=query,
            )
        return _PROMPT_TEMPLATE.format(context=context, query=query)
