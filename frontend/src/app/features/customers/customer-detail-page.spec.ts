import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';
import { ApiError } from '../../core/http/api-error';
import { CustomerResponse, SimulationHistoryPageResponse } from '../../shared/models/api.models';
import { CustomersApiService } from './data-access/customers-api.service';
import { SimulationHistoryApiService } from './data-access/simulation-history-api.service';
import { CustomerDetailPageComponent } from './customer-detail-page';

const customerId = '00000000-0000-4000-8000-000000000001';
const customer: CustomerResponse = {
  id: customerId,
  legal_name: 'Empresa de prueba',
  tax_id: 'B12345674',
  email: 'contacto@example.com',
  country: 'ES',
  plan: 'standard',
  created_at: '2026-11-18T12:00:00Z',
};

describe('CustomerDetailPageComponent', () => {
  it('shows the real customer while presenting an independent history failure', async () => {
    const customersApi = { get: vi.fn().mockReturnValue(of(customer)) };
    const historyApi = {
      getPage: vi
        .fn()
        .mockReturnValue(
          throwError(() => new ApiError(500, 'Historial temporalmente no disponible.')),
        ),
    };
    await TestBed.configureTestingModule({
      imports: [CustomerDetailPageComponent],
      providers: [
        provideRouter([]),
        { provide: CustomersApiService, useValue: customersApi },
        { provide: SimulationHistoryApiService, useValue: historyApi },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(CustomerDetailPageComponent);
    fixture.componentRef.setInput('customerId', customerId);
    fixture.detectChanges();
    await fixture.whenStable();

    expect(customersApi.get).toHaveBeenCalledExactlyOnceWith(customerId);
    expect(historyApi.getPage).toHaveBeenCalledExactlyOnceWith(customerId, 10, 0);
    expect(fixture.nativeElement.textContent).toContain('Empresa de prueba');
    expect(fixture.nativeElement.textContent).toContain('contacto@example.com');
    expect(fixture.nativeElement.textContent).toContain('Historial temporalmente no disponible.');
    expect(fixture.nativeElement.textContent).not.toContain('Cliente no encontrado');
  });

  it('renders an actual 404 as not found and sends no history query', async () => {
    const customersApi = {
      get: vi
        .fn()
        .mockReturnValue(
          throwError(() => new ApiError(404, 'No se encontró el recurso solicitado.')),
        ),
    };
    const historyApi = {
      getPage: vi
        .fn()
        .mockReturnValue(
          of({ items: [], total: 0, limit: 10, offset: 0 } satisfies SimulationHistoryPageResponse),
        ),
    };
    await TestBed.configureTestingModule({
      imports: [CustomerDetailPageComponent],
      providers: [
        provideRouter([]),
        { provide: CustomersApiService, useValue: customersApi },
        { provide: SimulationHistoryApiService, useValue: historyApi },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(CustomerDetailPageComponent);
    fixture.componentRef.setInput('customerId', customerId);
    fixture.detectChanges();
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).toContain('Cliente no encontrado');
    expect(historyApi.getPage).not.toHaveBeenCalled();
  });

  it('rejects a malformed UUID before making a detail request', async () => {
    const customersApi = { get: vi.fn() };
    const historyApi = { getPage: vi.fn() };
    await TestBed.configureTestingModule({
      imports: [CustomerDetailPageComponent],
      providers: [
        provideRouter([]),
        { provide: CustomersApiService, useValue: customersApi },
        { provide: SimulationHistoryApiService, useValue: historyApi },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(CustomerDetailPageComponent);
    fixture.componentRef.setInput('customerId', 'not-a-uuid');
    fixture.detectChanges();
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).toContain('no tiene un formato válido');
    expect(customersApi.get).not.toHaveBeenCalled();
    expect(historyApi.getPage).not.toHaveBeenCalled();
  });
});
