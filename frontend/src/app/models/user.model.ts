export interface User {
  uid: string;       // ID único de Firebase Auth
  email: string;     // Email del usuario
  displayName?: string; // Nombre visible (opcional)
}