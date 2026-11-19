import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import {
  FormControl,
  NonNullableFormBuilder,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { finalize } from 'rxjs';
import { ApiError } from '../../core/http/api-error';
import {
  CountryCode,
  CustomerCreateRequest,
  PlanCode,
  ProblemFieldError,
} from '../../shared/models/api.models';
import { SectionHeadingComponent } from '../../shared/components/section-heading';
import { CustomersApiService } from './data-access/customers-api.service';
import { trimmedEmail, trimmedLegalName, trimmedRequired } from './customer-form.validators';

type CustomerField = 'legal_name' | 'tax_id' | 'email' | 'country' | 'plan';

const countries: { code: CountryCode; name: string }[] = [
  { code: 'ES', name: 'España' },
  { code: 'PT', name: 'Portugal' },
  { code: 'FR', name: 'Francia' },
  { code: 'DE', name: 'Alemania' },
  { code: 'IT', name: 'Italia' },
  { code: 'NL', name: 'Países Bajos' },
];

@Component({
  imports: [
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    ReactiveFormsModule,
    RouterLink,
    SectionHeadingComponent,
  ],
  template: `
    <div class="create-page">
      <app-section-heading
        title="Datos de la empresa"
        description="Registra una empresa para consultar sus datos y preparar estimaciones más adelante."
      />

      <form class="customer-form" [formGroup]="form" (ngSubmit)="submit()" novalidate>
        <p class="required-note">
          <span aria-hidden="true">*</span> Todos los campos son obligatorios.
        </p>

        @if (formError()) {
          <div class="form-error" role="alert" tabindex="-1">
            <strong>No se pudo registrar el cliente</strong>
            <p>{{ formError() }}</p>
          </div>
        }

        <div class="form-grid">
          <mat-form-field appearance="outline" class="wide-field">
            <mat-label>Razón social</mat-label>
            <input
              matInput
              formControlName="legal_name"
              autocomplete="organization"
              required
              aria-describedby="legal-name-help"
              (input)="clearServerError('legal_name')"
            />
            <mat-hint id="legal-name-help"
              >Entre 1 y 255 caracteres después de quitar espacios exteriores.</mat-hint
            >
            @if (showError(form.controls.legal_name)) {
              <mat-error>{{ fieldMessage('legal_name') }}</mat-error>
            }
            @if (serverFieldErrors()['legal_name']) {
              <mat-error>{{ serverFieldErrors()['legal_name'] }}</mat-error>
            }
          </mat-form-field>

          <mat-form-field appearance="outline">
            <mat-label>País</mat-label>
            <mat-select
              formControlName="country"
              required
              (selectionChange)="clearServerError('country')"
            >
              @for (country of countries; track country.code) {
                <mat-option [value]="country.code">{{ country.name }}</mat-option>
              }
            </mat-select>
            @if (showError(form.controls.country)) {
              <mat-error>Selecciona un país.</mat-error>
            }
            @if (serverFieldErrors()['country']) {
              <mat-error>{{ serverFieldErrors()['country'] }}</mat-error>
            }
          </mat-form-field>

          <mat-form-field appearance="outline">
            <mat-label>Identificador fiscal</mat-label>
            <input
              matInput
              formControlName="tax_id"
              autocomplete="off"
              required
              aria-describedby="tax-id-help"
              (input)="clearServerError('tax_id')"
            />
            <mat-hint id="tax-id-help">{{ taxIdHelp() }}</mat-hint>
            @if (showError(form.controls.tax_id)) {
              <mat-error>Introduce el identificador fiscal.</mat-error>
            }
            @if (serverFieldErrors()['tax_id']) {
              <mat-error>{{ serverFieldErrors()['tax_id'] }}</mat-error>
            }
          </mat-form-field>

          <mat-form-field appearance="outline" class="wide-field">
            <mat-label>Email de contacto</mat-label>
            <input
              matInput
              type="email"
              formControlName="email"
              autocomplete="email"
              required
              (input)="clearServerError('email')"
            />
            @if (showError(form.controls.email)) {
              <mat-error>{{ fieldMessage('email') }}</mat-error>
            }
            @if (serverFieldErrors()['email']) {
              <mat-error>{{ serverFieldErrors()['email'] }}</mat-error>
            }
          </mat-form-field>

          <mat-form-field appearance="outline">
            <mat-label>Plan</mat-label>
            <mat-select
              formControlName="plan"
              required
              (selectionChange)="clearServerError('plan')"
            >
              <mat-option value="standard">Standard</mat-option>
            </mat-select>
            <mat-hint>Único plan disponible en esta versión.</mat-hint>
            @if (showError(form.controls.plan)) {
              <mat-error>Selecciona el plan disponible.</mat-error>
            }
            @if (serverFieldErrors()['plan']) {
              <mat-error>{{ serverFieldErrors()['plan'] }}</mat-error>
            }
          </mat-form-field>
        </div>

        <div class="form-footer">
          <a mat-button routerLink="/customers" [attr.aria-disabled]="submitting()">Cancelar</a>
          <button mat-flat-button color="primary" type="submit" [disabled]="submitting()">
            @if (submitting()) {
              Guardando…
            } @else {
              Guardar cliente
            }
          </button>
        </div>
        <p class="privacy-note">
          Los datos fiscales y de contacto se envían al servidor para el registro. No se muestran en
          los mensajes de error.
        </p>
      </form>
    </div>
  `,
  styles: `
    :host {
      display: block;
    }
    .create-page {
      display: grid;
      gap: var(--space-6);
    }
    .customer-form {
      display: grid;
      gap: var(--space-5);
      max-width: 58rem;
      padding: clamp(var(--space-4), 4vw, var(--space-8));
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      background: var(--color-surface);
      box-shadow: var(--shadow-sm);
    }
    .required-note {
      margin: 0;
      color: var(--color-text-muted);
      font-size: 0.85rem;
    }
    .required-note span {
      color: var(--color-error);
      font-weight: 700;
    }
    .form-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: var(--space-4) var(--space-5);
    }
    mat-form-field {
      width: 100%;
      min-width: 0;
    }
    .wide-field {
      grid-column: 1 / -1;
    }
    .form-error {
      padding: var(--space-4);
      border: 1px solid #fecaca;
      border-radius: var(--radius-sm);
      color: #7f1d1d;
      background: #fef2f2;
    }
    .form-error p {
      margin: var(--space-1) 0 0;
      line-height: 1.5;
    }
    .form-footer {
      display: flex;
      justify-content: flex-end;
      gap: var(--space-3);
      padding-top: var(--space-2);
      border-top: 1px solid var(--color-border);
    }
    .form-footer a,
    .form-footer button {
      min-height: 2.75rem;
    }
    .privacy-note {
      margin: 0;
      color: var(--color-text-muted);
      font-size: 0.76rem;
      line-height: 1.5;
    }
    @media (max-width: 620px) {
      .form-grid {
        grid-template-columns: 1fr;
      }
      .wide-field {
        grid-column: auto;
      }
    }
    @media (max-width: 400px) {
      .form-footer {
        flex-direction: column-reverse;
      }
      .form-footer a,
      .form-footer button {
        width: 100%;
      }
    }
  `,
})
export class CustomerCreatePageComponent {
  private readonly formBuilder = inject(NonNullableFormBuilder);
  private readonly customersApi = inject(CustomersApiService);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);

  readonly countries = countries;
  readonly submitting = signal(false);
  readonly submitted = signal(false);
  readonly formError = signal<string | null>(null);
  readonly serverFieldErrors = signal<Partial<Record<CustomerField, string>>>({});
  readonly form = this.formBuilder.group({
    legal_name: this.formBuilder.control('', [trimmedLegalName]),
    tax_id: this.formBuilder.control('', [trimmedRequired]),
    email: this.formBuilder.control('', [Validators.required, trimmedEmail]),
    country: this.formBuilder.control<CountryCode | ''>('', [Validators.required]),
    plan: this.formBuilder.control<PlanCode>('standard', [Validators.required]),
  });

  taxIdHelp(): string {
    return this.form.controls.country.value === 'ES'
      ? 'Para España, el servidor valida DNI/NIF, NIE o CIF.'
      : 'Se aplicará la validación genérica del país; no es una comprobación fiscal oficial.';
  }

  showError(
    control: FormControl<string> | FormControl<CountryCode | ''> | FormControl<PlanCode>,
  ): boolean {
    return control.invalid && (control.touched || this.submitted());
  }

  fieldMessage(field: 'legal_name' | 'email'): string {
    const control = this.form.controls[field];
    if (control.hasError('required')) {
      return field === 'legal_name'
        ? 'Introduce la razón social.'
        : 'Introduce un email de contacto.';
    }
    if (field === 'legal_name' && control.hasError('maxlength')) {
      return 'La razón social no puede superar los 255 caracteres después del recorte.';
    }
    if (field === 'email' && control.hasError('email')) {
      return 'Introduce un email con formato válido.';
    }
    return 'Revisa este campo.';
  }

  clearServerError(field: CustomerField): void {
    const control = this.form.controls[field];
    if (control.errors?.['server']) {
      const remainingErrors = { ...control.errors };
      delete remainingErrors['server'];
      control.setErrors(Object.keys(remainingErrors).length > 0 ? remainingErrors : null);
    }
    if (this.serverFieldErrors()[field]) {
      this.serverFieldErrors.update((errors) => {
        const next = { ...errors };
        delete next[field];
        return next;
      });
    }
    if (this.formError()) {
      this.formError.set(null);
    }
  }

  submit(): void {
    this.submitted.set(true);
    this.formError.set(null);
    this.serverFieldErrors.set({});
    if (this.submitting()) {
      return;
    }
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const values = this.form.getRawValue();
    if (!isCountryCode(values.country)) {
      this.form.controls.country.setErrors({ required: true });
      this.form.controls.country.markAsTouched();
      return;
    }

    const request: CustomerCreateRequest = {
      legal_name: values.legal_name.trim(),
      tax_id: values.tax_id,
      email: values.email.trim(),
      country: values.country,
      plan: values.plan,
    };

    this.submitting.set(true);
    this.customersApi
      .create(request)
      .pipe(
        finalize(() => this.submitting.set(false)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe({
        next: (customer) => {
          void this.router.navigate(['/customers', customer.id], {
            state: { customerCreated: true },
          });
        },
        error: (error: unknown) => this.handleSubmitError(error),
      });
  }

  private handleSubmitError(error: unknown): void {
    if (!(error instanceof ApiError)) {
      this.formError.set(
        'No se pudo confirmar el resultado. La solicitud podría haberse procesado; comprueba el listado antes de volver a enviarla.',
      );
      return;
    }

    if (error.status === 409) {
      this.formError.set(
        'Ya existe un cliente con ese identificador fiscal en el país seleccionado. Comprueba el listado.',
      );
      return;
    }

    if (error.status === 422) {
      const mapped: Partial<Record<CustomerField, string>> = {};
      for (const fieldError of error.problem?.errors ?? []) {
        const field = customerFieldFromProblem(fieldError);
        if (field) {
          mapped[field] = fieldError.message;
          const control = this.form.controls[field];
          control.setErrors({ ...control.errors, server: true });
          control.markAsTouched();
        }
      }
      this.serverFieldErrors.set(mapped);
      this.formError.set(
        Object.keys(mapped).length > 0
          ? 'Revisa los campos indicados y vuelve a intentarlo.'
          : 'El servidor rechazó algunos datos. Revisa el formulario e inténtalo de nuevo.',
      );
      return;
    }

    if (error.status === 0) {
      this.formError.set(
        'No se pudo confirmar el resultado. La solicitud podría haberse procesado; comprueba el listado antes de volver a enviarla.',
      );
      return;
    }

    this.formError.set(error.message);
  }
}

function isCountryCode(value: string): value is CountryCode {
  return countries.some((country) => country.code === value);
}

function customerFieldFromProblem(error: ProblemFieldError): CustomerField | null {
  const field = error.field.split('.').at(-1);
  return field === 'legal_name' ||
    field === 'tax_id' ||
    field === 'email' ||
    field === 'country' ||
    field === 'plan'
    ? field
    : null;
}
