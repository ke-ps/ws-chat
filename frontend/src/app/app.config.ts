import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { initializeApp } from 'firebase/app';
import { firebaseConfig } from './enviroments/firebase.config';

import { routes } from './app.routes';

// ============================================================
// PASO 1 - Inicializar Firebase
// Se ejecuta una sola vez al cargar la app
// ============================================================
initializeApp(firebaseConfig);

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideAnimationsAsync()
  ]
};