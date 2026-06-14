import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  // --------------------------------------------------------
  // Inyectar servicios
  // --------------------------------------------------------
  private authService = inject(AuthService);
  private router = inject(Router);

  // --------------------------------------------------------
  // Datos del formulario
  // --------------------------------------------------------
  email = '';
  password = '';
  errorMessage = '';
  loading = false;

  // --------------------------------------------------------
  // Login con Firebase Auth
  // --------------------------------------------------------
  onLogin(): void {
    if (!this.email || !this.password) {
      this.errorMessage = 'Por favor, completa todos los campos';
      return;
    }

    this.loading = true;
    this.errorMessage = '';

    this.authService.login(this.email, this.password)
      .then(() => {
        // Login exitoso, redirigir al chat
        this.router.navigate(['/chat']);
      })
      .catch((error) => {
        // Mostrar error según el código de Firebase
        this.errorMessage = this.getErrorMessage(error.code);
      })
      .finally(() => {
        this.loading = false;
      });
  }

  // --------------------------------------------------------
  // Navegar a registro
  // --------------------------------------------------------
  goToRegister(): void {
    this.router.navigate(['/register']);
  }

  // --------------------------------------------------------
  // Traducir errores de Firebase a mensajeslegibles
  // --------------------------------------------------------
  private getErrorMessage(code: string): string {
    const errors: Record<string, string> = {
      'auth/user-not-found': 'No existe ninguna cuenta con este email',
      'auth/wrong-password': 'La contraseña es incorrecta',
      'auth/invalid-email': 'El formato del email no es válido',
      'auth/too-many-requests': 'Demasiados intentos. Espera un momento',
      'auth/invalid-credential': 'Credenciales incorrectas'
    };
    return errors[code] || 'Error al iniciar sesión. Inténtalo de nuevo.';
  }
}