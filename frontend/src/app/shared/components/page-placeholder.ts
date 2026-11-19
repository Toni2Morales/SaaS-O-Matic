import { Component, input } from '@angular/core';

@Component({
  selector: 'app-page-placeholder',
  template: `
    <section class="placeholder" aria-labelledby="placeholder-title">
      <span class="placeholder-mark" aria-hidden="true">—</span>
      <h2 id="placeholder-title">{{ title() }}</h2>
      <p>{{ message() }}</p>
      <span class="status-label">Funcionalidad pendiente</span>
    </section>
  `,
  styles: `
    .placeholder {
      display: grid;
      max-width: 48rem;
      gap: var(--space-3);
      padding: clamp(var(--space-5), 5vw, var(--space-10));
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      background: var(--color-surface);
      box-shadow: var(--shadow-sm);
    }
    .placeholder-mark {
      display: grid;
      width: 2.75rem;
      height: 2.75rem;
      place-items: center;
      border-radius: var(--radius-md);
      color: var(--color-primary);
      background: var(--color-primary-soft);
      font-size: 1.3rem;
      font-weight: 700;
    }
    h2,
    p {
      margin: 0;
    }
    h2 {
      color: var(--color-text-strong);
      font-size: 1.15rem;
    }
    p {
      max-width: 58ch;
      color: var(--color-text-muted);
      line-height: 1.65;
    }
    .status-label {
      width: fit-content;
      margin-top: var(--space-2);
      padding: 0.35rem 0.65rem;
      border-radius: 999px;
      color: var(--color-primary);
      background: var(--color-primary-soft);
      font-size: 0.75rem;
      font-weight: 600;
    }
  `,
})
export class PagePlaceholderComponent {
  readonly title = input.required<string>();
  readonly message = input.required<string>();
}
