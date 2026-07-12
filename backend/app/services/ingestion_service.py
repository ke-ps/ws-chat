from typing import List

from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.models.document import Document
from app.repositories.chunk_repository import ChunkRepository
from app.services.document_service import DocumentService
from app.services.pdf_extraction_service import PDFExtractionService, PDFExtractionError
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService


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

        db_chunks = []
        for i, chunk_text in enumerate(chunks):
            embedding = self.embedding_service.generate(chunk_text)
            chunk = Chunk(
                document_id=document_id,
                chunk_index=i,
                content=chunk_text,
                embedding=embedding,
            )
            db_chunks.append(chunk)

        return self.chunk_repository.create_all(db_chunks)
