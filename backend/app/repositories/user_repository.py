# ============================================================
# repositories/user_repository.py
# ============================================================
# Acceso directo a la tabla users.
# Solo operaciones de base de datos, sin lógica de negocio.
# ============================================================

from sqlalchemy.orm import Session
from app.models.user import User
from typing import Optional


class UserRepository:
    """Repositorio para operaciones CRUD sobre la tabla users."""

    def __init__(self, db: Session):
        self.db = db

    def find_by_firebase_uid(self, firebase_uid: str) -> Optional[User]:
        """Busca un usuario por su firebase_uid."""
        return self.db.query(User).filter(User.firebase_uid == firebase_uid).first()

    def find_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su email."""
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User) -> User:
        """Crea un nuevo usuario en la base de datos."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User) -> User:
        """Actualiza un usuario existente."""
        self.db.commit()
        self.db.refresh(user)
        return user

    def upsert(self, firebase_uid: str, email: str, display_name: Optional[str]) -> User:
        """
        Crea o actualiza un usuario.
        Si existe firebase_uid, actualiza los datos.
        Si no existe, crea uno nuevo.
        """
        user = self.find_by_firebase_uid(firebase_uid)
        if user:
            # Actualizar datos por si cambiaron
            user.email = email
            user.display_name = display_name or email
            return self.update(user)
        else:
            # Crear nuevo usuario
            new_user = User(
                firebase_uid=firebase_uid,
                email=email,
                display_name=display_name or email
            )
            return self.create(new_user)