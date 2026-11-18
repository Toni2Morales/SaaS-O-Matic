import { Component, input } from '@angular/core';

@Component({
  selector: 'app-section-heading',
  template: `
    <header class="section-heading">
      <h2>{{ title() }}</h2>
      @if (description()) {
        <p>{{ description() }}</p>
      }
    </header>
  `,
  styles: `
    .section-heading {
      display: grid;
      gap: var(--space-2);
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
      color: var(--color-text-muted);
      line-height: 1.6;
    }
  `,
})
export class SectionHeadingComponent {
  readonly title = input.required<string>();
  readonly description = input('');
}
