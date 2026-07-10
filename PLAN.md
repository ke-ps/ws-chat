# PLAN.md

# WS-Chat Roadmap

Estado del proyecto: 🟡 En desarrollo

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

---

# Fase 4 — Arquitectura y refactorización ✅

- [x] Repository Pattern
- [x] Service Layer
- [x] Dependency Injection
- [x] Separación de responsabilidades
- [x] Organización del proyecto
- [x] MessageProcessor
- [x] ChatService como orquestador

---

# Fase 5 — Sistema de salas ✅

## 5.1 Backend de salas

- [x] Modelo Room
- [x] Repository
- [x] Service
- [x] Router
- [x] Persistencia

## 5.2 Participantes

- [x] Tabla RoomMember
- [x] Añadir miembro
- [x] Listar miembros

## 5.3 WebSocket por sala

- [x] Endpoint /ws/{room_id}
- [x] Validar sala
- [x] Broadcast por sala

## 5.4 Frontend de salas

- [x] Listar salas
- [x] Cambio dinámico de sala
- [x] Reconexión WebSocket

## 5.5 Gestión de salas

- [x] Crear sala
- [x] Entrar automáticamente
- [x] Actualizar listado

## 5.6 Persistencia de mensajes

- [x] Modelo Message
- [x] Guardar mensajes
- [x] Historial por sala
- [x] Orden cronológico
- [x] Mostrar historial al entrar

---

# Fase 6 — Funcionalidades del chat

## 6.1 Usuarios conectados ✅

- [x] Usuarios conectados por sala
- [x] Actualización en tiempo real

## 6.2 Indicador de escritura

- [ ] Usuario escribiendo...

## 6.3 Estado del WebSocket

- [ ] Conectando
- [ ] Conectado
- [ ] Desconectado
- [ ] Reconectando

## 6.4 Reconexión automática

- [ ] Reconectar automáticamente

---

# Fase 7 — Diseño (UI/UX)

## Sidebar

- [ ] Mejorar listado de salas
- [ ] Iconos
- [ ] Avatar

## Chat

- [ ] Burbujas de mensajes
- [ ] Diferenciar mensajes USER / IA
- [ ] Hora de mensajes
- [ ] Responsive

## Apariencia

- [ ] Tema moderno
- [ ] Tema oscuro (opcional)
- [ ] Animaciones

---

# Fase 8 — IA General 🚧

## 8.1 Integración

- [x] AIProvider
- [x] GroqProvider
- [x] AIService
- [x] Endpoint /ai/test
- [x] Dependency Injection
- [x] Variables de entorno

## 8.2 Chat IA

- [x] Invocación mediante @IA
- [x] MessageProcessor detecta menciones
- [x] ChatService desacoplado
- [x] Persistencia de respuestas IA
- [x] sender_type (USER / AI / SYSTEM)
- [x] user_id nullable para IA
- [x] Historial compatible con IA

## 8.3 Arquitectura preparada

- [x] ChatMessage
- [x] ChatResult
- [x] Separación JSON ↔ lógica
- [x] AIService preparado para futura integración RAG

---

# Fase 9 — Preparación RAG 🚧

## 9.1 Tipos de sala

- [x] RoomType (GENERAL / RAG)
- [x] room_type en Room
- [x] Sala RAG creada automáticamente al iniciar la aplicación

## 9.2 Flujo

- [ ] AIService decidirá entre IA General o RAG según room_type
- [ ] Crear RAGService
- [ ] Mantener Provider independiente del RAG

---

# Fase 10 — RAG (Documentación PDF)

## 10.1 Ingesta

- [x] Registro de documentos
- [x] Subida de PDFs
- [ ] Extracción de texto
- [ ] División en chunks
- [ ] Embeddings

## 10.2 Base vectorial

- [ ] Almacenar embeddings
- [ ] Búsqueda semántica
- [ ] Recuperación automática de contexto

## 10.3 Servicio RAG

- [ ] RAGService
- [ ] Construcción del contexto
- [ ] Prompt enriquecido
- [ ] Integración con AIService

## 10.4 Chat RAG

- [ ] Solo disponible en la sala RAG
- [ ] Búsqueda automática en todos los documentos
- [ ] Si no existe contexto suficiente, responder que la documentación no contiene esa información
- [ ] No utilizar conocimiento general del modelo

---

# Ideas futuras

- [ ] Chat privado
- [ ] Invitaciones
- [ ] Roles
- [ ] Administradores
- [ ] Reacciones
- [ ] Adjuntos
- [ ] Docker
- [ ] CI/CD
- [ ] Tests
- [ ] Despliegue

---

# Convenciones

Cada nueva funcionalidad debe:

- Mantener la arquitectura existente.
- Implementar únicamente la fase solicitada.
- No realizar refactors innecesarios.
- No modificar funcionalidades ya implementadas.
- No crear código que no sea necesario para la fase actual.
-No reestructures ni simplifiques PLAN.md. Conserva íntegramente el contenido existente y limita los cambios a marcar como completada la tarea implementada en esta fase. No elimines, renombres, reordenes ni modifiques fases o tareas ya existentes.

---

# Arquitectura IA

El proyecto tendrá dos modos claramente diferenciados.

## IA General

- Disponible en cualquier sala GENERAL.
- Se invoca escribiendo `@IA`.
- Puede responder cualquier pregunta.
- Utiliza únicamente el proveedor de IA (Groq).

## Sala RAG

- Existe una única sala RAG creada automáticamente.
- El usuario no puede crear salas RAG.
- Todas las consultas utilizan automáticamente RAG.
- Busca información en todos los documentos disponibles.
- Si la información no existe en la documentación, debe indicarlo y no responder usando conocimiento general.

---

# Flujo de desarrollo

1. Actualizar este archivo al finalizar cada fase.
2. Implementar únicamente la fase actual.
3. No avanzar automáticamente a la siguiente fase.

