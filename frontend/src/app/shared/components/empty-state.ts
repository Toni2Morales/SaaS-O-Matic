import { Component, input } from '@angular/core';

@Component({
  selector: 'app-empty-state',
  template: `
    <section class="empty-state" aria-live="polite">
      <span class="empty-mark" aria-hidden="true">✓</span>
      <h2>{{ title() }}</h2>
      <p>{{ message() }}</p>
      <ng-content />
    </section>
  `,
  styles: `
    .empty-state {
      display: grid;
      justify-items: center;
      gap: var(--space-3);
      padding: clamp(var(--space-6), 5vw, var(--space-10));
      border: 1px dashed #cbd5e1;
      border-radius: var(--radius-lg);
      background: var(--color-surface);
      text-align: center;
    }
    .empty-mark {
      display: grid;
      width: 2.5rem;
      height: 2.5rem;
      place-items: center;
      border-radius: 50%;
      color: var(--color-primary);
      background: var(--color-primary-soft);
      font-weight: 700;
    }
    h2,
    p {
      margin: 0;
    }
    h2 {
      color: var(--color-text-strong);
      font-size: 1.1rem;
    }
    p {
      max-width: 58ch;
      color: var(--color-text-muted);
      line-height: 1.6;
    }
  `,
})
export class EmptyStateComponent {
  readonly title = input.required<string>();
  readonly message = input.required<string>();
}
