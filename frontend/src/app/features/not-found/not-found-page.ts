import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';

@Component({
  imports: [MatButtonModule, RouterLink],
  template: `
    <section class="not-found" aria-labelledby="not-found-title">
      <p class="code">404</p>
      <h2 id="not-found-title">No encontramos esta página</h2>
      <p>Comprueba la dirección o vuelve al inicio.</p>
      <a mat-flat-button color="primary" routerLink="/">Ir al inicio</a>
    </section>
  `,
  styles: `
    .not-found {
      display: grid;
      justify-items: start;
      gap: var(--space-3);
    }
    .code {
      margin: 0;
      color: var(--color-primary);
      font-weight: 700;
    }
    h2,
    p {
      margin: 0;
    }
    h2 {
      color: var(--color-text-strong);
    }
    p:not(.code) {
      color: var(--color-text-muted);
    }
  `,
})
export class NotFoundPageComponent {}
