import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import {
  catchError,
  distinctUntilChanged,
  map,
  merge,
  of,
  Subject,
  switchMap,
  tap,
  timer,
} from 'rxjs';
import { ApiError } from '../../core/http/api-error';
import { CustomerResponse } from '../../shared/models/api.models';
import { CustomerCardComponent } from '../../shared/components/customer-card';
import { EmptyStateComponent } from '../../shared/components/empty-state';
import { ErrorStateComponent } from '../../shared/components/error-state';
import { LoadingStateComponent } from '../../shared/components/loading-state';
import { SectionHeadingComponent } from '../../shared/components/section-heading';
import { CustomersApiService } from './data-access/customers-api.service';

interface CustomerQuery {
  search: string;
  limit: number;
  offset: number;
  delay: number;
}

@Component({
  imports: [
    CustomerCardComponent,
    EmptyStateComponent,
    ErrorStateComponent,
    LoadingStateComponent,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    ReactiveFormsModule,
    RouterLink,
    SectionHeadingComponent,
  ],
  template: `
    <div class="customers-page">
      <header class="page-actions">
        <app-section-heading
          title="Listado de clientes"
          description="Busca y consulta las empresas registradas."
        />
        <a mat-flat-button color="primary" routerLink="/customers/new">＋ Nuevo cliente</a>
      </header>
      <p class="simulation-guidance">
        Para preparar una simulación, abre la ficha del cliente que corresponda.
      </p>

      <section class="search-panel" aria-label="Búsqueda de clientes">
        <mat-form-field appearance="outline" class="search-field">
          <mat-label>Buscar empresa o ID fiscal</mat-label>
          <input
            matInput
            type="search"
            autocomplete="off"
            [formControl]="searchControl"
            aria-label="Buscar por razón social o identificador fiscal"
            aria-describedby="search-help"
          />
          @if (searchControl.value) {
            <button
              matSuffix
              mat-button
              type="button"
              aria-label="Limpiar búsqueda"
              [disabled]="busy()"
              (click)="clearSearch()"
            >
              Limpiar
            </button>
          }
        </mat-form-field>
        <p id="search-help" class="search-help">
          La búsqueda se realiza en el servidor y no distingue mayúsculas; se conservan acentos y
          signos literales.
        </p>
      </section>

      <section class="results-section" aria-labelledby="results-heading" [attr.aria-busy]="busy()">
        <div class="results-heading">
          <h2 id="results-heading">
            {{ searchControl.value.trim() ? 'Resultados de búsqueda' : 'Empresas registradas' }}
          </h2>
          @if (!loading() && !error()) {
            <p class="result-count" aria-live="polite">
              {{ total() }} {{ total() === 1 ? 'resultado' : 'resultados' }}
            </p>
          }
        </div>

        @if (loading() || searchPending()) {
          <app-loading-state
            [message]="searchPending() ? 'Actualizando búsqueda…' : 'Cargando clientes…'"
          />
        } @else if (error()) {
          <app-error-state
            title="No se pudo cargar el listado"
            [message]="error()!"
            (retry)="reload()"
          />
        } @else if (total() === 0 && !searchControl.value.trim()) {
          <app-empty-state
            title="Todavía no hay clientes"
            message="Registra la primera empresa para empezar a gestionar sus estimaciones."
          >
            <a class="empty-action" routerLink="/customers/new">Registrar cliente</a>
          </app-empty-state>
        } @else if (customers().length === 0) {
          <app-empty-state
            title="No hay coincidencias"
            message="Prueba con otra razón social o identificador fiscal, o limpia la búsqueda."
          >
            <button class="empty-action" type="button" (click)="clearSearch()">
              Limpiar búsqueda
            </button>
          </app-empty-state>
        } @else {
          <div class="customer-list">
            @for (customer of customers(); track customer.id) {
              <app-customer-card [customer]="customer" />
            }
          </div>

          <div class="pagination" aria-label="Paginación de clientes">
            <mat-form-field appearance="outline" class="page-size-field">
              <mat-label>Resultados por página</mat-label>
              <mat-select
                [value]="limit()"
                [disabled]="busy()"
                (selectionChange)="changeLimit($event.value)"
              >
                @for (size of pageSizes; track size) {
                  <mat-option [value]="size">{{ size }}</mat-option>
                }
              </mat-select>
            </mat-form-field>
            <span class="page-indicator">{{ pageStart() }}–{{ pageEnd() }} de {{ total() }}</span>
            <div class="page-buttons">
              <button
                mat-button
                type="button"
                [disabled]="busy() || offset() === 0"
                aria-label="Página anterior"
                (click)="previousPage()"
              >
                Anterior
              </button>
              <button
                mat-button
                type="button"
                [disabled]="busy() || offset() + limit() >= total()"
                aria-label="Página siguiente"
                (click)="nextPage()"
              >
                Siguiente
              </button>
            </div>
          </div>
        }
      </section>
    </div>
  `,
  styles: `
    :host {
      display: block;
    }
    .customers-page {
      display: grid;
      gap: var(--space-6);
    }
    .page-actions {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: var(--space-4);
    }
    .page-actions a {
      min-height: 2.75rem;
      flex: 0 0 auto;
    }
    .simulation-guidance {
      margin: calc(-1 * var(--space-4)) 0 0;
      color: var(--color-text-muted);
      font-size: 0.85rem;
    }
    .search-panel {
      display: grid;
      gap: 0;
      padding: var(--space-5);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      background: var(--color-surface);
    }
    .search-field {
      width: 100%;
    }
    .search-help {
      margin: calc(-1 * var(--space-3)) 0 0;
      color: var(--color-text-muted);
      font-size: 0.8rem;
      line-height: 1.5;
    }
    .results-section {
      display: grid;
      gap: var(--space-4);
    }
    .results-heading {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: var(--space-3);
    }
    .results-heading h2 {
      margin: 0;
      color: var(--color-text-strong);
      font-size: 1.05rem;
    }
    .result-count {
      margin: 0;
      color: var(--color-text-muted);
      font-size: 0.85rem;
      font-variant-numeric: tabular-nums;
    }
    .customer-list {
      display: grid;
      gap: var(--space-3);
    }
    .pagination {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: var(--space-4);
      padding-top: var(--space-2);
    }
    .page-size-field {
      width: 10rem;
    }
    .page-indicator {
      color: var(--color-text-muted);
      font-size: 0.85rem;
      font-variant-numeric: tabular-nums;
    }
    .page-buttons {
      display: flex;
      gap: var(--space-2);
    }
    .empty-action {
      display: inline-flex;
      min-height: 2.75rem;
      align-items: center;
      padding-inline: var(--space-4);
      border: 1px solid #c7d2fe;
      border-radius: var(--radius-sm);
      color: var(--color-primary);
      background: #fff;
      font: inherit;
      font-size: 0.9rem;
      font-weight: 650;
      text-decoration: none;
      cursor: pointer;
    }
    .empty-action:hover {
      background: #f5f6ff;
    }
    @media (max-width: 600px) {
      .page-actions {
        align-items: stretch;
        flex-direction: column;
      }
      .page-actions a {
        align-self: flex-start;
      }
      .pagination {
        flex-wrap: wrap;
        justify-content: space-between;
      }
      .page-size-field {
        width: 9rem;
      }
      .search-panel {
        gap: var(--space-2);
      }
      .search-help {
        margin: 0;
        line-height: 1.6;
      }
    }
    @media (max-width: 360px) {
      .search-panel {
        padding: var(--space-3);
      }
      .page-indicator {
        order: 3;
        width: 100%;
        text-align: center;
      }
    }
  `,
})
export class CustomersPageComponent {
  private readonly customersApi = inject(CustomersApiService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly pageRequests = new Subject<{ offset: number; limit: number }>();

  readonly searchControl = new FormControl('', { nonNullable: true });
  readonly customers = signal<CustomerResponse[]>([]);
  readonly total = signal(0);
  readonly offset = signal(0);
  readonly limit = signal(20);
  readonly loading = signal(true);
  readonly searchPending = signal(false);
  readonly error = signal<string | null>(null);
  readonly pageSizes = [10, 20, 50] as const;

  constructor() {
    const initialQuery = of<CustomerQuery>({ search: '', limit: 20, offset: 0, delay: 0 });
    const searchQueries = this.searchControl.valueChanges.pipe(
      map((value) => value.trim()),
      distinctUntilChanged(),
      tap(() => this.searchPending.set(true)),
      map(
        (search): CustomerQuery => ({
          search,
          limit: this.limit(),
          offset: 0,
          delay: 300,
        }),
      ),
    );
    const pageQueries = this.pageRequests.pipe(
      map(
        ({ offset, limit }): CustomerQuery => ({
          search: this.searchControl.value.trim(),
          limit,
          offset,
          delay: 0,
        }),
      ),
    );

    merge(initialQuery, searchQueries, pageQueries)
      .pipe(
        switchMap((query) =>
          (query.delay === 0 ? of(query) : timer(query.delay).pipe(map(() => query))).pipe(
            tap(() => {
              this.searchPending.set(false);
              this.loading.set(true);
              this.error.set(null);
              this.limit.set(query.limit);
              this.offset.set(query.offset);
            }),
            switchMap(() =>
              this.customersApi.list(query.limit, query.offset, query.search).pipe(
                map((page) => ({ query, page, failure: null as string | null })),
                catchError((error: unknown) =>
                  of({
                    query,
                    page: null,
                    failure:
                      error instanceof ApiError
                        ? error.message
                        : 'No se pudieron consultar los clientes. Inténtalo de nuevo.',
                  }),
                ),
              ),
            ),
          ),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe(({ query, page, failure }) => {
        this.loading.set(false);
        this.searchPending.set(false);
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
          this.offset.set(correctedOffset);
          this.pageRequests.next({ offset: correctedOffset, limit: query.limit });
          return;
        }

        this.customers.set(page.items);
        this.total.set(page.total);
        this.offset.set(page.offset);
        this.limit.set(page.limit);
      });
  }

  busy(): boolean {
    return this.loading() || this.searchPending();
  }

  pageStart(): number {
    return this.total() === 0 ? 0 : this.offset() + 1;
  }

  pageEnd(): number {
    return Math.min(this.offset() + this.customers().length, this.total());
  }

  clearSearch(): void {
    if (this.searchControl.value !== '') {
      this.searchControl.setValue('');
    }
  }

  changeLimit(limit: number): void {
    this.pageRequests.next({ offset: 0, limit });
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
