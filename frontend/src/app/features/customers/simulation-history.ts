import { Component, DestroyRef, inject, input, signal } from '@angular/core';
import { takeUntilDestroyed, toObservable } from '@angular/core/rxjs-interop';
import { MatButtonModule } from '@angular/material/button';
import { RouterLink } from '@angular/router';
import { catchError, distinctUntilChanged, map, merge, of, Subject, switchMap, tap } from 'rxjs';
import { ApiError } from '../../core/http/api-error';
import { HistoricalSimulationResponse, Uuid } from '../../shared/models/api.models';
import { EmptyStateComponent } from '../../shared/components/empty-state';
import { ErrorStateComponent } from '../../shared/components/error-state';
import { LoadingStateComponent } from '../../shared/components/loading-state';
import { SectionHeadingComponent } from '../../shared/components/section-heading';
import {
  formatDateOnly,
  formatDateTime,
  formatExactRate,
  formatMoney,
} from '../../shared/utils/display-format';
import { SimulationHistoryApiService } from './data-access/simulation-history-api.service';

interface HistoryQuery {
  offset: number;
  limit: number;
}

@Component({
  selector: 'app-simulation-history',
  imports: [
    EmptyStateComponent,
    ErrorStateComponent,
    LoadingStateComponent,
    MatButtonModule,
    RouterLink,
    SectionHeadingComponent,
  ],
  template: `
    <section
      class="history-section"
      aria-label="Historial de simulaciones"
      [attr.aria-busy]="loading()"
    >
      <div class="history-header">
        <app-section-heading
          title="Historial de simulaciones"
          description="Registros guardados para este cliente; los importes históricos no se recalculan."
        />
        @if (!loading() && !error()) {
          <span class="history-total" aria-live="polite"
            >{{ total() }} {{ total() === 1 ? 'simulación' : 'simulaciones' }}</span
          >
        }
        <a
          mat-flat-button
          color="primary"
          [routerLink]="['/customers', customerId(), 'simulations', 'new']"
          >Nueva simulación</a
        >
      </div>

      @if (loading()) {
        <app-loading-state message="Cargando historial…" />
      } @else if (error()) {
        <app-error-state
          title="No se pudo cargar el historial"
          [message]="error()!"
          (retry)="reload()"
        />
      } @else if (items().length === 0) {
        <app-empty-state
          title="Aún no hay simulaciones guardadas"
          message="Cuando se complete una simulación para este cliente, aparecerá aquí. Los datos históricos desconocidos no se sustituyen por valores actuales."
        />
      } @else {
        <div class="history-list">
          @for (item of items(); track item.id) {
            <article class="history-card">
              <header class="history-card-header">
                <div>
                  <h3>Simulación del {{ formatDateTime(item.created_at) }}</h3>
                  <p>
                    {{
                      item.billing_period === 'monthly'
                        ? 'Estimación mensual'
                        : 'Periodicidad no disponible'
                    }}
                  </p>
                </div>
                <span class="record-id" [attr.aria-label]="'Identificador de registro ' + item.id"
                  >Registro guardado</span
                >
              </header>

              <dl class="history-metrics">
                <div>
                  <dt>Usuarios</dt>
                  <dd>{{ item.user_count }}</dd>
                </div>
                <div>
                  <dt>Almacenamiento</dt>
                  <dd>
                    {{ item.storage_gb === null ? 'No registrado' : item.storage_gb + ' GB' }}
                  </dd>
                </div>
                <div>
                  <dt>Llamadas API / mes</dt>
                  <dd>
                    {{
                      item.api_calls_per_month === null
                        ? 'No registrado'
                        : numberFormat.format(item.api_calls_per_month)
                    }}
                  </dd>
                </div>
                <div>
                  <dt>Subtotal EUR</dt>
                  <dd>{{ formatMoney(item.user_subtotal_eur, 'EUR') }}</dd>
                </div>
                <div>
                  <dt>Total EUR</dt>
                  <dd>{{ formatMoney(item.total_eur, 'EUR') }}</dd>
                </div>
                <div>
                  <dt>Total convertido</dt>
                  <dd>{{ formatMoney(item.converted_total, item.display_currency) }}</dd>
                </div>
              </dl>

              <details class="snapshot-details">
                <summary>Ver datos del snapshot</summary>
                <dl class="snapshot-grid">
                  <div>
                    <dt>Impuesto</dt>
                    <dd>{{ formatMoney(item.tax_amount_eur, 'EUR') }}</dd>
                  </div>
                  <div>
                    <dt>País fiscal</dt>
                    <dd>{{ item.tax_country ?? 'No registrado' }}</dd>
                  </div>
                  <div>
                    <dt>Tasa fiscal</dt>
                    <dd>{{ formatExactRate(item.tax_rate) }}</dd>
                  </div>
                  <div>
                    <dt>Ámbito fiscal</dt>
                    <dd>{{ item.tax_territory ?? 'No registrado' }}</dd>
                  </div>
                  <div>
                    <dt>Referencia de cambio</dt>
                    <dd>{{ formatDateOnly(item.exchange_rate_date) }}</dd>
                  </div>
                  <div>
                    <dt>Tipo de cambio</dt>
                    <dd>{{ formatExactRate(item.exchange_rate) }}</dd>
                  </div>
                  <div>
                    <dt>Fuente de cambio</dt>
                    <dd>{{ item.exchange_rate_source ?? 'No registrado' }}</dd>
                  </div>
                  <div>
                    <dt>Tipo obtenido</dt>
                    <dd>{{ formatDateTime(item.exchange_rate_obtained_at) }}</dd>
                  </div>
                  <div>
                    <dt>Catálogo fiscal</dt>
                    <dd>{{ item.tax_catalog_version ?? 'No registrado' }}</dd>
                  </div>
                  <div>
                    <dt>Fecha de verificación fiscal</dt>
                    <dd>{{ formatDateOnly(item.tax_verified_on) }}</dd>
                  </div>
                </dl>
              </details>
            </article>
          }
        </div>

        <nav class="history-pagination" aria-label="Páginas del historial">
          <span>{{ pageStart() }}–{{ pageEnd() }} de {{ total() }}</span>
          <div>
            <button
              mat-button
              type="button"
              aria-label="Página anterior del historial"
              [disabled]="offset() === 0"
              (click)="previousPage()"
            >
              Anterior
            </button>
            <button
              mat-button
              type="button"
              aria-label="Página siguiente del historial"
              [disabled]="offset() + limit() >= total()"
              (click)="nextPage()"
            >
              Siguiente
            </button>
          </div>
        </nav>
      }
    </section>
  `,
  styles: `
    :host {
      display: block;
    }
    .history-section {
      display: grid;
      gap: var(--space-5);
    }
    .history-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: var(--space-4);
    }
    .history-header app-section-heading {
      flex: 1;
      min-width: 0;
    }
    .history-total {
      color: var(--color-text-muted);
      font-size: 0.85rem;
      font-variant-numeric: tabular-nums;
    }
    .history-list {
      display: grid;
      gap: var(--space-4);
    }
    .history-card {
      display: grid;
      gap: var(--space-5);
      padding: var(--space-5);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      background: var(--color-surface);
    }
    .history-card-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: var(--space-4);
    }
    .history-card-header h3 {
      margin: 0;
      color: var(--color-text-strong);
      font-size: 1rem;
    }
    .history-card-header p {
      margin: var(--space-1) 0 0;
      color: var(--color-text-muted);
      font-size: 0.82rem;
    }
    .record-id {
      flex: 0 0 auto;
      padding: 0.25rem 0.6rem;
      border-radius: 999px;
      color: #475569;
      background: #f1f5f9;
      font-size: 0.72rem;
    }
    .history-metrics,
    .snapshot-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: var(--space-4);
      margin: 0;
    }
    .history-metrics div,
    .snapshot-grid div {
      min-width: 0;
    }
    dt {
      color: var(--color-text-muted);
      font-size: 0.72rem;
      font-weight: 650;
      letter-spacing: 0.035em;
      text-transform: uppercase;
    }
    dd {
      margin: var(--space-1) 0 0;
      color: var(--color-text-strong);
      font-size: 0.92rem;
      font-variant-numeric: tabular-nums;
      overflow-wrap: anywhere;
    }
    .snapshot-details {
      padding-top: var(--space-4);
      border-top: 1px solid var(--color-border);
    }
    .snapshot-details summary {
      width: fit-content;
      color: var(--color-primary);
      font-size: 0.86rem;
      font-weight: 600;
      cursor: pointer;
    }
    .snapshot-grid {
      margin-top: var(--space-4);
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .history-pagination {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      gap: var(--space-4);
      color: var(--color-text-muted);
      font-size: 0.85rem;
      font-variant-numeric: tabular-nums;
    }
    .history-pagination > div {
      display: flex;
      gap: var(--space-2);
    }
    @media (max-width: 720px) {
      .history-metrics {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }
    @media (max-width: 450px) {
      .history-header {
        align-items: stretch;
        flex-direction: column;
      }
      .history-header a {
        width: 100%;
      }
      .history-card {
        padding: var(--space-4);
      }
      .history-card-header {
        flex-direction: column;
      }
      .history-metrics,
      .snapshot-grid {
        grid-template-columns: 1fr;
      }
      .history-pagination {
        justify-content: space-between;
      }
    }
  `,
})
export class SimulationHistoryComponent {
  private readonly historyApi = inject(SimulationHistoryApiService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly pageRequests = new Subject<HistoryQuery>();

  readonly customerId = input.required<Uuid>();
  readonly items = signal<HistoricalSimulationResponse[]>([]);
  readonly total = signal(0);
  readonly offset = signal(0);
  readonly limit = signal(10);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  protected readonly formatMoney = formatMoney;
  protected readonly formatExactRate = formatExactRate;
  protected readonly formatDateOnly = formatDateOnly;
  protected readonly formatDateTime = formatDateTime;
  protected readonly numberFormat = new Intl.NumberFormat('es-ES', { maximumFractionDigits: 0 });

  constructor() {
    toObservable(this.customerId)
      .pipe(
        distinctUntilChanged(),
        switchMap((customerId) => {
          this.items.set([]);
          this.total.set(0);
          this.offset.set(0);
          this.limit.set(10);
          this.error.set(null);
          this.loading.set(true);

          const initialQuery = of<HistoryQuery>({ offset: 0, limit: 10 });
          const pageQueries = this.pageRequests.pipe(map((query) => ({ ...query })));
          return merge(initialQuery, pageQueries).pipe(
            tap((query) => {
              this.loading.set(true);
              this.error.set(null);
              this.offset.set(query.offset);
              this.limit.set(query.limit);
            }),
            switchMap((query) =>
              this.historyApi.getPage(customerId, query.limit, query.offset).pipe(
                map((page) => ({ query, page, failure: null as string | null })),
                catchError((error: unknown) =>
                  of({
                    query,
                    page: null,
                    failure:
                      error instanceof ApiError
                        ? error.message
                        : 'No se pudo consultar el historial. Inténtalo de nuevo.',
                  }),
                ),
              ),
            ),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe(({ query, page, failure }) => {
        this.loading.set(false);
        if (failure) {
          this.error.set(failure);
          return;
        }
        if (!page) {
          return;
        }

        const correctedOffset =
          page.total === 0
            ? 0
            : Math.min(query.offset, Math.floor((page.total - 1) / query.limit) * query.limit);
        if (correctedOffset !== query.offset) {
          this.loading.set(true);
          this.pageRequests.next({ offset: correctedOffset, limit: query.limit });
          return;
        }

        this.items.set(page.items);
        this.total.set(page.total);
        this.offset.set(page.offset);
        this.limit.set(page.limit);
      });
  }

  pageStart(): number {
    return this.total() === 0 ? 0 : this.offset() + 1;
  }

  pageEnd(): number {
    return Math.min(this.offset() + this.items().length, this.total());
  }

  previousPage(): void {
    this.pageRequests.next({
      offset: Math.max(0, this.offset() - this.limit()),
      limit: this.limit(),
    });
  }

  nextPage(): void {
    if (this.offset() + this.limit() < this.total()) {
      this.pageRequests.next({ offset: this.offset() + this.limit(), limit: this.limit() });
    }
  }

  reload(): void {
    this.pageRequests.next({ offset: this.offset(), limit: this.limit() });
  }
}
