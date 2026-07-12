from app.services.semantic_search_service import SemanticSearchService


class ContextService:

    def __init__(self, search_service: SemanticSearchService):
        self._search_service = search_service

    def retrieve_context(self, query: str, top_k: int = 5) -> str:
        results = self._search_service.search(query, top_k=top_k)
        if not results:
            return ""

        parts: list[str] = []
        for i, r in enumerate(results, 1):
            parts.append(
                f"[Documento {r.chunk.document_id} | Fragmento {r.chunk.chunk_index}]\n{r.chunk.content}"
            )

        return "\n\n".join(parts)
