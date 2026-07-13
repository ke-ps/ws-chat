from typing import List

from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.models.document import Document
from app.repositories.chunk_repository import ChunkRepository
from app.services.document_service import DocumentService
from app.services.pdf_extraction_service import PDFExtractionService, PDFExtractionError
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService


EMBEDDING_BATCH_SIZE = 100


class IngestionService:

    def __init__(self, db: Session, embedding_service: EmbeddingService):
        self.db = db
        self.document_service = DocumentService(db)
        self.pdf_extraction_service = PDFExtractionService(db)
        self.chunking_service = ChunkingService()
        self.embedding_service = embedding_service
        self.chunk_repository = ChunkRepository(db)

    def ingest_document(self, document_id: int) -> List[Chunk]:
        document = self.document_service.get_document_by_id(document_id)
        if not document:
            raise ValueError(f"Document {document_id} not found")

        full_text = self.pdf_extraction_service.extract_text(document_id)
        chunks = self.chunking_service.chunk_text(full_text)

        self.chunk_repository.delete_by_document(document_id)

        all_chunks: List[Chunk] = []
        batch_size = EMBEDDING_BATCH_SIZE
        for batch_start in range(0, len(chunks), batch_size):
            batch = chunks[batch_start:batch_start + batch_size]
            embeddings = self.embedding_service.generate_batch(batch)
            batch_chunks = []
            for offset, (chunk_text, embedding) in enumerate(zip(batch, embeddings)):
                chunk = Chunk(
                    document_id=document_id,
                    chunk_index=batch_start + offset,
                    content=chunk_text,
                    embedding=embedding,
                )
                batch_chunks.append(chunk)
            all_chunks.extend(self.chunk_repository.create_all(batch_chunks))

        return all_chunks
