import { Component, DestroyRef, inject, input, signal } from '@angular/core';
import { takeUntilDestroyed, toObservable } from '@angular/core/rxjs-interop';
import { DOCUMENT } from '@angular/common';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import {
  catchError,
  distinctUntilChanged,
  map,
  merge,
  of,
  startWith,
  Subject,
  switchMap,
  tap,
  timer,
} from 'rxjs';
import { ApiError } from '../../core/http/api-error';
import {
  CustomerResponse,
  Currency,
  SimulationPreviewRequest,
  SimulationPreviewResponse,
  SimulationResponse,
} from '../../shared/models/api.models';
import {
  formatDateOnly,
  formatDateTime,
  formatExactRate,
  formatMoney,
  formatPercentRate,
} from '../../shared/utils/display-format';
import { CustomersApiService } from '../customers/data-access/customers-api.service';
import { SimulationsApiService } from './data-access/simulations-api.service';

const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const integer: ValidatorFn = (control) =>
  control.value === null || (Number.isFinite(control.value) && Number.isInteger(control.value))
    ? null
    : { integer: true };

type SimulationForm = FormGroup<{
  user_count: FormControl<number | null>;
  storage_gb: FormControl<number | null>;
  api_calls_per_month: FormControl<number | null>;
  display_currency: FormControl<Currency>;
}>;

