import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';
import { ApiError } from '../../core/http/api-error';
import {
  HistoricalSimulationResponse,
  SimulationHistoryPageResponse,
} from '../../shared/models/api.models';
import { SimulationHistoryApiService } from './data-access/simulation-history-api.service';
import { SimulationHistoryComponent } from './simulation-history';

const customerId = '00000000-0000-4000-8000-000000000001';

function historical(
  id: number,
  overrides: Partial<HistoricalSimulationResponse>,
): HistoricalSimulationResponse {
  return {
    id: `00000000-0000-4000-8000-${String(id).padStart(12, '0')}`,
    customer_id: customerId,
    user_count: 0,
    storage_gb: null,
    api_calls_per_month: null,
    billing_period: 'monthly',
    user_subtotal_eur: '0.00',
    created_at: null,
    tax_country: null,
    tax_rate: null,
    tax_source: null,
    tax_catalog_version: null,
    tax_verified_on: null,
    tax_territory: null,
    tax_effective_from: null,
    tax_amount_eur: null,
    total_eur: null,
    display_currency: null,
    exchange_rate: null,
    exchange_rate_date: null,
    exchange_rate_obtained_at: null,
    exchange_rate_source: null,
    converted_total: null,
    ...overrides,
  };
}

function historyPage(items: HistoricalSimulationResponse[]): SimulationHistoryPageResponse {
  return { items, total: items.length, limit: 10, offset: 0 };
}

describe('SimulationHistoryComponent', () => {
  it('renders old generations with unknown data rather than substituting zero or a current value', async () => {
    const beforeConsumptionAndSnapshot = historical(1, {
      user_count: 5,
      user_subtotal_eur: '50.00',
      created_at: '2024-01-02T10:00:00Z',
    });
    const consumptionWithoutSnapshot = historical(2, {
      user_count: 0,
      storage_gb: 0,
      api_calls_per_month: 0,
      user_subtotal_eur: '0.00',
      created_at: '2025-04-12T10:00:00Z',
    });
    const fullSnapshot = historical(3, {
      user_count: 15,
      storage_gb: 250,
      api_calls_per_month: 100000,
      user_subtotal_eur: '140.00',
      created_at: '2026-11-18T12:00:00Z',
      tax_country: 'ES',
      tax_rate: '0.21',
      tax_source: 'fuente sintética',
      tax_catalog_version: 'test-v1',
      tax_verified_on: '2026-11-18',
      tax_territory: 'Península y Baleares',
      tax_amount_eur: '29.40',
      total_eur: '169.40',
      display_currency: 'USD',
      exchange_rate: '1.234567890123456789',
      exchange_rate_date: '2026-11-17',
      exchange_rate_obtained_at: '2026-11-18T11:00:00Z',
      exchange_rate_source: 'Frankfurter (fixture)',
      converted_total: '209.14',
    });
    const api = {
      getPage: vi
        .fn()
        .mockReturnValue(
          of(historyPage([fullSnapshot, consumptionWithoutSnapshot, beforeConsumptionAndSnapshot])),
        ),
    };
    await TestBed.configureTestingModule({
      imports: [SimulationHistoryComponent],
      providers: [provideRouter([]), { provide: SimulationHistoryApiService, useValue: api }],
    }).compileComponents();

    const fixture = TestBed.createComponent(SimulationHistoryComponent);
    fixture.componentRef.setInput('customerId', customerId);
    fixture.detectChanges();
    await fixture.whenStable();

    expect(api.getPage).toHaveBeenCalledExactlyOnceWith(customerId, 10, 0);
    expect(fixture.nativeElement.textContent).toContain('No registrado');
    expect(fixture.nativeElement.textContent).toContain('0 GB');
    expect(fixture.nativeElement.textContent).toContain('0,00\u00a0€');
    expect(fixture.nativeElement.textContent).toContain('140,00\u00a0€');
    expect(fixture.nativeElement.textContent).toContain('209,14\u00a0US$');
    expect(fixture.nativeElement.textContent).not.toContain('0,00\u00a0US$');
    expect(fixture.nativeElement.textContent).not.toContain('Total EUR</dt><dd>50,00');
    expect(fixture.nativeElement.querySelector('details')).not.toBeNull();
    expect(fixture.nativeElement.querySelector('.history-header a').getAttribute('href')).toBe(
      `/customers/${customerId}/simulations/new`,
    );
  });

  it('keeps a history error local and provides an explicit retry', async () => {
    const api = {
      getPage: vi
        .fn()
        .mockReturnValueOnce(
          throwError(() => new ApiError(500, 'No se pudo completar la solicitud.')),
        )
        .mockReturnValueOnce(of(historyPage([]))),
    };
    await TestBed.configureTestingModule({
      imports: [SimulationHistoryComponent],
      providers: [provideRouter([]), { provide: SimulationHistoryApiService, useValue: api }],
    }).compileComponents();
    const fixture = TestBed.createComponent(SimulationHistoryComponent);
    fixture.componentRef.setInput('customerId', customerId);
    fixture.detectChanges();
    await fixture.whenStable();
    expect(fixture.nativeElement.textContent).toContain('No se pudo completar la solicitud.');

    fixture.nativeElement.querySelector('.retry-button').click();
    fixture.detectChanges();
    await fixture.whenStable();
    expect(api.getPage).toHaveBeenCalledTimes(2);
    expect(fixture.nativeElement.textContent).toContain('Aún no hay simulaciones guardadas');
  });

  it('requests history pages from the server using the selected offset', async () => {
    const first = historical(4, {
      user_count: 1,
      user_subtotal_eur: '10.00',
      created_at: '2026-11-18T12:00:00Z',
    });
    const later = historical(5, {
      user_count: 2,
      user_subtotal_eur: '20.00',
      created_at: '2026-11-17T12:00:00Z',
    });
    const api = {
      getPage: vi
        .fn()
        .mockImplementation((_id: string, limit: number, offset: number) =>
          of({ items: [offset === 0 ? first : later], total: 11, limit, offset }),
        ),
    };
    await TestBed.configureTestingModule({
      imports: [SimulationHistoryComponent],
      providers: [provideRouter([]), { provide: SimulationHistoryApiService, useValue: api }],
    }).compileComponents();
    const fixture = TestBed.createComponent(SimulationHistoryComponent);
    fixture.componentRef.setInput('customerId', customerId);
    fixture.detectChanges();
    await fixture.whenStable();

    fixture.nativeElement.querySelector('[aria-label="Página siguiente del historial"]').click();
    fixture.detectChanges();
    await fixture.whenStable();

    expect(api.getPage).toHaveBeenNthCalledWith(1, customerId, 10, 0);
    expect(api.getPage).toHaveBeenNthCalledWith(2, customerId, 10, 10);
    expect(fixture.nativeElement.textContent).toContain('20,00\u00a0€');
  });
});
