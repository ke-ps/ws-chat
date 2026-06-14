import { Injectable } from '@angular/core';
import { getAuth } from 'firebase/auth';
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User as FirebaseUser
} from 'firebase/auth';
import { BehaviorSubject, Observable } from 'rxjs';
import { User } from '../models/user.model';

// ============================================================
// AuthService - Gestiona toda la autenticación con Firebase
// Encapsula la lógica de Firebase Auth y expone un Observable
// de usuario para que los componentes puedan reaccionar a
// cambios de estado (login/logout).
//
// Firebase SDK v9+ usa getAuth() en vez de inyección de dependencias.
// Esto es el patrón oficial del SDK modular.
// ============================================================

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  // --------------------------------------------------------
  // Obtener instancia de Auth via getAuth() (oficial de Firebase)
  // No se inyecta - se llama directamente cuando se necesita
  // --------------------------------------------------------
  private get auth() {
    return getAuth();
  }

  // --------------------------------------------------------
  // Observable público del usuario actual
  // Los componentes se suscriben para reaccionar a login/logout
  // --------------------------------------------------------
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  currentUser$: Observable<User | null> = this.currentUserSubject.asObservable();

  constructor() {
    // Escuchar cambios de estado de autenticación
    // Se ejecuta cada vez que un usuario inicia o cierra sesión
    onAuthStateChanged(this.auth, (firebaseUser) => {
      if (firebaseUser) {
        const user: User = {
          uid: firebaseUser.uid,
          email: firebaseUser.email || '',
          displayName: firebaseUser.displayName || firebaseUser.email || ''
        };
        this.currentUserSubject.next(user);
      } else {
        this.currentUserSubject.next(null);
      }
    });
  }

  // --------------------------------------------------------
  // Obtener usuario actual de forma síncrona
  // Útil para saber si estamos autenticados al cargar la app
  // --------------------------------------------------------
  getCurrentUser(): User | null {
    return this.currentUserSubject.getValue();
  }

  // --------------------------------------------------------
  // Registro de nuevo usuario con email y contraseña
  // --------------------------------------------------------
  register(email: string, password: string): Promise<FirebaseUser> {
    return createUserWithEmailAndPassword(this.auth, email, password)
      .then((credential) => credential.user);
  }

  // --------------------------------------------------------
  // Login con email y contraseña
  // --------------------------------------------------------
  login(email: string, password: string): Promise<FirebaseUser> {
    return signInWithEmailAndPassword(this.auth, email, password)
      .then((credential) => credential.user);
  }

  // --------------------------------------------------------
  // Logout - cerrar sesión
  // --------------------------------------------------------
  logout(): Promise<void> {
    return signOut(this.auth);
  }

  // --------------------------------------------------------
  // Obtener el token JWT de Firebase
  // Necesario para autenticar peticiones al backend
  // --------------------------------------------------------
  async getIdToken(): Promise<string | null> {
    const user = this.auth.currentUser;
    if (user) {
      return await user.getIdToken();
    }
    return null;
  }
}