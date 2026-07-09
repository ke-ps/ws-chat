from sqlalchemy.orm import Session
from app.models.document import Document
from typing import List


class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, document: Document) -> Document:
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def find_by_id(self, document_id: int) -> Document | None:
        return self.db.query(Document).filter(Document.id == document_id).first()

    def find_by_room(self, room_id: int) -> List[Document]:
        return (
            self.db.query(Document)
            .filter(Document.room_id == room_id)
            .order_by(Document.created_at.desc())
            .all()
        )

    def find_by_room_and_filename(self, room_id: int, filename: str) -> Document | None:
        return (
            self.db.query(Document)
            .filter(Document.room_id == room_id, Document.filename == filename)
            .first()
        )

    def delete(self, document: Document) -> None:
        self.db.delete(document)
        self.db.commit()
