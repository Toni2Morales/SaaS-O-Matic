import { provideRouter, Router } from '@angular/router';
import { TestBed } from '@angular/core/testing';
import { of, Subject, throwError } from 'rxjs';
import { ApiError } from '../../core/http/api-error';
import { CustomerCreateRequest, CustomerResponse } from '../../shared/models/api.models';
import { CustomersApiService } from './data-access/customers-api.service';
import { CustomerCreatePageComponent } from './customer-create-page';

const createdCustomer: CustomerResponse = {
  id: '00000000-0000-4000-8000-000000000001',
  legal_name: 'Empresa de prueba',
  tax_id: 'PT-ACME 2026',
  email: 'contacto@example.com',
  country: 'PT',
  plan: 'standard',
  created_at: '2026-11-18T12:00:00Z',
};

function fillValidForm(component: CustomerCreatePageComponent): void {
  component.form.setValue({
    legal_name: '  Empresa de prueba  ',
    tax_id: 'PT-ACME 2026',
    email: ' contacto@example.com ',
    country: 'PT',
    plan: 'standard',
  });
}

describe('CustomerCreatePageComponent', () => {
  it('validates required data and never sends an incomplete request', async () => {
    const api = { create: vi.fn().mockReturnValue(of(createdCustomer)) };
    await TestBed.configureTestingModule({
      imports: [CustomerCreatePageComponent],
      providers: [provideRouter([]), { provide: CustomersApiService, useValue: api }],
    }).compileComponents();
    const fixture = TestBed.createComponent(CustomerCreatePageComponent);
    fixture.detectChanges();

    fixture.componentInstance.submit();
    fixture.detectChanges();

    expect(api.create).not.toHaveBeenCalled();
    expect(fixture.nativeElement.textContent).toContain('Introduce la razón social.');
    expect(fixture.nativeElement.textContent).toContain('Selecciona un país.');
  });

  it('sends the selected international country and explicit standard plan, then navigates only after 201', async () => {
    const api = { create: vi.fn().mockReturnValue(of(createdCustomer)) };
    await TestBed.configureTestingModule({
      imports: [CustomerCreatePageComponent],
      providers: [provideRouter([]), { provide: CustomersApiService, useValue: api }],
    }).compileComponents();
    const fixture = TestBed.createComponent(CustomerCreatePageComponent);
    fixture.detectChanges();
    const router = TestBed.inject(Router);
    const navigate = vi.spyOn(router, 'navigate').mockResolvedValue(true);
    fillValidForm(fixture.componentInstance);
    expect(
      Object.fromEntries(
        Object.entries(fixture.componentInstance.form.controls).map(([key, control]) => [
          key,
          control.errors,
        ]),
      ),
    ).toEqual({ legal_name: null, tax_id: null, email: null, country: null, plan: null });
    expect(fixture.componentInstance.form.valid).toBe(true);
    fixture.componentInstance.submit();
    fixture.detectChanges();
    await fixture.whenStable();

    const expected: CustomerCreateRequest = {
      legal_name: 'Empresa de prueba',
      tax_id: 'PT-ACME 2026',
      email: 'contacto@example.com',
      country: 'PT',
      plan: 'standard',
    };
    expect(api.create).toHaveBeenCalledExactlyOnceWith(expected);
    expect(navigate).toHaveBeenCalledWith(['/customers', createdCustomer.id], {
      state: { customerCreated: true },
    });
  });

  it('preserves entered data on conflict and does not report success', async () => {
    const api = {
      create: vi
        .fn()
        .mockReturnValue(
          throwError(
            () => new ApiError(409, 'La operación entra en conflicto con datos existentes.'),
          ),
        ),
    };
    await TestBed.configureTestingModule({
      imports: [CustomerCreatePageComponent],
      providers: [provideRouter([]), { provide: CustomersApiService, useValue: api }],
    }).compileComponents();
    const fixture = TestBed.createComponent(CustomerCreatePageComponent);
    fixture.detectChanges();
    fillValidForm(fixture.componentInstance);
    expect(fixture.componentInstance.form.valid).toBe(true);
    fixture.componentInstance.submit();
    fixture.detectChanges();

    expect(fixture.componentInstance.form.controls.tax_id.value).toBe('PT-ACME 2026');
    expect(fixture.componentInstance.form.controls.legal_name.value).toBe('  Empresa de prueba  ');
    expect(fixture.componentInstance.formError()).toContain('Ya existe un cliente');
  });

  it('maps only recognized validation fields and keeps unknown details private', async () => {
    const api = {
      create: vi.fn().mockReturnValue(
        throwError(
          () =>
            new ApiError(422, 'Revisa los datos introducidos.', {
              type: 'about:blank',
              title: 'Datos inválidos',
              status: 422,
              detail: 'Revisa los datos introducidos.',
              errors: [
                { field: 'body.email', message: 'Email no válido' },
                { field: 'database.password', message: 'internal-secret' },
              ],
            }),
        ),
      ),
    };
    await TestBed.configureTestingModule({
      imports: [CustomerCreatePageComponent],
      providers: [provideRouter([]), { provide: CustomersApiService, useValue: api }],
    }).compileComponents();
    const fixture = TestBed.createComponent(CustomerCreatePageComponent);
    fixture.detectChanges();
    fillValidForm(fixture.componentInstance);
    expect(fixture.componentInstance.form.valid).toBe(true);
    fixture.componentInstance.submit();
    fixture.detectChanges();

    expect(fixture.componentInstance.serverFieldErrors()).toEqual({ email: 'Email no válido' });
    expect(fixture.nativeElement.textContent).not.toContain('internal-secret');
    expect(fixture.componentInstance.form.controls.email.invalid).toBe(true);
    expect(fixture.componentInstance.form.controls.tax_id.value).toBe('PT-ACME 2026');
  });

  it('prevents concurrent submits while the first create request is pending', async () => {
    const response = new Subject<CustomerResponse>();
    const api = { create: vi.fn().mockReturnValue(response) };
    await TestBed.configureTestingModule({
      imports: [CustomerCreatePageComponent],
      providers: [provideRouter([]), { provide: CustomersApiService, useValue: api }],
    }).compileComponents();
    const fixture = TestBed.createComponent(CustomerCreatePageComponent);
    fixture.detectChanges();
    vi.spyOn(TestBed.inject(Router), 'navigate').mockResolvedValue(true);
    fillValidForm(fixture.componentInstance);

    fixture.componentInstance.submit();
    fixture.componentInstance.submit();
    expect(api.create).toHaveBeenCalledExactlyOnceWith({
      legal_name: 'Empresa de prueba',
      tax_id: 'PT-ACME 2026',
      email: 'contacto@example.com',
      country: 'PT',
      plan: 'standard',
    });
    expect(fixture.componentInstance.submitting()).toBe(true);

    response.next(createdCustomer);
    response.complete();
    await fixture.whenStable();
    expect(fixture.componentInstance.submitting()).toBe(false);
  });

  it('explains an ambiguous transport failure and does not automatically repeat the POST', async () => {
    const api = {
      create: vi
        .fn()
        .mockReturnValue(throwError(() => new ApiError(0, 'No se pudo conectar con el servidor.'))),
    };
    await TestBed.configureTestingModule({
      imports: [CustomerCreatePageComponent],
      providers: [provideRouter([]), { provide: CustomersApiService, useValue: api }],
    }).compileComponents();
    const fixture = TestBed.createComponent(CustomerCreatePageComponent);
    fixture.detectChanges();
    vi.spyOn(TestBed.inject(Router), 'navigate').mockResolvedValue(true);
    fillValidForm(fixture.componentInstance);

    fixture.componentInstance.submit();
    fixture.detectChanges();

    expect(api.create).toHaveBeenCalledTimes(1);
    expect(fixture.componentInstance.formError()).toContain(
      'La solicitud podría haberse procesado',
    );
    expect(fixture.componentInstance.form.controls.legal_name.value).toBe('  Empresa de prueba  ');
  });
});
