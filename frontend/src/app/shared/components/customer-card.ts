import { Component, input } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CustomerResponse } from '../models/api.models';

const countryNames: Record<CustomerResponse['country'], string> = {
  ES: 'España',
  PT: 'Portugal',
  FR: 'Francia',
  DE: 'Alemania',
  IT: 'Italia',
  NL: 'Países Bajos',
};

@Component({
  selector: 'app-customer-card',
  imports: [RouterLink],
  template: `
    <article class="customer-card">
      <div class="customer-main">
        <a
          class="customer-name"
          [routerLink]="['/customers', customer().id]"
          [attr.aria-label]="customer().legal_name"
        >
          <span>{{ customer().legal_name }}</span>
          <span class="detail-cue" aria-hidden="true">Abrir ficha →</span>
        </a>
        <span class="customer-tax-id">{{ customer().tax_id }}</span>
      </div>
      <dl class="customer-details">
        <div>
          <dt>País</dt>
          <dd>{{ countryNames[customer().country] }}</dd>
        </div>
        <div class="email-detail">
          <dt>Email</dt>
          <dd>{{ customer().email }}</dd>
        </div>
        <div>
          <dt>Plan</dt>
          <dd>
            <span class="plan-badge">{{ customer().plan }}</span>
          </dd>
        </div>
      </dl>
    </article>
  `,
  styles: `
    .customer-card {
      display: grid;
      grid-template-columns: minmax(12rem, 1fr) minmax(0, 2fr);
      align-items: center;
      gap: var(--space-5);
      padding: var(--space-5);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      background: var(--color-surface);
      box-shadow: var(--shadow-sm);
    }
    .customer-main {
      display: grid;
      min-width: 0;
      gap: var(--space-1);
    }
    .customer-name {
      display: inline-flex;
      align-items: baseline;
      flex-wrap: wrap;
      gap: var(--space-2);
      overflow-wrap: anywhere;
      color: var(--color-text-strong);
      font-weight: 650;
      text-decoration: none;
    }
    .customer-name span:first-child {
      text-decoration: underline;
      text-decoration-color: #c7d2fe;
      text-underline-offset: 0.18em;
    }
    .detail-cue {
      color: var(--color-primary);
      font-size: 0.75rem;
      font-weight: 600;
      white-space: nowrap;
    }
    .customer-name:hover {
      color: var(--color-primary);
      text-decoration: underline;
    }
    .customer-tax-id {
      overflow-wrap: anywhere;
      color: var(--color-text-muted);
      font-size: 0.875rem;
      font-variant-numeric: tabular-nums;
    }
    .customer-details {
      display: grid;
      grid-template-columns: minmax(7rem, 0.7fr) minmax(10rem, 1.5fr) minmax(5rem, 0.5fr);
      gap: var(--space-4);
      margin: 0;
    }
    .customer-details div {
      min-width: 0;
    }
    dt {
      color: var(--color-text-muted);
      font-size: 0.72rem;
      font-weight: 650;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }
    dd {
      overflow-wrap: anywhere;
      margin: var(--space-1) 0 0;
      color: var(--color-text);
      font-size: 0.9rem;
    }
    .plan-badge {
      display: inline-flex;
      border-radius: 999px;
      padding: 0.2rem 0.55rem;
      color: #3730a3;
      background: var(--color-primary-soft);
      font-size: 0.78rem;
      font-weight: 600;
    }
    @media (max-width: 767px) {
      .customer-card {
        grid-template-columns: 1fr;
        gap: var(--space-4);
      }
      .customer-details {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
      .email-detail {
        grid-column: 1 / -1;
      }
    }
    @media (max-width: 360px) {
      .customer-card {
        padding: var(--space-4);
      }
    }
  `,
})
export class CustomerCardComponent {
  readonly customer = input.required<CustomerResponse>();
  protected readonly countryNames = countryNames;
}