@Component({
  imports: [
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatSliderModule,
    ReactiveFormsModule,
    RouterLink,
  ],
  template: `
    <main class="simulator">
      <a
        class="back-link"
        [routerLink]="customerId() ? ['/customers', customerId()] : ['/customers']"
        >← Volver</a
      >
      <h1 tabindex="-1">Simulador de suscripción</h1>
      @if (loadingCustomer()) {
        <p role="status">Cargando cliente…</p>
      } @else if (customerError()) {
        <section class="notice error" role="alert">
          <p>{{ customerError() }}</p>
          <button mat-button (click)="retryCustomer()">Intentar de nuevo</button>
        </section>
      } @else if (customer(); as client) {
        <section class="customer-context" aria-label="Cliente seleccionado">
          <strong>{{ client.legal_name }}</strong
          ><span>{{ countryName(client.country) }} · Plan {{ client.plan }}</span>
        </section>
        <div class="columns">
          <section class="panel">
            <h2>Configuración mensual</h2>
            <form [formGroup]="form" (ngSubmit)="save()" novalidate>
              <div class="field-heading"><span>Usuarios activos</span><span>0–1.000.000</span></div>
              <mat-slider
                min="0"
                max="1000"
                step="1"
                discrete
                [disabled]="saving() || !sliderEnabled()"
                aria-label="Usuarios activos, de 0 a 1.000"
              >
                <input matSliderThumb [value]="sliderValue()" (valueChange)="setSlider($event)" />
              </mat-slider>
              <mat-form-field appearance="outline" class="full-width">
                <mat-label>Usuarios activos</mat-label
                ><input
                  id="user-count"
                  matInput
                  type="number"
                  min="0"
                  max="1000000"
                  step="1"
                  formControlName="user_count"
                  aria-describedby="users-help users-error"
                />
                @if (form.controls.user_count.invalid && form.controls.user_count.touched) {
                  <mat-error id="users-error">{{ fieldError('user_count') }}</mat-error>
                }
              </mat-form-field>
              <p id="users-help" class="help">
                El deslizador llega a 1.000. Para cifras mayores, el deslizador se desactiva sin
                cambiar el valor manual.
              </p>
              <div class="tiers" aria-label="Tarifas progresivas por usuario">
                <span>Primeros 10: {{ bandCounts()[0] }} usuarios × 10 € / usuario</span>
                <span>11–50: {{ bandCounts()[1] }} usuarios × 8 € / usuario</span>
                <span>51+: {{ bandCounts()[2] }} usuarios × 5 € / usuario</span>
              </div>
              <mat-form-field appearance="outline" class="full-width">
                <mat-label>Almacenamiento contratado (GB)</mat-label
                ><input
                  matInput
                  type="number"
                  min="0"
                  max="1000000"
                  step="1"
                  formControlName="storage_gb"
                  aria-describedby="storage-help storage-error"
                />
                @if (form.controls.storage_gb.invalid && form.controls.storage_gb.touched) {
                  <mat-error id="storage-error">{{ fieldError('storage_gb') }}</mat-error>
                }
              </mat-form-field>
              <p id="storage-help" class="help">
                Dato informativo; sin coste adicional en este MVP.
              </p>
              <mat-form-field appearance="outline" class="full-width">
                <mat-label>Llamadas API mensuales</mat-label
                ><input
                  matInput
                  type="number"
                  min="0"
                  max="1000000000"
                  step="1"
                  formControlName="api_calls_per_month"
                  aria-describedby="calls-help calls-error"
                />
                @if (
                  form.controls.api_calls_per_month.invalid &&
                  form.controls.api_calls_per_month.touched
                ) {
                  <mat-error id="calls-error">{{ fieldError('api_calls_per_month') }}</mat-error>
                }
              </mat-form-field>
              <p id="calls-help" class="help">Dato informativo; sin coste adicional en este MVP.</p>
              <mat-form-field appearance="outline" class="full-width"
                ><mat-label>Divisa de visualización</mat-label>
                <mat-select formControlName="display_currency" aria-label="Divisa de visualización"
                  ><mat-option value="EUR">EUR — Euro</mat-option
                  ><mat-option value="USD">USD — Dólar estadounidense</mat-option
                  ><mat-option value="GBP">GBP — Libra esterlina</mat-option></mat-select
                >
              </mat-form-field>
            </form>
          </section>
          <section class="panel result-panel" aria-labelledby="estimate-heading">
            <h2 id="estimate-heading">Estimación mensual</h2>
            <p class="status" role="status" aria-live="polite">{{ statusMessage() }}</p>
            @if (preview(); as result) {
              <div [class.stale]="stale()">
                @if (stale()) {
                  <p class="notice">Estimación anterior: los parámetros han cambiado.</p>
                }
                <p class="total-label">Total mensual · {{ result.display_currency }}</p>
                <p class="total">{{ money(result.converted_total, result.display_currency) }}</p>
                <dl>
                  <div>
                    <dt>Subtotal usuarios (EUR)</dt>
                    <dd>{{ money(result.user_subtotal_eur, 'EUR') }}</dd>
                  </div>
                  <div>
                    <dt>País fiscal</dt>
                    <dd>{{ countryName(client.country) }} ({{ result.tax_country }})</dd>
                  </div>
                  <div>
                    <dt>Impuesto ({{ percentRate(result.tax_rate) }})</dt>
                    <dd>{{ money(result.tax_amount_eur, 'EUR') }}</dd>
                  </div>
                  <div>
                    <dt>Total original EUR</dt>
                    <dd>{{ money(result.total_eur, 'EUR') }}</dd>
                  </div>
                </dl>
                @if (result.display_currency !== 'EUR') {
                  <details>
                    <summary>Información del tipo de cambio</summary>
                    <dl>
                      <div>
                        <dt>Tipo</dt>
                        <dd>{{ result.exchange_rate }} {{ result.display_currency }} / EUR</dd>
                      </div>
                      <div>
                        <dt>Fecha de referencia</dt>
                        <dd>{{ dateOnly(result.exchange_rate_date) }}</dd>
                      </div>
                      <div>
                        <dt>Recuperado</dt>
                        <dd>{{ dateTime(result.exchange_rate_obtained_at) }}</dd>
                      </div>
                      <div>
                        <dt>Fuente</dt>
                        <dd>{{ result.exchange_rate_source }}</dd>
                      </div>
                    </dl>
                  </details>
                }
                @if (saved(); as persisted) {
                  <p class="notice success" role="status">
                    Simulación guardada. Resultado definitivo:
                    {{ money(persisted.converted_total, persisted.display_currency) }}.
                    <a [routerLink]="['/customers', client.id]">Ver ficha e historial</a>
                  </p>
                }
              </div>
            }
            @if (errorMessage()) {
              <div class="notice error" role="alert">
                <p>{{ errorMessage() }}</p>
                @if (fxUnavailable()) {
                  <button mat-button (click)="retryPreview()">Reintentar estimación</button
                  ><button mat-button (click)="selectEur()">Cambiar a EUR</button>
                }
              </div>
            }
            <p class="disclaimer">
              Estimación comercial; no es una factura ni asesoramiento fiscal.
            </p>
            <button
              mat-flat-button
              color="primary"
              type="button"
              [disabled]="!canSave()"
              (click)="save()"
            >
              {{ saving() ? 'Guardando…' : 'Guardar simulación' }}
            </button>
            @if (saveUncertain()) {
              <p class="notice error" role="alert">
                No se recibió confirmación. La simulación podría haberse guardado; consulta el
                historial antes de volver a intentarlo.
                <a [routerLink]="['/customers', client.id]">Consultar historial</a>
              </p>
            }
          </section>
        </div>
      }
    </main>
  `,
  styles: `
    :host {
      display: block;
    }
    .simulator {
      display: grid;
      gap: var(--space-5);
      max-width: 76rem;
      margin: auto;
    }
    .back-link {
      color: var(--color-primary);
      font-weight: 600;
    }
    h1,
    h2,
    p {
      margin: 0;
    }
    h1 {
      color: var(--color-text-strong);
      font-size: clamp(1.6rem, 3vw, 2rem);
    }
    h2 {
      font-size: 1.15rem;
      color: var(--color-text-strong);
    }
    .customer-context,
    .panel {
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: clamp(var(--space-4), 3vw, var(--space-6));
      box-shadow: var(--shadow-sm);
    }
    .customer-context {
      display: flex;
      justify-content: space-between;
      gap: var(--space-3);
      flex-wrap: wrap;
    }
    .customer-context span,
    .help,
    .disclaimer {
      color: var(--color-text-muted);
    }
    .columns {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      align-items: start;
      gap: var(--space-5);
    }
    .panel {
      display: grid;
      gap: var(--space-4);
      min-width: 0;
    }
    .panel form {
      display: grid;
      gap: var(--space-2);
    }
    .field-heading {
      display: flex;
      justify-content: space-between;
      gap: var(--space-2);
      font-weight: 650;
    }
    mat-slider {
      width: 100%;
    }
    .full-width {
      width: 100%;
    }
    .help {
      font-size: 0.88rem;
      line-height: 1.55;
      margin-top: calc(-1 * var(--space-2));
      margin-bottom: var(--space-2);
    }
    .tiers {
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-2);
      margin: var(--space-2) 0 var(--space-3);
    }
    .tiers span {
      border-radius: 999px;
      background: var(--color-primary-soft);
      color: #3730a3;
      padding: 0.35rem 0.65rem;
      font-size: 0.8rem;
    }
    .result-panel {
      position: sticky;
      top: var(--space-4);
    }
    .status {
      min-height: 1.5rem;
      color: var(--color-text-muted);
    }
    .total-label {
      color: var(--color-text-muted);
    }
    .total {
      font-size: clamp(2rem, 5vw, 3rem);
      line-height: 1.15;
      font-weight: 750;
      color: var(--color-primary);
      overflow-wrap: anywhere;
      font-variant-numeric: tabular-nums;
    }
    .stale {
      opacity: 0.75;
    }
    dl {
      display: grid;
      gap: var(--space-3);
      margin: 0;
    }
    dl div {
      display: flex;
      justify-content: space-between;
      gap: var(--space-3);
      padding-bottom: var(--space-2);
      border-bottom: 1px solid var(--color-border);
    }
    dt {
      color: var(--color-text-muted);
    }
    dd {
      margin: 0;
      text-align: right;
      font-weight: 600;
      overflow-wrap: anywhere;
    }
    details summary {
      cursor: pointer;
      color: var(--color-primary);
      padding: var(--space-2) 0;
    }
    .notice {
      padding: var(--space-3);
      border-radius: var(--radius-sm);
      background: #fffbeb;
      color: #78350f;
      line-height: 1.5;
    }
    .error {
      background: #fef2f2;
      color: #7f1d1d;
    }
    .success {
      background: #ecfdf5;
      color: #065f46;
    }
    .disclaimer {
      font-size: 0.85rem;
      line-height: 1.5;
    }
    button[mat-flat-button] {
      min-height: 2.75rem;
    }
    @media (max-width: 760px) {
      .columns {
        grid-template-columns: minmax(0, 1fr);
      }
      .result-panel {
        position: static;
      }
      .customer-context {
        flex-direction: column;
      }
    }
  `,
})
export class SimulationPageComponent {
  private readonly customersApi = inject(CustomersApiService);
  private readonly simulationsApi = inject(SimulationsApiService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly document = inject(DOCUMENT);
  private readonly customerRetry = new Subject<void>();
  private readonly previewRetry = new Subject<void>();
  readonly customerId = input<string>();
  readonly customer = signal<CustomerResponse | null>(null);
  readonly loadingCustomer = signal(true);
  readonly customerError = signal<string | null>(null);
  readonly form: SimulationForm = new FormGroup({
    user_count: new FormControl<number | null>(15, [
      Validators.required,
      Validators.min(0),
      Validators.max(1_000_000),
      integer,
    ]),
    storage_gb: new FormControl<number | null>(0, [
      Validators.required,
      Validators.min(0),
      Validators.max(1_000_000),
      integer,
    ]),
    api_calls_per_month: new FormControl<number | null>(0, [
      Validators.required,
      Validators.min(0),
      Validators.max(1_000_000_000),
      integer,
    ]),
    display_currency: new FormControl<Currency>('EUR', { nonNullable: true }),
  });
  readonly preview = signal<SimulationPreviewResponse | null>(null);
  readonly saved = signal<SimulationResponse | null>(null);
  readonly stale = signal(true);
  readonly preparing = signal(false);
  readonly calculating = signal(false);
  readonly saving = signal(false);
  readonly errorMessage = signal<string | null>(null);
  readonly fxUnavailable = signal(false);
  readonly saveUncertain = signal(false);
  private currentRequest: SimulationPreviewRequest | null = null;
  private generation = 0;
  protected readonly money = formatMoney;
  protected readonly exactRate = formatExactRate;
  protected readonly percentRate = formatPercentRate;
  protected readonly dateOnly = formatDateOnly;
  protected readonly dateTime = formatDateTime;

  constructor() {
    merge(toObservable(this.customerId), this.customerRetry)
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        switchMap(() => {
          const id = this.customerId();
          this.customer.set(null);
          this.loadingCustomer.set(true);
          this.customerError.set(null);
          if (!id || !uuidPattern.test(id))
            return of({ customer: null, error: 'El identificador del cliente no es válido.' });
          return this.customersApi.get(id).pipe(
            map((customer) => ({ customer, error: null as string | null })),
            catchError((error: unknown) =>
              of({
                customer: null,
                error:
                  error instanceof ApiError && error.status === 404
                    ? 'No se encontró el cliente.'
                    : 'No se pudo cargar el cliente. Inténtalo de nuevo.',
              }),
            ),
          );
        }),
      )
      .subscribe(({ customer, error }) => {
        this.customer.set(customer);
        this.customerError.set(error);
        this.loadingCustomer.set(false);
        if (customer) this.form.updateValueAndValidity({ emitEvent: true });
        else this.invalidatePreview();
      });

    merge(
      this.form.valueChanges.pipe(
        startWith(this.form.getRawValue()),
        map(() => ({ force: false })),
      ),
      this.previewRetry.pipe(map(() => ({ force: true }))),
    )
      .pipe(
        map((trigger) => ({ ...trigger, request: this.makeRequest() })),
        distinctUntilChanged(
          (a, b) => !b.force && JSON.stringify(a.request) === JSON.stringify(b.request),
        ),
        tap(({ request }) => {
          this.generation++;
          this.currentRequest = request;
          this.stale.set(true);
          this.saved.set(null);
          this.errorMessage.set(null);
          this.fxUnavailable.set(false);
          this.preparing.set(!!request);
          this.calculating.set(false);
        }),
        switchMap((request) => {
          if (!request.request || !this.customer()) return of(null);
          const generation = this.generation;
          return timer(250).pipe(
            tap(() => {
              if (generation === this.generation) {
                this.preparing.set(false);
                this.calculating.set(true);
              }
            }),
            switchMap(() => this.simulationsApi.preview(request.request!)),
            map((result) => ({ result, error: null as unknown, generation })),
            catchError((error: unknown) => of({ result: null, error, generation })),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((outcome) => {
        if (!outcome) return;
        if (outcome.generation !== this.generation) return;
        this.preparing.set(false);
        this.calculating.set(false);
        if (outcome.error) {
          this.errorMessage.set(
            outcome.error instanceof ApiError && outcome.error.status === 503
              ? 'No se pudo obtener un tipo de cambio. Conservamos tus datos; reintenta o selecciona EUR.'
              : 'No se pudo calcular la estimación. Revisa los datos e inténtalo de nuevo.',
          );
          this.fxUnavailable.set(outcome.error instanceof ApiError && outcome.error.status === 503);
          this.stale.set(true);
          return;
        }
        this.preview.set(outcome.result);
        this.stale.set(false);
        this.errorMessage.set(null);
      });
  }

  protected sliderEnabled(): boolean {
    const value = this.form.controls.user_count.value;
    return value !== null && Number.isInteger(value) && value >= 0 && value <= 1000;
  }
  protected sliderValue(): number {
    const value = this.form.controls.user_count.value;
    return value !== null && value >= 0 && value <= 1000 ? value : 0;
  }
  protected setSlider(value: number): void {
    this.form.controls.user_count.setValue(value);
    this.form.controls.user_count.markAsTouched();
  }
  protected bandCounts(): readonly [number, number, number] {
    const count = this.form.controls.user_count.value;
    if (count === null || !Number.isInteger(count) || count < 0) return [0, 0, 0];
    return [Math.min(count, 10), Math.min(Math.max(count - 10, 0), 40), Math.max(count - 50, 0)];
  }
  protected countryName(code: string): string {
    return (
      (
        {
          ES: 'España',
          PT: 'Portugal',
          FR: 'Francia',
          DE: 'Alemania',
          IT: 'Italia',
          NL: 'Países Bajos',
        } as Record<string, string>
      )[code] ?? code
    );
  }
  protected fieldError(field: 'user_count' | 'storage_gb' | 'api_calls_per_month'): string {
    const control = this.form.controls[field];
    if (control.hasError('required')) return 'Este campo es obligatorio.';
    if (control.hasError('integer')) return 'Introduce un número entero.';
    if (control.hasError('min')) return 'El valor mínimo es 0.';
    if (control.hasError('max'))
      return `El valor máximo es ${field === 'api_calls_per_month' ? '1.000.000.000' : '1.000.000'}.`;
    return 'Introduce un número válido.';
  }
  protected statusMessage(): string {
    if (this.saving()) return 'Guardando simulación…';
    if (this.preparing()) return 'Preparando nueva estimación…';
    if (this.calculating()) return 'Calculando estimación…';
    if (this.form.invalid) return 'Completa los campos correctamente para calcular.';
    if (this.stale() && this.preview()) return 'Preparando una estimación actualizada…';
    if (this.preview() && !this.stale()) return 'Estimación actualizada.';
    return 'Preparando estimación…';
  }
  protected canSave(): boolean {
    return (
      !!this.customer() &&
      !!this.currentRequest &&
      this.form.valid &&
      !this.stale() &&
      !this.preparing() &&
      !this.calculating() &&
      !this.saving() &&
      !!this.preview()
    );
  }
  protected retryCustomer(): void {
    this.customerRetry.next();
  }
  protected retryPreview(): void {
    if (this.currentRequest && this.customer()) {
      this.stale.set(true);
      this.previewRetry.next();
    }
  }
  protected selectEur(): void {
    this.form.controls.display_currency.setValue('EUR');
  }
  protected save(): void {
    if (!this.canSave() || !this.currentRequest) return;
    const request = this.currentRequest;
    this.saving.set(true);
    this.saveUncertain.set(false);
    this.form.disable();
    this.simulationsApi
      .create(request)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (result) => {
          const previousPreview = this.preview();
          const changed =
            !!previousPreview &&
            (result.total_eur !== previousPreview.total_eur ||
              result.converted_total !== previousPreview.converted_total);
          this.saved.set(result);
          this.preview.set(result);
          this.stale.set(false);
          this.saving.set(false);
          this.form.enable();
          this.form.markAsPristine();
          if (changed)
            this.errorMessage.set(
              'El importe definitivo se ha actualizado con el cálculo recibido al guardar.',
            );
          this.document.defaultView?.requestAnimationFrame(() =>
            this.document.querySelector('h1')?.focus(),
          );
        },
        error: (error: unknown) => {
          this.saving.set(false);
          this.form.enable();
          this.errorMessage.set(
            error instanceof ApiError && error.status > 0
              ? error.message
              : 'No se recibió respuesta al guardar; la simulación podría haberse persistido. Consulta el historial antes de reintentar.',
          );
          this.saveUncertain.set(!(error instanceof ApiError) || error.status === 0);
        },
      });
  }
  private makeRequest(): SimulationPreviewRequest | null {
    const client = this.customer();
    const value = this.form.getRawValue();
    if (
      !client ||
      this.form.invalid ||
      value.user_count === null ||
      value.storage_gb === null ||
      value.api_calls_per_month === null
    )
      return null;
    return {
      customer_id: client.id,
      user_count: value.user_count,
      storage_gb: value.storage_gb,
      api_calls_per_month: value.api_calls_per_month,
      display_currency: value.display_currency,
    };
  }
  private invalidatePreview(): void {
    this.generation++;
    this.currentRequest = null;
    this.stale.set(true);
    this.preparing.set(false);
    this.calculating.set(false);
    this.previewRetry.next();
  }
}
