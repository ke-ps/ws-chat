from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base


class User(Base):
    """
    Tabla users:
    - id: clave primaria auto-incrementada
    - firebase_uid: ID único de Firebase (único en la tabla)
    - email: email del usuario (único en la tabla)
    - display_name: nombre visible (opcional)
    - created_at: fecha de creación del registro
    - updated_at: fecha de última actualización
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firebase_uid = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    display_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    memberships = relationship("RoomMember", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, firebase_uid={self.firebase_uid})>"