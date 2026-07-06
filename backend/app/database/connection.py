# ============================================================
# database/connection.py
# ============================================================
# Configuración de la sesión de base de datos con SQLAlchemy.
# Usa un scoped_session para que cada request tenga su propia
# sesión de forma thread-safe.
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ============================================================
# Cadena de conexión MySQL de Aiven
# Formato: mysql+pymysql://user:password@host:port/database
# ============================================================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://avnadmin:tu_password@tu_host:25185/defaultdb"
)

# Configuración SSL para conexión segura con Aiven
_ssl_args = {
    "check_hostname": True,
}

# Motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # Verifica la conexión antes de usar
    pool_recycle=3600,      # Recicla conexiones cada hora
    connect_args={"ssl": _ssl_args},
    echo=False               # Cambiar a True para ver SQL en consola
)

# ============================================================
# SessionFactory - crea sesiones para cada operación
# ============================================================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base declarativa para los modelos
Base = declarative_base()


# ============================================================
# Dependency de FastAPI para inyectar la sesión en los routers
# Se usa como: def endpoint(db: Session = Depends(get_db))
# ============================================================
def get_db():
    """Abre una sesión, la usa, y la cierra automáticamente."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# Al iniciar la app, crear las tablas si no existen
# Se llama desde main.py al arrancar
# ============================================================
def init_db():
    """Crea todas las tablas definidas en los modelos."""
    Base.metadata.create_all(bind=engine)