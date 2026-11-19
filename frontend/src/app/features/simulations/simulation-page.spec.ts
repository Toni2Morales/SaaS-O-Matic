import { provideRouter } from '@angular/router';
import { TestBed } from '@angular/core/testing';
import { Observable, of, throwError } from 'rxjs';
import { ApiError } from '../../core/http/api-error';
import {
  CustomerResponse,
  SimulationPreviewResponse,
  SimulationResponse,
} from '../../shared/models/api.models';
import { CustomersApiService } from '../customers/data-access/customers-api.service';
import { SimulationsApiService } from './data-access/simulations-api.service';
import { SimulationPageComponent } from './simulation-page';

const customerId = '00000000-0000-4000-8000-000000000045';
const customer: CustomerResponse = {
  id: customerId,
  legal_name: 'Empresa TASK045B sintética',
  tax_id: 'B12345674',
  email: 'audit@example.com',
  country: 'ES',
  plan: 'standard',
  created_at: '2026-11-19T10:00:00Z',
};

function estimate(currency: 'EUR' | 'USD' = 'EUR'): SimulationPreviewResponse {
  return {
    customer_id: customerId,
    user_count: 15,
    user_subtotal_eur: '140.00',
    storage_gb: 250,
    api_calls_per_month: 100000,
    billing_period: 'monthly',
    tax_country: 'ES',
    tax_rate: '0.21',
    tax_source: 'Agencia Tributaria (fixture)',
    tax_catalog_version: 'TASK045B-fixture',
    tax_verified_on: '2026-11-17',
    tax_territory: 'Península y Baleares',
    tax_effective_from: null,
    tax_amount_eur: '29.40',
    total_eur: '169.40',
    display_currency: currency,
    exchange_rate: currency === 'EUR' ? '1' : '1.0998',
    exchange_rate_date: currency === 'EUR' ? null : '2026-11-18',
    exchange_rate_obtained_at: '2026-11-19T10:00:00Z',
    exchange_rate_source: currency === 'EUR' ? 'identity' : 'Frankfurter (fixture)',
    converted_total: currency === 'EUR' ? '169.40' : '186.31',
  };
}

async function setup(preview: (currency: 'EUR' | 'USD') => Observable<SimulationPreviewResponse>) {
  const customersApi = { get: vi.fn().mockReturnValue(of(customer)) };
  const simulationsApi = {
    preview: vi.fn((request: { display_currency: 'EUR' | 'USD' }) =>
      preview(request.display_currency),
    ),
    create: vi.fn().mockReturnValue(
      of({
        ...estimate(),
        id: '00000000-0000-4000-8000-000000000046',
        created_at: '2026-11-19T10:01:00Z',
      } satisfies SimulationResponse),
    ),
  };
  await TestBed.configureTestingModule({
    imports: [SimulationPageComponent],
    providers: [
      provideRouter([]),
      { provide: CustomersApiService, useValue: customersApi },
      { provide: SimulationsApiService, useValue: simulationsApi },
    ],
  }).compileComponents();
  const fixture = TestBed.createComponent(SimulationPageComponent);
  fixture.componentRef.setInput('customerId', customerId);
  return { fixture, simulationsApi };
}

describe('SimulationPageComponent terminal preview states', () => {
  it('does not leave a preparation announcement when the first FX preview fails', async () => {
    const { fixture, simulationsApi } = await setup(() =>
      throwError(() => new ApiError(503, 'FX unavailable')),
    );
    fixture.detectChanges();
    expect(fixture.componentInstance.customer()).toEqual(customer);
    fixture.componentInstance.form.controls.display_currency.setValue('USD');
    await vi.waitFor(() =>
      expect(simulationsApi.preview).toHaveBeenCalledExactlyOnceWith(
        expect.objectContaining({ customer_id: customerId, display_currency: 'USD' }),
      ),
    );
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('.status').textContent.trim()).toBe('');
    expect(fixture.nativeElement.querySelector('[role="alert"]').textContent).toContain(
      'No se pudo obtener un tipo de cambio',
    );
    expect(fixture.nativeElement.querySelector('button[mat-flat-button]')?.disabled).toBe(true);
  });

  it('keeps an old preview explicitly stale after FX failure and recovers by manual retry', async () => {
    let failFx = false;
    const simulationsApiPreview = (currency: 'EUR' | 'USD') =>
      failFx && currency === 'USD'
        ? throwError(() => new ApiError(503, 'FX unavailable'))
        : of(estimate(currency));
    const { fixture, simulationsApi } = await setup(simulationsApiPreview);
    fixture.detectChanges();
    await vi.waitFor(() => expect(simulationsApi.preview).toHaveBeenCalledTimes(1));
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('.total').textContent).toContain('169,40');

    failFx = true;
    fixture.componentInstance.form.controls.display_currency.setValue('USD');
    fixture.detectChanges();
    await vi.waitFor(() => expect(simulationsApi.preview).toHaveBeenCalledTimes(2));
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('.status').textContent.trim()).toBe('');
    expect(fixture.nativeElement.textContent).toContain('No se pudo obtener un tipo de cambio');
    expect(fixture.nativeElement.textContent).toContain(
      'Estimación anterior: los parámetros han cambiado.',
    );
    expect(fixture.nativeElement.querySelector('button[mat-flat-button]')?.disabled).toBe(true);

    failFx = false;
    const retry = fixture.nativeElement.querySelector('.notice.error button') as HTMLButtonElement;
    retry.click();
    await vi.waitFor(() => expect(simulationsApi.preview).toHaveBeenCalledTimes(3));
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('.status').textContent).toContain(
      'Estimación actualizada.',
    );
    expect(fixture.nativeElement.querySelector('.total').textContent).toContain('186,31');
  });

  it('clears a previous save error after a later successful save', async () => {
    const { fixture, simulationsApi } = await setup(() => of(estimate()));
    simulationsApi.create
      .mockReturnValueOnce(throwError(() => new ApiError(500, 'El servidor no pudo guardar.')))
      .mockReturnValueOnce(
        of({
          ...estimate(),
          id: '00000000-0000-4000-8000-000000000047',
          created_at: '2026-11-19T10:02:00Z',
        } satisfies SimulationResponse),
      );
    fixture.detectChanges();
    await vi.waitFor(() => expect(simulationsApi.preview).toHaveBeenCalledTimes(1));
    fixture.detectChanges();
    const save = fixture.nativeElement.querySelector(
      'button[mat-flat-button]',
    ) as HTMLButtonElement;

    save.click();
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('[role="alert"]').textContent).toContain(
      'El servidor no pudo guardar.',
    );
    expect(save.disabled).toBe(false);

    save.click();
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('[role="alert"]')).toBeNull();
    expect(fixture.nativeElement.textContent).toContain(
      'Simulación guardada. Resultado definitivo:',
    );
  });
});
