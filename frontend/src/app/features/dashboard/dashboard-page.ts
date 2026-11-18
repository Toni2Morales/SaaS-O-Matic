import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { catchError, finalize, of } from 'rxjs';
import { CustomersApiService } from '../customers/data-access/customers-api.service';
import { ApiError } from '../../core/http/api-error';
import { CustomerResponse } from '../../shared/models/api.models';
import { CustomerCardComponent } from '../../shared/components/customer-card';
import { EmptyStateComponent } from '../../shared/components/empty-state';
import { ErrorStateComponent } from '../../shared/components/error-state';
import { LoadingStateComponent } from '../../shared/components/loading-state';
import { SectionHeadingComponent } from '../../shared/components/section-heading';

@Component({
  imports: [
    CustomerCardComponent,
    EmptyStateComponent,
    ErrorStateComponent,
    LoadingStateComponent,
    RouterLink,
    SectionHeadingComponent,
  ],
  template: `
    <div class="dashboard-page">
      <app-section-heading
        title="Bienvenido a SaaS-O-Matic"
        description="Herramienta interna para consultar clientes y preparar estimaciones mensuales de suscripciones SaaS."
      />

      <section class="overview-card" aria-labelledby="overview-title" [attr.aria-busy]="loading()">
        <div class="overview-copy">
          <span class="eyebrow">Panel comercial</span>
          <h2 id="overview-title">Una vista clara de tus clientes</h2>
          <p>Consulta empresas registradas y continúa con sus próximas acciones.</p>
        </div>
        <div
          class="customer-total"
          role="status"
          aria-live="polite"
          [attr.aria-label]="
            error()
              ? 'Total de clientes no disponible'
              : total() + ' ' + (total() === 1 ? 'cliente registrado' : 'clientes registrados')
          "
        >
          @if (loading()) {
            <app-loading-state message="Consultando clientes…" />
          } @else if (error()) {
            <span class="total-number" aria-hidden="true">—</span>
            <span class="total-label">Total no disponible</span>
          } @else {
            <span class="total-number">{{ total() }}</span>
            <span class="total-label">{{
              total() === 1 ? 'cliente registrado' : 'clientes registrados'
            }}</span>
          }
        </div>
      </section>

      <section class="capabilities" aria-label="Capacidades disponibles">
        <article class="capability-card">
          <span class="capability-icon" aria-hidden="true">⌖</span>
          <div>
            <h2>Países admitidos</h2>
            <p>España, Portugal, Francia, Alemania, Italia y Países Bajos</p>
          </div>
        </article>
        <article class="capability-card">
          <span class="capability-icon" aria-hidden="true">€</span>
          <div>
            <h2>Divisas disponibles</h2>
            <p>EUR, USD y GBP para las simulaciones</p>
          </div>
        </article>
      </section>

      <section class="quick-actions" aria-labelledby="quick-actions-title">
        <app-section-heading
          title="Acciones rápidas"
          description="Empieza por registrar o buscar un cliente."
        />
        <div class="action-grid">
          <a class="action-card action-card--primary" routerLink="/customers/new">
            <span class="action-icon" aria-hidden="true">＋</span>
            <span><strong>Nuevo cliente</strong><small>Registra una empresa</small></span>
            <span class="action-arrow" aria-hidden="true">→</span>
          </a>
          <a class="action-card" routerLink="/customers">
            <span class="action-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <circle cx="10.8" cy="10.8" r="6.3" />
                <path d="m16 16 4.2 4.2" />
              </svg>
            </span>
            <span><strong>Buscar clientes</strong><small>Consulta el listado</small></span>
            <span class="action-arrow" aria-hidden="true">→</span>
          </a>
          <a class="action-card" routerLink="/customers">
            <span class="action-icon" aria-hidden="true">↗</span>
            <span
              ><strong>Nueva simulación</strong><small>Primero selecciona un cliente</small></span
            >
            <span class="action-arrow" aria-hidden="true">→</span>
          </a>
        </div>
      </section>

      <section
        class="customer-preview"
        aria-labelledby="customer-preview-title"
        [attr.aria-busy]="loading()"
      >
        <div class="preview-header">
          <app-section-heading
            title="Clientes"
            description="Acceso a una selección del listado de clientes."
          />
          <a class="text-link" routerLink="/customers"
            >Ver todos <span aria-hidden="true">→</span></a
          >
        </div>
        <p id="customer-preview-title" class="visually-hidden">Accesos a clientes</p>
        @if (loading()) {
          <app-loading-state message="Cargando clientes…" />
        } @else if (error()) {
          <app-error-state
            title="No se pudieron cargar los clientes"
            [message]="error()!"
            (retry)="loadCustomers()"
          />
        } @else if (customers().length === 0) {
          <app-empty-state
            title="Todavía no hay clientes"
            message="Cuando registres una empresa, podrás consultarla desde aquí."
          >
            <a class="empty-action" routerLink="/customers/new">Registrar primer cliente</a>
          </app-empty-state>
        } @else {
          <div class="customer-list">
            @for (customer of customers(); track customer.id) {
              <app-customer-card [customer]="customer" />
            }
          </div>
          <p class="selection-note">
            Se muestran hasta seis clientes de la lista ordenada; no representa el orden de altas
            recientes.
          </p>
        }
      </section>
    </div>
  `,
  styles: `
    :host {
      display: block;
    }
    .dashboard-page {
      display: grid;
      gap: var(--space-8);
    }
    .overview-card {
      display: grid;
      grid-template-columns: minmax(0, 1.5fr) minmax(13rem, 0.7fr);
      gap: var(--space-8);
      align-items: center;
      padding: clamp(var(--space-5), 4vw, var(--space-8));
      border-radius: var(--radius-lg);
      color: #fff;
      background: linear-gradient(120deg, #312e81, #4f46e5 66%, #6366f1);
      box-shadow: 0 12px 30px rgb(49 46 129 / 18%);
    }
    .overview-copy .eyebrow {
      margin: 0 0 var(--space-2);
      color: #e0e7ff;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }
    .overview-copy h2 {
      margin: 0;
      font-size: clamp(1.45rem, 3vw, 2rem);
      letter-spacing: -0.035em;
    }
    .overview-copy p {
      max-width: 54ch;
      margin: var(--space-3) 0 0;
      color: #e0e7ff;
      line-height: 1.6;
    }
    .customer-total {
      display: grid;
      justify-items: center;
      align-content: center;
      min-height: 8rem;
      border: 1px solid rgb(255 255 255 / 25%);
      border-radius: var(--radius-md);
      background: rgb(255 255 255 / 12%);
      text-align: center;
    }
    .customer-total app-loading-state {
      color: #fff;
    }
    .total-number {
      font-size: clamp(2.5rem, 5vw, 3.5rem);
      font-weight: 750;
      line-height: 1;
      font-variant-numeric: tabular-nums;
    }
    .total-label {
      margin-top: var(--space-2);
      color: #e0e7ff;
      font-size: 0.85rem;
    }
    .capabilities {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: var(--space-4);
    }
    .capability-card {
      display: flex;
      align-items: flex-start;
      gap: var(--space-4);
      min-height: 7rem;
      padding: var(--space-5);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      background: var(--color-surface);
    }
    .capability-icon,
    .action-icon {
      display: grid;
      width: 2.5rem;
      height: 2.5rem;
      flex: 0 0 auto;
      place-items: center;
      border-radius: var(--radius-sm);
      color: var(--color-primary);
      background: var(--color-primary-soft);
      font-size: 1.25rem;
      font-weight: 700;
    }
    .capability-card h2 {
      margin: 0;
      color: var(--color-text-strong);
      font-size: 0.95rem;
    }
    .capability-card p {
      margin: var(--space-2) 0 0;
      color: var(--color-text-muted);
      font-size: 0.88rem;
      line-height: 1.5;
    }
    .quick-actions,
    .customer-preview {
      display: grid;
      gap: var(--space-5);
    }
    .action-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: var(--space-4);
    }
    .action-card {
      display: flex;
      min-width: 0;
      min-height: 5.5rem;
      align-items: center;
      gap: var(--space-3);
      padding: var(--space-4);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      color: inherit;
      background: var(--color-surface);
      text-decoration: none;
      transition:
        border-color 120ms ease,
        transform 120ms ease,
        box-shadow 120ms ease;
    }
    .action-card:hover {
      transform: translateY(-2px);
      border-color: #a5b4fc;
      box-shadow: var(--shadow-sm);
    }
    .action-card--primary {
      border-color: #c7d2fe;
      background: #f5f6ff;
    }
    .action-card > span:nth-child(2) {
      display: grid;
      min-width: 0;
      gap: var(--space-1);
    }
    .action-card strong {
      color: var(--color-text-strong);
      font-size: 0.92rem;
    }
    .action-card small {
      color: var(--color-text-muted);
      line-height: 1.4;
    }
    .action-icon svg {
      width: 1.3rem;
      height: 1.3rem;
      fill: none;
      stroke: currentColor;
      stroke-linecap: round;
      stroke-width: 1.8;
    }
    .action-arrow {
      margin-left: auto;
      color: var(--color-primary);
      font-size: 1.1rem;
    }
    .preview-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      gap: var(--space-4);
    }
    .text-link,
    .empty-action {
      color: var(--color-primary);
      font-size: 0.9rem;
      font-weight: 650;
      text-decoration: none;
    }
    .text-link:hover,
    .empty-action:hover {
      text-decoration: underline;
    }
    .customer-list {
      display: grid;
      gap: var(--space-3);
    }
    .selection-note {
      margin: 0;
      color: var(--color-text-muted);
      font-size: 0.78rem;
    }
    .empty-action {
      display: inline-flex;
      min-height: 2.75rem;
      align-items: center;
      padding-inline: var(--space-4);
      border: 1px solid #c7d2fe;
      border-radius: var(--radius-sm);
      background: #fff;
    }
    .visually-hidden {
      position: absolute;
      width: 1px;
      height: 1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      clip-path: inset(50%);
    }
    @media (max-width: 900px) {
      .action-grid {
        grid-template-columns: 1fr;
      }
      .action-card {
        min-height: 4.5rem;
      }
    }
    @media (max-width: 680px) {
      .overview-card {
        grid-template-columns: 1fr;
        gap: var(--space-5);
      }
      .customer-total {
        min-height: 6.5rem;
      }
    }
    @media (max-width: 520px) {
      .capabilities {
        grid-template-columns: 1fr;
      }
      .preview-header {
        align-items: flex-start;
      }
    }
    @media (prefers-reduced-motion: reduce) {
      .action-card {
        transition: none;
      }
    }
  `,
})
export class DashboardPageComponent {
  private readonly customersApi = inject(CustomersApiService);
  private readonly destroyRef = inject(DestroyRef);

  readonly customers = signal<CustomerResponse[]>([]);
  readonly total = signal(0);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);

  constructor() {
    this.loadCustomers();
  }

  loadCustomers(): void {
    this.loading.set(true);
    this.error.set(null);
    this.customersApi
      .list(6, 0, '')
      .pipe(
        catchError((error: unknown) => {
          this.error.set(
            error instanceof ApiError
              ? error.message
              : 'No se pudieron consultar los clientes. Inténtalo de nuevo.',
          );
          return of(null);
        }),
        finalize(() => this.loading.set(false)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((page) => {
        if (page) {
          this.customers.set(page.items);
          this.total.set(page.total);
        }
      });
  }
}
