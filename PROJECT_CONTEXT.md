# PROJECT_CONTEXT.md

# WS-Chat — Contexto del Proyecto

## Descripción

WS-Chat es un proyecto Full Stack desarrollado como proyecto de clase.

El objetivo es construir un sistema de chat en tiempo real utilizando una arquitectura limpia y escalable, incorporando posteriormente Inteligencia Artificial y un sistema RAG (Retrieval-Augmented Generation) basado en documentación PDF.

El desarrollo se realiza por fases pequeñas para mantener el código sencillo y fácilmente mantenible.

---

# Stack tecnológico

## Backend

- FastAPI
- SQLAlchemy
- MySQL (Aiven)
- WebSockets
- Firebase Admin SDK

## Frontend

- Angular (Standalone Components)
- Angular Material
- RxJS

## Autenticación

- Firebase Authentication

## IA

Proveedor actual:

- Groq

Arquitectura preparada para permitir cambiar de proveedor sin modificar la lógica de negocio.

---

# Arquitectura

El backend sigue una arquitectura por capas.

```
Router
    ↓
Service
    ↓
Repository
    ↓
Database
```

Cada capa tiene una única responsabilidad.

## Models

Representan únicamente las entidades de la base de datos.

No contienen lógica de negocio.

## Repositories

Acceso a datos mediante SQLAlchemy.

Responsables únicamente de consultas CRUD.

## Services

Implementan toda la lógica de negocio.

Los routers nunca contienen lógica compleja.

## Routers

Reciben peticiones.

Validan datos.

Llaman al Service correspondiente.

Devuelven la respuesta.

---

# Estructura IA

Actualmente existen las siguientes capas:

```
AIProvider (interfaz)

        ▲

GroqProvider

        ▲

AIService

        ▲

MessageProcessor

        ▲

ChatService

        ▲

WebSocket
```

Cada capa tiene una responsabilidad concreta.

## AIProvider

Define la interfaz de cualquier proveedor de IA.

Permite sustituir Groq por OpenAI u otro proveedor sin modificar el resto del proyecto.

## GroqProvider

Únicamente realiza llamadas a la API de Groq.

No contiene lógica del proyecto.

No conoce salas.

No conoce RAG.

No conoce la base de datos.

## AIService

Es el punto de entrada para cualquier consulta a la IA.

Actualmente delega directamente al Provider.

En el futuro decidirá si utilizar:

- IA General
- RAG

según el tipo de sala.

## MessageProcessor

Es responsable de procesar el contenido de los mensajes.

Actualmente:

- detecta menciones "@IA"
- persiste mensajes
- solicita respuestas a AIService

En el futuro también decidirá cuándo lanzar consultas RAG.

## ChatService

Actúa únicamente como coordinador.

No contiene lógica de negocio compleja.

---

# Flujo actual del chat

```
Usuario

↓

Angular

↓

WebSocket

↓

ChatService

↓

MessageProcessor

↓

MessageService

↓

Repository

↓

MySQL
```

Si el mensaje comienza por:

```
@IA
```

el flujo continúa así:

```
MessageProcessor

↓

AIService

↓

GroqProvider

↓

Groq API

↓

Respuesta IA

↓

Persistencia

↓

Broadcast WebSocket
```

---

# WebSocket

Existe un único endpoint:

```
/ws/{room_id}
```

Cada sala mantiene:

- conexiones activas
- usuarios conectados

El servidor realiza broadcast únicamente a los usuarios de esa sala.

---

# Modelo Message

Los mensajes utilizan:

```
sender_type
```

Valores:

- USER
- AI
- SYSTEM

Los mensajes IA tienen:

```
user_id = NULL
```

Esto evita crear usuarios ficticios para representar la IA.

---

# Sistema de salas

Actualmente existen dos tipos.

## GENERAL

Salas normales.

Pueden ser creadas por los usuarios.

Permiten conversar libremente.

La IA responde mediante:

```
@IA
```

---

## RAG

Existe una única sala.

Se crea automáticamente al arrancar el backend.

Los usuarios no pueden crear nuevas salas RAG.

Toda consulta realizada en esta sala utilizará exclusivamente documentación.

---

# RAG (objetivo)

El sistema RAG tendrá la siguiente arquitectura.

```
Usuario

↓

Sala RAG

↓

AIService

↓

RAGService

↓

Vector Store

↓

Contexto

↓

GroqProvider

↓

Respuesta
```

Características:

- búsqueda automática en todos los documentos
- recuperación semántica
- respuesta únicamente basada en documentación
- nunca responder usando conocimiento general si no existe contexto

---

# Decisiones de arquitectura

## Provider

Nunca debe conocer:

- salas
- room_id
- RAG
- base de datos
- reglas del proyecto

Debe limitarse a realizar llamadas a la API del modelo.

---

## AIService

Es el único responsable de decidir:

- IA General
- RAG

Esto permite cambiar la estrategia sin modificar el Provider.

---

## MessageProcessor

Toda la lógica relacionada con el contenido del mensaje debe implementarse aquí.

No debe trasladarse al WebSocket.

---

## ChatService

Debe permanecer extremadamente pequeño.

Su única responsabilidad es coordinar el flujo.

---

# Base de datos

Motor:

- MySQL (Aiven)

ORM:

- SQLAlchemy

Las tablas se crean mediante:

```
init_db()
```

No se utilizan migraciones automáticas.

Los cambios de esquema se aplican manualmente mediante scripts SQL cuando sea necesario.

---

# Estado actual

## Completado

- Backend FastAPI
- Angular
- Firebase Authentication
- Persistencia MySQL
- Repository Pattern
- Service Layer
- WebSockets
- Salas
- Participantes
- Historial
- Usuarios conectados
- AIService
- GroqProvider
- Endpoint `/ai/test`
- IA mediante `@IA`
- Persistencia de respuestas IA
- sender_type
- ChatMessage
- ChatResult
- MessageProcessor
- RoomType
- Sala RAG creada automáticamente

---

## En desarrollo

Implementación del sistema RAG.

Próximas fases:

- RAGService
- Ingesta de PDFs
- Chunking
- Embeddings
- Base vectorial
- Recuperación de contexto
- Respuestas limitadas exclusivamente a la documentación

---

# Filosofía del proyecto

Siempre priorizar:

- simplicidad
- arquitectura limpia
- separación de responsabilidades
- código legible
- evolución por fases pequeñas
- mínimo código necesario

No implementar funcionalidades futuras antes de tiempo.

Cada fase debe dejar preparada la siguiente, pero sin desarrollarla.