import { provideLocationMocks } from '@angular/common/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { TestBed } from '@angular/core/testing';
import { routes } from './app.routes';
import { CustomerCreatePageComponent } from './features/customers/customer-create-page';
import { NotFoundPageComponent } from './features/not-found/not-found-page';

describe('application routes', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [provideRouter(routes), provideLocationMocks()] });
  });

  it('loads the customer preparation route directly', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/customers/new', CustomerCreatePageComponent);

    expect(page).toBeInstanceOf(CustomerCreatePageComponent);
    expect(harness.routeNativeElement?.textContent).toContain('Nuevo cliente');
    expect(harness.routeNativeElement?.textContent).toContain('Todos los campos son obligatorios');
  });

  it('renders an explicit not-found page for unknown routes', async () => {
    const harness = await RouterTestingHarness.create();
    const page = await harness.navigateByUrl('/unknown/route', NotFoundPageComponent);

    expect(page).toBeInstanceOf(NotFoundPageComponent);
    expect(harness.routeNativeElement?.textContent).toContain('No encontramos esta página');
  });
});
