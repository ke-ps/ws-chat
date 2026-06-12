import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Message } from '../models/message.model';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private messagesSubject = new BehaviorSubject<Message[]>([]);
  messages$: Observable<Message[]> = this.messagesSubject.asObservable();

  private ws: WebSocket | null = null;
  private wsUrl = 'ws://localhost:8000/ws';
  private useWebSocket = false; // Cambiar a true cuando el backend esté listo

  constructor() {
    this.initLocalSimulation();
  }

  private initLocalSimulation(): void {
    // Simulación local: respuestas automáticas para probar la UI
    if (!this.useWebSocket) {
      const initialMessages: Message[] = [
        {
          id: '1',
          content: '¡Hola! Este es el chat local. Cambia useWebSocket a true para conectar al backend.',
          sender: 'Bot',
          timestamp: new Date()
        }
      ];
      this.messagesSubject.next(initialMessages);
    }
  }

  sendMessage(content: string): void {
    const message: Message = {
      id: crypto.randomUUID(),
      content,
      sender: 'Tú',
      timestamp: new Date()
    };

    const currentMessages = this.messagesSubject.getValue();
    this.messagesSubject.next([...currentMessages, message]);

    if (!this.useWebSocket) {
      // Simulación local: el bot responde después de 1 segundo
      setTimeout(() => {
        const botResponse: Message = {
          id: crypto.randomUUID(),
          content: `Recibí: "${content}" - Esto es una respuesta simulada`,
          sender: 'Bot',
          timestamp: new Date()
        };
        const updatedMessages = this.messagesSubject.getValue();
        this.messagesSubject.next([...updatedMessages, botResponse]);
      }, 1000);
    }
  }

  connectWebSocket(): void {
    if (this.useWebSocket && !this.ws) {
      this.ws = new WebSocket(this.wsUrl);

      this.ws.onopen = () => {
        console.log('WebSocket conectado');
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const message: Message = {
          id: data.id || crypto.randomUUID(),
          content: data.content,
          sender: data.sender,
          timestamp: new Date(data.timestamp)
        };
        const currentMessages = this.messagesSubject.getValue();
        this.messagesSubject.next([...currentMessages, message]);
      };

      this.ws.onerror = (error) => {
        console.error('Error WebSocket:', error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket desconectado');
        this.ws = null;
      };
    }
  }

  disconnectWebSocket(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}