# PLAN.md

# WS-Chat Roadmap

Estado del proyecto: 🟡 En desarrollo

---

# Arquitectura

Arquitectura utilizada:

- Router → Service → Repository
- AIProvider desacoplado mediante inyección de dependencias
- AIService como punto de entrada para cualquier proveedor LLM
- MessageProcessor encargado del procesamiento de mensajes
- ChatService como coordinador del flujo
- Preparado para futuras integraciones RAG sin modificar la arquitectura existente

---

# Fase 1 — Configuración inicial ✅

- [x] Backend FastAPI
- [x] Estructura del proyecto
- [x] SQLAlchemy
- [x] MySQL
- [x] CORS
- [x] Health Check

---

# Fase 2 — Frontend y autenticación ✅

- [x] Angular
- [x] Angular Material
- [x] Routing
- [x] Firebase Authentication
- [x] Login
- [x] Registro
- [x] Logout
- [x] Guards
- [x] Sincronización Firebase → Backend
- [x] Persistencia de usuarios

---

# Fase 3 — Chat en tiempo real ✅

- [x] WebSocket
- [x] Envío de mensajes
- [x] Recepción de mensajes
- [x] Broadcast
- [x] Firebase Admin SDK
- [x] Usuarios conectados por sala

---

# Fase 4 — Arquitectura y refactorización ✅

- [x] Repository Pattern
- [x] Service Layer
- [x] Separación de responsabilidades
- [x] Organización del proyecto
- [x] AIProvider (Strategy Pattern)
- [x] AIService
- [x] Dependency Injection
- [x] MessageProcessor
- [x] ChatMessage / ChatResult (DTOs)

---

# Fase 5 — Sistema de salas ✅

## 5.1 Backend

- [x] Modelo Room
- [x] Repository
- [x] Service
- [x] Router
- [x] Persistencia

## 5.2 Participantes

- [x] Tabla RoomMember
- [x] Añadir miembro
- [x] Listar miembros

## 5.3 WebSocket

- [x] Endpoint /ws/{room_id}
- [x] Validar sala
- [x] Broadcast por sala

## 5.4 Frontend

- [x] Listar salas
- [x] Cambio dinámico de sala
- [x] Reconexión WebSocket

## 5.5 Gestión de salas

- [x] Crear sala
- [x] Entrar automáticamente
- [x] Actualizar listado
- [x] Validaciones

## 5.6 Persistencia

- [x] Modelo Message
- [x] Guardar mensajes
- [x] Cargar historial
- [x] Ordenar por fecha
- [x] Mostrar historial al entrar

---

# Fase 6 — Mejoras del chat

## 6.1 Usuarios conectados

- [x] Mostrar usuarios conectados por sala

## 6.2 Indicador de escritura

- [ ] Usuario está escribiendo...

## 6.3 Estado WebSocket

- [ ] Conectando
- [ ] Conectado
- [ ] Desconectado
- [ ] Reconectando

## 6.4 Reconexión automática

- [ ] Reconexión automática

---

# Fase 7 — Diseño (Pendiente)

## Sidebar

- [ ] Mejorar listado
- [ ] Iconos
- [ ] Avatar

## Chat

- [ ] Burbujas
- [ ] Scroll
- [ ] Hora
- [ ] Responsive

## Apariencia

- [ ] Tema moderno
- [ ] Tema oscuro (opcional)
- [ ] Animaciones

---

# Fase 8 — IA General ✅

## Arquitectura

- [x] AIProvider
- [x] GroqProvider
- [x] AIService
- [x] Dependencias FastAPI
- [x] Endpoint de prueba
- [x] Variables de entorno
- [x] Manejo de errores

## Chat IA

- [x] Detectar mensajes "@IA"
- [x] Procesar mediante MessageProcessor
- [x] Consultar Groq
- [x] Persistir respuestas IA
- [x] SenderType (USER / AI / SYSTEM)
- [x] Mostrar respuestas en tiempo real
- [x] Mostrar respuestas en historial

---

# Fase 9 — Preparación RAG ✅

## Arquitectura

- [x] RoomType (GENERAL / RAG)
- [x] Sala RAG creada automáticamente al iniciar el backend
- [x] Arquitectura preparada para decidir flujo según RoomType

---

# Fase 10 — RAG

## 10.1 Gestión documental

- [ ] Subida de PDFs
- [ ] Asociar documentos a la sala RAG
- [ ] Gestión de documentos

## 10.2 Procesamiento

- [ ] Lectura PDF
- [ ] División en chunks
- [ ] Generación de embeddings

## 10.3 Base vectorial

- [ ] Índice vectorial
- [ ] Recuperación semántica

## 10.4 RAG Service

- [ ] RAGService
- [ ] Recuperar contexto
- [ ] PromptBuilder
- [ ] Integración con AIService

## 10.5 Chat RAG

- [ ] Buscar automáticamente en toda la documentación
- [ ] Responder únicamente usando el contexto recuperado
- [ ] Si no existe contexto suficiente, indicar que no dispone de información
- [ ] Mantener separada la IA general del RAG

---

# Ideas futuras

- [ ] Chat privado
- [ ] Invitaciones
- [ ] Roles
- [ ] Administradores
- [ ] Reacciones
- [ ] Adjuntos
- [ ] Notificaciones
- [ ] Docker
- [ ] CI/CD
- [ ] Despliegue
- [ ] Tests
- [ ] Streaming de respuestas IA
- [ ] Memoria conversacional
- [ ] Múltiples proveedores LLM

---

# Convenciones

Cada nueva funcionalidad debe:

- Mantener la arquitectura Router → Service → Repository.
- No romper funcionalidades existentes.
- Evitar refactors innecesarios.
- Implementar únicamente la fase actual.
- Mantener el proyecto preparado para futuras ampliaciones.

---

# Flujo de desarrollo

1. Crear rama `feature/...`
2. Implementar únicamente la fase correspondiente.
3. Validar funcionamiento.
4. Actualizar este PLAN.md.
5. Commit.
6. Merge a `develop`.