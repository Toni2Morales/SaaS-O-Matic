import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-error-state',
  template: `
    <section class="error-state" role="alert">
      <span class="error-mark" aria-hidden="true">!</span>
      <div class="error-copy">
        <h2>{{ title() }}</h2>
        <p>{{ message() }}</p>
      </div>
      @if (retryable()) {
        <button class="retry-button" type="button" (click)="retry.emit()">Intentar de nuevo</button>
      }
    </section>
  `,
  styles: `
    .error-state {
      display: flex;
      align-items: flex-start;
      gap: var(--space-3);
      padding: var(--space-5);
      border: 1px solid #fecaca;
      border-radius: var(--radius-md);
      color: #7f1d1d;
      background: #fef2f2;
    }
    .error-mark {
      display: grid;
      width: 1.5rem;
      height: 1.5rem;
      flex: 0 0 auto;
      place-items: center;
      border: 1px solid currentcolor;
      border-radius: 50%;
      font-weight: 700;
    }
    .error-copy {
      flex: 1;
    }
    h2,
    p {
      margin: 0;
    }
    h2 {
      font-size: 1rem;
    }
    p {
      margin-top: var(--space-1);
      line-height: 1.55;
    }
    .retry-button {
      min-height: 2.5rem;
      border: 1px solid currentcolor;
      border-radius: var(--radius-sm);
      padding-inline: var(--space-3);
      color: inherit;
      background: transparent;
      font: inherit;
      font-weight: 600;
      cursor: pointer;
    }
    @media (max-width: 480px) {
      .error-state {
        flex-wrap: wrap;
      }
      .retry-button {
        margin-left: calc(1.5rem + var(--space-3));
      }
    }
  `,
})
export class ErrorStateComponent {
  readonly title = input('No se pudo completar la solicitud');
  readonly message = input.required<string>();
  readonly retryable = input(true);
  readonly retry = output<void>();
}
