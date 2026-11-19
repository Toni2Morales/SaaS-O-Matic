import { Component, input } from '@angular/core';

@Component({
  selector: 'app-empty-state',
  template: `
    <section class="empty-state" aria-live="polite">
      <svg class="empty-icon" viewBox="0 0 32 32" aria-hidden="true" focusable="false">
        <path d="M5 8h22v16H5z" />
        <path d="M3.5 13h7l2 3h6l2-3h7" />
      </svg>
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
    .empty-icon {
      width: 2.5rem;
      height: 2.5rem;
      fill: none;
      stroke: var(--color-primary);
      stroke-linecap: round;
      stroke-linejoin: round;
      stroke-width: 1.7;
    }
    .empty-icon path:first-child {
      fill: var(--color-primary-soft);
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
