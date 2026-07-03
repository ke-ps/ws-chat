import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Message } from '../models/message.model';
import { Room } from '../models/room.model';

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
  // PASO 2 - Salas
  // --------------------------------------------------------
  private roomsSubject = new BehaviorSubject<Room[]>([]);
  rooms$: Observable<Room[]> = this.roomsSubject.asObservable();

  private selectedRoomIdSubject = new BehaviorSubject<number | null>(null);
  selectedRoomId$: Observable<number | null> = this.selectedRoomIdSubject.asObservable();

  // --------------------------------------------------------
  // PASO 3 - Configuración WebSocket
  // --------------------------------------------------------
  private ws: WebSocket | null = null;
  private wsUrl = '';
  private useWebSocket = true;

  constructor() {
    // No auto-conectar - esperar a que el usuario seleccione una sala
  }

  // --------------------------------------------------------
  // Cargar salas desde el backend
  // --------------------------------------------------------
  async loadRooms(): Promise<void> {
    try {
      const response = await fetch('http://localhost:8000/rooms');
      const rooms: Room[] = await response.json();
      this.roomsSubject.next(rooms);
    } catch (error) {
      console.error('Error al cargar salas:', error);
    }
  }

  // --------------------------------------------------------
  // Seleccionar una sala y conectar WebSocket
  // --------------------------------------------------------
  selectRoom(roomId: number): void {
    if (this.selectedRoomIdSubject.getValue() === roomId && this.ws) {
      return;
    }
    this.disconnectWebSocket();
    this.messagesSubject.next([]);
    this.selectedRoomIdSubject.next(roomId);
    this.wsUrl = `ws://localhost:8000/ws/${roomId}`;
    this.connectWebSocket();
  }

  // --------------------------------------------------------
  // PASO 4 - Enviar mensaje
  // sender = email del usuario autenticado con Firebase
  // --------------------------------------------------------
  sendMessage(content: string, sender: string): void {
    const message: Message = {
      id: crypto.randomUUID(),
      content,
      sender,
      timestamp: new Date()
    };

    const currentMessages = this.messagesSubject.getValue();
    this.messagesSubject.next([...currentMessages, message]);

    if (this.useWebSocket && this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ id: message.id, content, sender }));
    }
  }

  // --------------------------------------------------------
  // PASO 5 - Conectar al servidor WebSocket
  // --------------------------------------------------------
  private connectWebSocket(): void {
    if (!this.useWebSocket || !this.wsUrl || this.ws) {
      return;
    }
    const ws = new WebSocket(this.wsUrl);
    this.ws = ws;

    ws.onopen = () => {
      console.log('WebSocket conectado a sala', this.selectedRoomIdSubject.getValue());
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const message: Message = {
        id: data.id || crypto.randomUUID(),
        content: data.content,
        sender: data.sender,
        timestamp: new Date(data.timestamp)
      };
      const currentMessages = this.messagesSubject.getValue();
      const exists = currentMessages.some(m => m.id === message.id);
      if (!exists) {
        this.messagesSubject.next([...currentMessages, message]);
      }
    };

    ws.onerror = (error) => {
      console.error('Error WebSocket:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket desconectado');
      if (this.ws === ws) {
        this.ws = null;
      }
    };
  }

  // --------------------------------------------------------
  // PASO 6 - Desconectar
  // --------------------------------------------------------
  disconnectWebSocket(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}