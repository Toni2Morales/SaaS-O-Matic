import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { API_BASE_URL } from '../config/api.config';
import { ApiError } from './api-error';
import { ApiClient } from './api-client';
import { apiErrorInterceptor } from './api-error.interceptor';
import { CustomerCreateRequest, SimulationPreviewRequest } from '../../shared/models/api.models';

describe('ApiClient', () => {
  let client: ApiClient;
  let httpTesting: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(withInterceptors([apiErrorInterceptor])),
        provideHttpClientTesting(),
        { provide: API_BASE_URL, useValue: '/api' },
      ],
    });
    client = TestBed.inject(ApiClient);
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpTesting.verify());

  it('uses the central API prefix and typed customer page parameters', () => {
    client.getCustomersPage(10, 20, 'École').subscribe((page) => {
      expect(page.total).toBe(0);
      expect(page.items).toEqual([]);
    });

    const request = httpTesting.expectOne((candidate) => candidate.url === '/api/customers');
    expect(request.request.method).toBe('GET');
    expect(request.request.params.get('limit')).toBe('10');
    expect(request.request.params.get('offset')).toBe('20');
    expect(request.request.params.get('search')).toBe('École');
    request.flush({ items: [], total: 0, limit: 10, offset: 20 });
  });

  it('normalizes a controlled service error without retrying the request', () => {
    let received: unknown;
    client.getCustomersPage().subscribe({ error: (error: unknown) => (received = error) });

    const request = httpTesting.expectOne('/api/customers?limit=20&offset=0');
    request.flush(
      {
        type: 'about:blank',
        title: 'Unavailable',
        status: 503,
        detail: 'provider detail must not be exposed',
      },
      { status: 503, statusText: 'Service Unavailable' },
    );

    expect(received).toBeInstanceOf(ApiError);
    expect((received as ApiError).status).toBe(503);
    expect((received as ApiError).message).toBe('El servicio no está disponible temporalmente.');
    expect((received as ApiError).message).not.toContain('provider detail');
    httpTesting.expectNone('/api/customers?limit=20&offset=0');
  });

  it('posts a typed customer request without changing its fiscal identifier', () => {
    const payload: CustomerCreateRequest = {
      legal_name: 'Empresa Internacional',
      tax_id: 'PT-ACME 2026',
      email: 'contacto@example.test',
      country: 'PT',
      plan: 'standard',
    };
    client.createCustomer(payload).subscribe((customer) => {
      expect(customer.id).toBe('00000000-0000-4000-8000-000000000001');
      expect(customer.tax_id).toBe(payload.tax_id);
    });

    const request = httpTesting.expectOne('/api/customers');
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual(payload);
    request.flush({
      ...payload,
      id: '00000000-0000-4000-8000-000000000001',
      created_at: '2026-11-18T12:00:00Z',
    });
  });

  it('fetches a customer detail and its independently paginated history', () => {
    const customerId = '00000000-0000-4000-8000-000000000001';
    client.getCustomer(customerId).subscribe((customer) => expect(customer.country).toBe('ES'));
    const detail = httpTesting.expectOne(`/api/customers/${customerId}`);
    expect(detail.request.method).toBe('GET');
    detail.flush({
      id: customerId,
      legal_name: 'Empresa Ejemplo',
      tax_id: 'B12345674',
      email: 'contacto@example.test',
      country: 'ES',
      plan: 'standard',
      created_at: '2026-11-18T12:00:00Z',
    });

    client.getCustomerSimulationsPage(customerId, 10, 20).subscribe((page) => {
      expect(page.total).toBe(20);
      expect(page.items).toEqual([]);
    });
    const history = httpTesting.expectOne(
      `/api/customers/${customerId}/simulations?limit=10&offset=20`,
    );
    expect(history.request.method).toBe('GET');
    history.flush({ items: [], total: 20, limit: 10, offset: 20 });
  });

  it('uses only the existing preview and create simulation contracts', () => {
    const payload: SimulationPreviewRequest = {
      customer_id: '00000000-0000-4000-8000-000000000001',
      user_count: 15,
      storage_gb: 250,
      api_calls_per_month: 100000,
      display_currency: 'EUR',
    };
    client
      .previewSimulation(payload)
      .subscribe((result) => expect(result.user_subtotal_eur).toBe('140.00'));
    const preview = httpTesting.expectOne('/api/simulations/preview');
    expect(preview.request.method).toBe('POST');
    expect(preview.request.body).toEqual(payload);
    preview.flush({ user_subtotal_eur: '140.00' });

    client.createSimulation(payload).subscribe((result) => expect(result.id).toBe('simulation-id'));
    const create = httpTesting.expectOne('/api/simulations');
    expect(create.request.method).toBe('POST');
    expect(create.request.body).toEqual(payload);
    create.flush({ id: 'simulation-id' });
  });
});
