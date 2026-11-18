import { provideRouter } from '@angular/router';
import { TestBed } from '@angular/core/testing';
import { of, Subject } from 'rxjs';
import { CustomerPageResponse, CustomerResponse } from '../../shared/models/api.models';
import { CustomersApiService } from './data-access/customers-api.service';
import { CustomersPageComponent } from './customers-page';

const customer = (id: string, legalName: string): CustomerResponse => ({
  id,
  legal_name: legalName,
  tax_id: 'PT-ACME 2026',
  email: 'contacto@example.com',
  country: 'PT',
  plan: 'standard',
  created_at: '2026-11-18T12:00:00Z',
});

const page = (
  items: CustomerResponse[],
  total: number,
  limit = 20,
  offset = 0,
): CustomerPageResponse => ({
  items,
  total,
  limit,
  offset,
});

describe('CustomersPageComponent', () => {
  afterEach(() => vi.useRealTimers());

  it('shows the backend total, uses server pagination, and keeps the filter on page change', async () => {
    const api = {
      list: vi
        .fn()
        .mockImplementation((_limit: number, offset: number) =>
          of(
            offset === 0
              ? page([customer('00000000-0000-4000-8000-000000000001', 'Empresa A')], 21)
              : page(
                  [customer('00000000-0000-4000-8000-000000000002', 'Empresa B')],
                  21,
                  20,
                  offset,
                ),
          ),
        ),
    };
    await TestBed.configureTestingModule({
      imports: [CustomersPageComponent],
      providers: [provideRouter([]), { provide: CustomersApiService, useValue: api }],
    }).compileComponents();
    const fixture = TestBed.createComponent(CustomersPageComponent);
    fixture.detectChanges();
    await fixture.whenStable();

    expect(api.list).toHaveBeenNthCalledWith(1, 20, 0, '');
    expect(fixture.nativeElement.textContent).toContain('21 resultados');
    vi.useFakeTimers();
    fixture.componentInstance.searchControl.setValue('  Empresa  ');
    await vi.advanceTimersByTimeAsync(300);
    fixture.detectChanges();
    expect(api.list).toHaveBeenNthCalledWith(2, 20, 0, 'Empresa');

    fixture.componentInstance.nextPage();
    fixture.detectChanges();
    expect(api.list).toHaveBeenNthCalledWith(3, 20, 20, 'Empresa');
    expect(fixture.nativeElement.textContent).toContain('Empresa B');
  });

  it('cancels an in-flight older search so its late response cannot replace current results', async () => {
    const initial = new Subject<CustomerPageResponse>();
    const oldSearch = new Subject<CustomerPageResponse>();
    const newSearch = new Subject<CustomerPageResponse>();
    const api = {
      list: vi.fn().mockImplementation((_limit: number, _offset: number, search: string) => {
        if (search === 'Antiguo') return oldSearch;
        if (search === 'Actual') return newSearch;
        return initial;
      }),
    };
    await TestBed.configureTestingModule({
      imports: [CustomersPageComponent],
      providers: [provideRouter([]), { provide: CustomersApiService, useValue: api }],
    }).compileComponents();
    const fixture = TestBed.createComponent(CustomersPageComponent);
    fixture.detectChanges();
    initial.next(page([], 0));
    fixture.detectChanges();

    vi.useFakeTimers();
    fixture.componentInstance.searchControl.setValue('Antiguo');
    await vi.advanceTimersByTimeAsync(300);
    fixture.componentInstance.searchControl.setValue('Actual');
    await vi.advanceTimersByTimeAsync(300);
    newSearch.next(
      page([customer('00000000-0000-4000-8000-000000000003', 'Resultado actual')], 1, 20, 0),
    );
    oldSearch.next(
      page([customer('00000000-0000-4000-8000-000000000004', 'Resultado obsoleto')], 1, 20, 0),
    );
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Resultado actual');
    expect(fixture.nativeElement.textContent).not.toContain('Resultado obsoleto');
  });
});
