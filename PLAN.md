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
- [x] Separación de responsabilidades
- [x] Organización del proyecto

---

# Fase 5 — Sistema de salas

## 5.1 Backend de salas ✅

- [x] Modelo Room
- [x] Repository
- [x] Service
- [x] Router
- [x] Persistencia

## 5.2 Participantes ✅

- [x] Tabla RoomMember
- [x] Añadir miembro
- [x] Listar miembros

## 5.3 WebSocket por sala ✅

- [x] Endpoint /ws/{room_id}
- [x] Validar sala
- [x] Broadcast por sala

## 5.4 Frontend de salas ✅

- [x] Listar salas
- [x] Cambio dinámico de sala
- [x] Reconexión WebSocket
- [x] Corrección de cambio de sala

## 5.5 Gestión de salas desde el frontend

- [x] Crear sala
- [x] Entrar automáticamente en la nueva sala
- [x] Actualizar listado
- [x] Validaciones

## 5.6 Persistencia de mensajes

- [x] Modelo Message
- [x] Guardar mensajes
- [x] Cargar historial por sala
- [x] Ordenar por fecha
- [ ] Mostrar historial al entrar

---

# Fase 6 — Funcionalidades del chat

## 6.1 Usuarios conectados

- [ ] Mostrar usuarios conectados por sala

## 6.2 Indicador de escritura

- [ ] "Usuario está escribiendo..."

## 6.3 Estado del WebSocket

- [ ] Conectando
- [ ] Conectado
- [ ] Desconectado
- [ ] Reconectando

## 6.4 Reconexión automática

- [ ] Reconectar automáticamente si se pierde la conexión

---

# Fase 7 — Diseño (UI/UX)

## Sidebar

- [ ] Mejorar listado de salas
- [ ] Iconos
- [ ] Avatar

## Chat

- [ ] Burbujas de mensajes
- [ ] Mejor scroll
- [ ] Hora de mensajes
- [ ] Responsive

## Apariencia

- [ ] Tema moderno
- [ ] Tema oscuro (opcional)
- [ ] Animaciones básicas

---

# Fase 8 — IA General

## 8.1 Asistente global

- [ ] Crear usuario IA
- [ ] Detectar mensajes que comiencen por @ia
- [ ] Enviar consulta al modelo
- [ ] Publicar la respuesta como un mensaje más del chat

## 8.2 Servicio IA

- [ ] ai_service.py
- [ ] Configuración del proveedor de IA
- [ ] Variables de entorno
- [ ] Manejo de errores

---

# Fase 9 — IA especializada (RAG)

## 9.1 Salas IA

- [ ] Añadir tipo de sala (normal / ai)

## 9.2 Ingesta documental

- [ ] Subir documentación
- [ ] Dividir documentos en chunks
- [ ] Generar embeddings

## 9.3 Base vectorial

- [ ] Almacenar embeddings
- [ ] Recuperar contexto

## 9.4 Servicio RAG

- [ ] rag_service.py
- [ ] Buscar contexto relevante
- [ ] Construir prompt
- [ ] Generar respuesta

## 9.5 Chat RAG

- [ ] La IA responde únicamente usando la documentación disponible
- [ ] Si no encuentra contexto, indicar que no dispone de información

---

# Ideas futuras (Fuera del alcance actual)

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

# Convenciones

Cada nueva funcionalidad debe cumplir:

- Mantener la arquitectura existente.
- Implementar únicamente la fase solicitada.
- No realizar refactors innecesarios.
- No modificar funcionalidades ya implementadas.
- No crear código que no sea necesario para la fase actual.

---

# Flujo de desarrollo

1.Actualizar este archivo marcando la fase como completada.