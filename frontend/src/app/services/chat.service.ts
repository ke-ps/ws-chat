import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Message } from '../models/message.model';

// ============================================================
// ORDEN DE EJECUCIÓN - Cómo funciona el chat:
// ============================================================
// 1. El componente (ChatComponent) se carga y muestra la lista de mensajes
// 2. El usuario escribe un mensaje y pulsa "Enviar"
// 3. ChatComponent llama a chatService.sendMessage()
// 4. ChatService:
//    a. Crea el mensaje con id, contenido, sender y timestamp
//    b. Lo añade al BehaviorSubject (actualiza la lista en la UI)
//    c. Envía el mensaje al servidor WebSocket
// 5. El servidor recibe el mensaje y hace broadcast a TODOS los clientes
// 6. Todos los clientes reciben el mensaje en onmessage y lo añaden a su lista
// ============================================================

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  // --------------------------------------------------------
  // PASO 1 - BehaviorSubject: almacena la lista de mensajes
  // Observable público para que el componente se suscriba
  // --------------------------------------------------------
  private messagesSubject = new BehaviorSubject<Message[]>([]);
  messages$: Observable<Message[]> = this.messagesSubject.asObservable();

  // --------------------------------------------------------
  // PASO 2 - Configuración WebSocket y usuario
  // --------------------------------------------------------
  private ws: WebSocket | null = null;
  private wsUrl = 'ws://localhost:8000/ws';
  private useWebSocket = true;

  // Nombre de usuario único para este navegador/sesión
  private username = `User-${Math.floor(Math.random() * 9000) + 1000}`;

  constructor() {
    // Se conecta automáticamente al backend al iniciar
    if (this.useWebSocket) {
      this.connectWebSocket();
    }
  }

  // --------------------------------------------------------
  // PASO 3 - Enviar mensaje
  // --------------------------------------------------------
  sendMessage(content: string): void {
    const message: Message = {
      id: crypto.randomUUID(),
      content,
      sender: this.username,
      timestamp: new Date()
    };

    // 3a. Actualizar la lista local (esto refresca la UI automaticamente)
    const currentMessages = this.messagesSubject.getValue();
    this.messagesSubject.next([...currentMessages, message]);

    // 3b. Enviar al servidor WebSocket para broadcast (incluye id para deduplicar)
    if (this.useWebSocket && this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ id: message.id, content, sender: this.username }));
    }
  }

  // --------------------------------------------------------
  // PASO 4 - Conectar al servidor WebSocket
  // --------------------------------------------------------
  connectWebSocket(): void {
    if (this.useWebSocket && !this.ws) {
      this.ws = new WebSocket(this.wsUrl);

      // 4a. Cuando la conexión se establece
      this.ws.onopen = () => {
        console.log('WebSocket conectado');
      };

      // 4b. Cuando llega un mensaje del servidor (broadcast de otro cliente o eco del nuestro)
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const message: Message = {
          id: data.id || crypto.randomUUID(),
          content: data.content,
          sender: data.sender,
          timestamp: new Date(data.timestamp)
        };
        // Ignorar si el mensaje ya existe (evita duplicado del emisor)
        const currentMessages = this.messagesSubject.getValue();
        const exists = currentMessages.some(m => m.id === message.id);
        if (!exists) {
          this.messagesSubject.next([...currentMessages, message]);
        }
      };

      // 4c. Manejo de errores
      this.ws.onerror = (error) => {
        console.error('Error WebSocket:', error);
      };

      // 4d. Cuando se cierra la conexión
      this.ws.onclose = () => {
        console.log('WebSocket desconectado');
        this.ws = null;
      };
    }
  }

  // --------------------------------------------------------
  // PASO 5 - Desconectar (para limpiar recursos)
  // --------------------------------------------------------
  disconnectWebSocket(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  // --------------------------------------------------------
  // PASO 6 - Obtener nombre de usuario
  // --------------------------------------------------------
  getUsername(): string {
    return this.username;
  }
}