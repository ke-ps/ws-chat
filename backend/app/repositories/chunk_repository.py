from sqlalchemy.orm import Session
from app.models.chunk import Chunk
from typing import List


class ChunkRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_document(self, document_id: int) -> List[Chunk]:
        return self.db.query(Chunk).filter(
            Chunk.document_id == document_id
        ).order_by(Chunk.chunk_index).all()

    def create(self, chunk: Chunk) -> Chunk:
        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)
        return chunk

    def create_all(self, chunks: List[Chunk]) -> List[Chunk]:
        self.db.add_all(chunks)
        self.db.commit()
        for c in chunks:
            self.db.refresh(c)
        return chunks

    def find_all_with_embedding(self) -> List[Chunk]:
        return self.db.query(Chunk).filter(
            Chunk.embedding.isnot(None)
        ).all()

    def delete_by_document(self, document_id: int) -> None:
        self.db.query(Chunk).filter(Chunk.document_id == document_id).delete()
        self.db.commit()
