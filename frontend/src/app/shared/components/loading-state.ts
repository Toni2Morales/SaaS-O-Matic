import { Component, input } from '@angular/core';

@Component({
  selector: 'app-loading-state',
  template: `
    <div class="state loading-state" role="status" aria-live="polite">
      <span class="spinner" aria-hidden="true"></span>
      <span>{{ message() }}</span>
    </div>
  `,
  styles: `
    .state {
      display: flex;
      min-height: 7rem;
      align-items: center;
      justify-content: center;
      gap: var(--space-3);
      color: var(--color-text-muted);
    }
    .spinner {
      width: 1.25rem;
      height: 1.25rem;
      border: 2px solid var(--color-border);
      border-top-color: var(--color-primary);
      border-radius: 50%;
      animation: rotate 700ms linear infinite;
    }
    @keyframes rotate {
      to {
        transform: rotate(360deg);
      }
    }
    @media (prefers-reduced-motion: reduce) {
      .spinner {
        animation: none;
        border-top-color: var(--color-primary);
      }
    }
  `,
})
export class LoadingStateComponent {
  readonly message = input('Cargando información…');
}
