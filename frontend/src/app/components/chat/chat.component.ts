import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { ChatService } from '../../services/chat.service';
import { Message } from '../../models/message.model';

// ============================================================
// ChatComponent - Solo se encarga de la UI
// NO tiene lógica de conexión ni comunicación
// Todo eso está en ChatService
// ============================================================

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatListModule
  ],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss'
})
export class ChatComponent {
  // --------------------------------------------------------
  // Inyectar ChatService para acceder a los mensajes
  // --------------------------------------------------------
  private chatService = inject(ChatService);
  messages$ = this.chatService.messages$; // Observable de mensajes
  newMessage = ''; // Modelo del input de texto
  username = this.chatService.getUsername(); // Nombre de usuario único

  // --------------------------------------------------------
  // Enviar mensaje - llama al service, no hace nada más
  // --------------------------------------------------------
  sendMessage(): void {
    if (this.newMessage.trim()) {
      this.chatService.sendMessage(this.newMessage);
      this.newMessage = ''; // Limpiar input después de enviar
    }
  }

  // --------------------------------------------------------
  // trackBy para optimizar el render de la lista
  // --------------------------------------------------------
  trackByMessageId(index: number, message: Message): string {
    return message.id;
  }
}