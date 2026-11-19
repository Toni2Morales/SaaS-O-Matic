import { provideRouter } from '@angular/router';
import { TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { ApiError } from '../../core/http/api-error';
import { CustomerResponse } from '../../shared/models/api.models';
import { CustomersApiService } from '../customers/data-access/customers-api.service';
import { DashboardPageComponent } from './dashboard-page';

const sampleCustomer: CustomerResponse = {
  id: '00000000-0000-4000-8000-000000000001',
  legal_name: 'Empresa de prueba',
  tax_id: 'B12345674',
  email: 'contacto@example.com',
  country: 'ES',
  plan: 'standard',
  created_at: '2026-11-18T12:00:00Z',
};

describe('DashboardPageComponent', () => {
  it('uses the paginated response total and a bounded customer selection', async () => {
    const api = {
      list: vi
        .fn()
        .mockReturnValue(of({ items: [sampleCustomer], total: 42, limit: 6, offset: 0 })),
    };
    await TestBed.configureTestingModule({
      imports: [DashboardPageComponent],
      providers: [provideRouter([]), { provide: CustomersApiService, useValue: api }],
    }).compileComponents();

    const fixture = TestBed.createComponent(DashboardPageComponent);
    fixture.detectChanges();
    await fixture.whenStable();

    expect(api.list).toHaveBeenCalledExactlyOnceWith(6, 0, '');
    expect(fixture.nativeElement.textContent).toContain('42');
    expect(fixture.nativeElement.textContent).toContain('Empresa de prueba');
    expect(fixture.nativeElement.textContent).not.toContain('MRR');
    expect(fixture.nativeElement.textContent).toContain(
      'no representa el orden de altas recientes',
    );
  });

  it('distinguishes a real empty result from an API error', async () => {
    const api = { list: vi.fn().mockReturnValue(of({ items: [], total: 0, limit: 6, offset: 0 })) };
    await TestBed.configureTestingModule({
      imports: [DashboardPageComponent],
      providers: [provideRouter([]), { provide: CustomersApiService, useValue: api }],
    }).compileComponents();
    const fixture = TestBed.createComponent(DashboardPageComponent);
    fixture.detectChanges();
    await fixture.whenStable();
    expect(fixture.nativeElement.textContent).toContain('Todavía no hay clientes');
    expect(fixture.nativeElement.querySelector('.customer-total').getAttribute('aria-label')).toBe(
      '0 clientes registrados',
    );

    fixture.destroy();
    const failingApi = {
      list: vi.fn().mockReturnValue(throwError(() => new ApiError(500, 'Servicio no disponible.'))),
    };
    TestBed.resetTestingModule();
    await TestBed.configureTestingModule({
      imports: [DashboardPageComponent],
      providers: [provideRouter([]), { provide: CustomersApiService, useValue: failingApi }],
    }).compileComponents();
    const failedFixture = TestBed.createComponent(DashboardPageComponent);
    failedFixture.detectChanges();
    await failedFixture.whenStable();
    expect(failedFixture.nativeElement.textContent).toContain('Servicio no disponible.');
  });
});
