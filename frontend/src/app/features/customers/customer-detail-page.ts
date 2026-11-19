import { Component, DestroyRef, inject, input, signal } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { toObservable, takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { catchError, distinctUntilChanged, map, merge, of, Subject, switchMap, tap } from 'rxjs';
import { ApiError } from '../../core/http/api-error';
import { CustomerResponse } from '../../shared/models/api.models';
import { ErrorStateComponent } from '../../shared/components/error-state';
import { LoadingStateComponent } from '../../shared/components/loading-state';
import { formatDateTime } from '../../shared/utils/display-format';
import { SimulationHistoryComponent } from './simulation-history';
import { CustomersApiService } from './data-access/customers-api.service';

const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const countryNames: Record<CustomerResponse['country'], string> = {
  ES: 'España',
  PT: 'Portugal',
  FR: 'Francia',
  DE: 'Alemania',
  IT: 'Italia',
  NL: 'Países Bajos',
};

@Component({
  imports: [
    ErrorStateComponent,
    LoadingStateComponent,
    MatButtonModule,
    RouterLink,
    SimulationHistoryComponent,
  ],
  template: `
    <div class="detail-page">
      <div class="back-row"><a mat-button routerLink="/customers">← Volver a clientes</a></div>
      @if (loading()) {
        <app-loading-state message="Cargando datos del cliente…" />
      } @else if (error()) {
        <app-error-state
          [title]="notFound() ? 'Cliente no encontrado' : 'No se pudo cargar el cliente'"
          [message]="error()!"
          [retryable]="!notFound()"
          (retry)="retryCustomer()"
        />
        @if (notFound()) {
          <a class="list-link" routerLink="/customers">Ir al listado de clientes</a>
        }
      } @else if (customer(); as record) {
        @if (createdNotice()) {
          <p class="created-notice" role="status">El cliente se ha creado correctamente.</p>
        }
        <section class="customer-profile" aria-labelledby="customer-profile-title">
          <div class="profile-heading">
            <div>
              <p class="eyebrow">Ficha de cliente</p>
              <h2 id="customer-profile-title">{{ record.legal_name }}</h2>
              <p class="profile-tax-id">
                Identificador fiscal: <strong>{{ record.tax_id }}</strong>
              </p>
            </div>
            <a
              mat-flat-button
              color="primary"
              [routerLink]="['/customers', record.id, 'simulations', 'new']"
              >Nueva simulación</a
            >
          </div>
          <dl class="profile-grid">
            <div>
              <dt>Email de contacto</dt>
              <dd>{{ record.email }}</dd>
            </div>
            <div>
              <dt>País</dt>
              <dd>{{ countryNames[record.country] }}</dd>
            </div>
            <div>
              <dt>Plan</dt>
              <dd>
                <span class="plan-badge">{{ record.plan }}</span>
              </dd>
            </div>
            <div>
              <dt>Cliente desde</dt>
              <dd>{{ formatDateTime(record.created_at) }}</dd>
            </div>
          </dl>
        </section>

        <app-simulation-history [customerId]="record.id" />
      }
    </div>
  `,
  styles: `
    :host {
      display: block;
    }
    .detail-page {
      display: grid;
      gap: var(--space-5);
    }
    .back-row {
      margin-top: calc(-1 * var(--space-4));
    }
    .customer-profile {
      display: grid;
      gap: var(--space-6);
      padding: clamp(var(--space-5), 4vw, var(--space-8));
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      background: var(--color-surface);
      box-shadow: var(--shadow-sm);
    }
    .profile-heading {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: var(--space-5);
    }
    .profile-heading a {
      min-height: 2.75rem;
      flex: 0 0 auto;
    }
    .eyebrow {
      margin: 0 0 var(--space-2);
      color: var(--color-primary);
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }
    h2 {
      margin: 0;
      color: var(--color-text-strong);
      font-size: clamp(1.35rem, 3vw, 1.8rem);
      overflow-wrap: anywhere;
    }
    .profile-tax-id {
      margin: var(--space-2) 0 0;
      color: var(--color-text-muted);
      overflow-wrap: anywhere;
    }
    .profile-tax-id strong {
      color: var(--color-text);
      font-variant-numeric: tabular-nums;
    }
    .profile-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: var(--space-4);
      margin: 0;
      padding-top: var(--space-5);
      border-top: 1px solid var(--color-border);
    }
    .profile-grid div {
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
      margin: var(--space-2) 0 0;
      color: var(--color-text-strong);
      overflow-wrap: anywhere;
    }
    .plan-badge {
      display: inline-flex;
      padding: 0.2rem 0.55rem;
      border-radius: 999px;
      color: #3730a3;
      background: var(--color-primary-soft);
      font-size: 0.8rem;
      font-weight: 650;
    }
    .created-notice {
      margin: 0;
      padding: var(--space-3) var(--space-4);
      border: 1px solid #a7f3d0;
      border-radius: var(--radius-sm);
      color: #065f46;
      background: #ecfdf5;
    }
    .list-link {
      width: fit-content;
      color: var(--color-primary);
      font-weight: 600;
    }
    @media (max-width: 800px) {
      .profile-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }
    @media (max-width: 500px) {
      .profile-heading {
        flex-direction: column;
      }
      .profile-heading a {
        width: 100%;
      }
      .profile-grid {
        grid-template-columns: 1fr;
      }
    }
  `,
})
export class CustomerDetailPageComponent {
  private readonly customersApi = inject(CustomersApiService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly document = inject(DOCUMENT);
  private readonly retryRequests = new Subject<string>();

  readonly customerId = input<string>();
  readonly customer = signal<CustomerResponse | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly notFound = signal(false);
  readonly createdNotice = signal(false);
  protected readonly countryNames = countryNames;
  protected readonly formatDateTime = formatDateTime;

  constructor() {
    const navigationState = this.document.defaultView?.history.state as
      | { customerCreated?: unknown }
      | null
      | undefined;
    this.createdNotice.set(navigationState?.customerCreated === true);
    merge(toObservable(this.customerId), this.retryRequests)
      .pipe(
        distinctUntilChanged(),
        tap(() => {
          this.customer.set(null);
          this.loading.set(true);
          this.error.set(null);
          this.notFound.set(false);
        }),
        switchMap((customerId) => {
          if (!customerId || !uuidPattern.test(customerId)) {
            return of({
              customer: null,
              error: 'El identificador de cliente no tiene un formato válido.',
              notFound: false,
            });
          }
          return this.customersApi.get(customerId).pipe(
            map((customer) => ({ customer, error: null, notFound: false })),
            catchError((error: unknown) =>
              of({
                customer: null,
                error:
                  error instanceof ApiError
                    ? error.message
                    : 'No se pudieron consultar los datos del cliente. Inténtalo de nuevo.',
                notFound: error instanceof ApiError && error.status === 404,
              }),
            ),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => {
        this.customer.set(result.customer);
        this.error.set(result.error);
        this.notFound.set(result.notFound);
        this.loading.set(false);
      });
  }

  retryCustomer(): void {
    const customerId = this.customerId();
    if (customerId) {
      this.retryRequests.next(customerId);
    }
  }
}
