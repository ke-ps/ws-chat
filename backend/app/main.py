# ============================================================
# PASO 1 - Imports
# ============================================================
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
from datetime import datetime

# ============================================================
# PASO 2 - Crear la app FastAPI
# ============================================================
app = FastAPI()

# ============================================================
# PASO 3 - Configurar CORS
# Permite que el frontend Angular (puerto 4200) se conecte
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PASO 4 - Inicializar base de datos
# Crear tablas al arrancar la aplicación
# ============================================================
@app.on_event("startup")
def on_startup():
    from app.database.connection import init_db
    init_db()


# ============================================================
# PASO 5 - Registrar routers
# ============================================================
from app.routers.auth import router as auth_router
app.include_router(auth_router)


# ============================================================
# PASO 6 - Endpoints HTTP
# ============================================================

@app.get("/health")
def health():
    """Endpoint de verificación - GET /health"""
    return {"status": "ok"}


# ============================================================
# PASO 7 - WebSocket Manager
# Gestiona las conexiones activas y el broadcast de mensajes
# ============================================================
class ConnectionManager:
    """Administra las conexiones WebSocket activas."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Acepta una nueva conexión WebSocket."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Elimina una conexión WebSocket cerrada."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Envía un mensaje a TODOS los clientes conectados."""
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


# ============================================================
# PASO 8 - Endpoint WebSocket /ws
# Recibe mensajes de un cliente y los reenvía a todos
# ============================================================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            message["timestamp"] = datetime.now().isoformat()
            await manager.broadcast(message)
    except Exception:
        manager.disconnect(websocket)