import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { expect, test } from '@playwright/test';

const customerId = '00000000-0000-4000-8000-000000000044';
const screenshotDirectory = process.env['TASK044_SCREENSHOT_DIR'];
const syntheticCustomer = {
  id: customerId,
  legal_name: 'Empresa sintética TASK044',
  tax_id: 'B12345674',
  email: 'qa@example.test',
  country: 'ES',
  plan: 'standard',
  created_at: '2026-11-19T10:00:00Z',
};

const amounts: Record<number, { subtotal: string; tax: string; total: string }> = {
  0: { subtotal: '0.00', tax: '0.00', total: '0.00' },
  15: { subtotal: '140.00', tax: '29.40', total: '169.40' },
  16: { subtotal: '148.00', tax: '31.08', total: '179.08' },
};

function simulation(currency: string, users: number) {
  const amount = amounts[users];
  if (!amount) throw new Error(`No hay fixture de referencia para ${users} usuarios.`);
  const converted =
    currency === 'EUR'
      ? amount.total
      : currency === 'USD'
        ? users === 16
          ? '196.95'
          : users === 0
            ? '0.00'
            : '186.31'
        : users === 16
          ? '149.26'
          : users === 0
            ? '0.00'
            : '141.19';
  return {
    customer_id: customerId,
    user_count: users,
    user_subtotal_eur: amount.subtotal,
    storage_gb: 250,
    api_calls_per_month: 100000,
    billing_period: 'monthly',
    tax_country: 'ES',
    tax_rate: '0.21',
    tax_source: 'Agencia Tributaria (fixture sintético)',
    tax_catalog_version: 'TASK044-fixture',
    tax_verified_on: '2026-11-17',
    tax_territory: 'Península y Baleares',
    tax_effective_from: null,
    tax_amount_eur: amount.tax,
    total_eur: amount.total,
    display_currency: currency,
    exchange_rate: currency === 'EUR' ? '1' : currency === 'USD' ? '1.0998' : '0.83348',
    exchange_rate_date: currency === 'EUR' ? null : '2026-11-18',
    exchange_rate_obtained_at: '2026-11-19T10:00:00Z',
    exchange_rate_source: currency === 'EUR' ? 'identity' : 'Frankfurter (fixture)',
    converted_total: converted,
  };
}

test('captures TASK044 interface evidence using deterministic intercepted APIs', async ({
  page,
}) => {
  test.skip(
    !screenshotDirectory,
    'Define TASK044_SCREENSHOT_DIR con una carpeta temporal fuera del repositorio.',
  );
  mkdirSync(resolve(screenshotDirectory!), { recursive: true });
  let customer = { ...syntheticCustomer };
  let history: Record<string, unknown>[] = [];
  let fxUnavailable = false;

  await page.route('**/api/customers**', async (route) => {
    const url = new URL(route.request().url());
    if (route.request().method() === 'POST' && url.pathname === '/api/customers') {
      const body = route.request().postDataJSON() as typeof customer;
      customer = { ...body, id: customerId, created_at: '2026-11-19T10:00:00Z' };
      return route.fulfill({ status: 201, json: customer });
    }
    if (url.pathname === `/api/customers/${customerId}`) {
      return route.fulfill({ json: customer });
    }
    if (url.pathname === `/api/customers/${customerId}/simulations`) {
      const limit = Number(url.searchParams.get('limit') ?? 10);
      const offset = Number(url.searchParams.get('offset') ?? 0);
      return route.fulfill({
        json: {
          items: history.slice(offset, offset + limit),
          total: history.length,
          limit,
          offset,
        },
      });
    }
    return route.fulfill({ json: { items: [customer], total: 1, limit: 20, offset: 0 } });
  });
  await page.route('**/api/simulations/preview', async (route) => {
    const body = route.request().postDataJSON() as { display_currency: string; user_count: number };
    if (fxUnavailable && body.display_currency !== 'EUR') {
      return route.fulfill({
        status: 503,
        contentType: 'application/problem+json',
        json: {
          type: 'about:blank',
          title: 'Unavailable',
          status: 503,
          detail: 'Proveedor FX sintético no disponible.',
        },
      });
    }
    return route.fulfill({ json: simulation(body.display_currency, body.user_count) });
  });
  await page.route('**/api/simulations', async (route) => {
    const body = route.request().postDataJSON() as { display_currency: string; user_count: number };
    const created = {
      ...simulation(body.display_currency, body.user_count),
      id: `00000000-0000-4000-8000-${String(history.length + 1).padStart(12, '0')}`,
      created_at: '2026-11-19T10:01:00Z',
    };
    history = [created, ...history];
    return route.fulfill({ status: 201, json: created });
  });

  const screenshot = async (
    name: string,
    scrollTarget?: string,
    options: { dismissOverlays?: boolean; allowSkipLinkFocus?: boolean } = {},
  ) => {
    if (options.dismissOverlays !== false) await page.keyboard.press('Escape');
    if (options.dismissOverlays !== false) await expect(page.getByRole('listbox')).toHaveCount(0);
    if (scrollTarget) await page.locator(scrollTarget).scrollIntoViewIfNeeded();
    else await page.evaluate(() => window.scrollTo(0, 0));
    if (options.allowSkipLinkFocus !== true) {
      await expect(
        page.getByRole('link', { name: 'Saltar al contenido principal' }),
      ).not.toBeFocused();
    }
    await page.screenshot({ path: resolve(screenshotDirectory!, name), fullPage: false });
  };

  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Panel comercial', level: 1 })).toBeVisible();
  await screenshot('TASK044-dashboard-desktop.png');
  await page.setViewportSize({ width: 390, height: 844 });
  await screenshot('TASK044-dashboard-mobile.png');

  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/customers');
  await expect(page.getByRole('heading', { name: 'Listado de clientes' })).toBeVisible();
  await screenshot('TASK044-clientes-desktop.png');
  await page.setViewportSize({ width: 390, height: 844 });
  await screenshot('TASK044-clientes-mobile.png');

  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto('/customers/new');
  await page.getByLabel('Razón social').fill(customer.legal_name);
  await page.getByRole('combobox', { name: 'País' }).click();
  await page.getByRole('option', { name: 'España' }).click();
  await page.getByLabel('Identificador fiscal').fill(customer.tax_id);
  await page.getByLabel('Email de contacto').fill(customer.email);
  await screenshot('TASK044-registro-desktop.png');
  await page.setViewportSize({ width: 390, height: 844 });
  await screenshot('TASK044-registro-mobile.png');
  await page.getByRole('button', { name: 'Guardar cliente' }).click();
  await expect(page).toHaveURL(`/customers/${customerId}`);
  await expect(page.getByRole('heading', { name: customer.legal_name })).toBeVisible();
  await screenshot('TASK044-ficha-historial-desktop.png');
  await page.setViewportSize({ width: 390, height: 844 });
  await screenshot('TASK044-ficha-historial-mobile.png', 'app-simulation-history');

  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto(`/customers/${customerId}/simulations/new`);
  await expect(page.locator('.total')).toHaveText('169,40 €');
  await screenshot('TASK044-simulador-desktop.png');
  await page.setViewportSize({ width: 390, height: 844 });
  await screenshot('TASK044-simulador-mobile.png');
  await expect(page.locator('.mobile-estimate')).toContainText('169,40 €');
  await expect(page.locator('.mobile-estimate')).toHaveCSS('position', 'static');
  await screenshot('TASK044-simulador-mobile-resumen.png', '.mobile-estimate');

  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto(`/customers/${customerId}/simulations/new`);
  await page.getByRole('spinbutton', { name: 'Almacenamiento contratado (GB)' }).fill('250');
  await page.getByRole('spinbutton', { name: 'Llamadas al servicio / mes' }).fill('100000');
  await expect(page.locator('.total')).toHaveText('169,40 €');
  await screenshot('TASK044-simulador-15-usuarios.png');
  await page.locator('#user-count').fill('16');
  await expect(page.locator('.total')).toHaveText('179,08 €');
  await screenshot('TASK044-simulador-16-usuarios.png');

  const currency = page.getByRole('combobox', { name: 'Divisa de visualización' });
  await currency.click();
  await page.getByRole('option', { name: 'USD — Dólar estadounidense' }).click();
  await expect(page.locator('.total')).toHaveText('196,95 US$');
  await page.locator('details').locator('summary').click();
  await screenshot('TASK044-simulador-usd.png');
  await currency.click();
  await page.getByRole('option', { name: 'GBP — Libra esterlina' }).click();
  await expect(page.locator('.total')).toHaveText('149,26 £');
  await page.locator('details').locator('summary').click();
  await screenshot('TASK044-simulador-gbp.png');

  await page.locator('#user-count').fill('1000001');
  await page.locator('#user-count').blur();
  await expect(page.getByText('El valor máximo es 1.000.000.')).toBeVisible();
  await expect(page.locator('.tiers')).toHaveCount(0);
  await screenshot('TASK044-simulador-validacion.png');

  await page.locator('#user-count').fill('16');
  fxUnavailable = true;
  await expect(page.getByText(/No se pudo obtener un tipo de cambio/)).toBeVisible();
  await screenshot('TASK044-simulador-error-fx.png');
  fxUnavailable = false;
  await page.getByRole('button', { name: 'Reintentar estimación' }).click();
  await expect(page.locator('.total')).toHaveText('149,26 £');
  await page.getByRole('button', { name: 'Guardar simulación' }).click();
  await expect(page.getByText(/Simulación guardada/)).toBeVisible();
  await screenshot('TASK044-simulacion-guardada.png');

  await page.getByRole('link', { name: 'Ver ficha e historial' }).click();
  await expect(page.getByText('1 simulación')).toBeVisible();
  await screenshot('TASK044-historial-persistido.png', 'app-simulation-history');

  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.getByRole('button', { name: 'Menú' }).click();
  await expect(page.getByRole('button', { name: 'Cerrar menú' })).toBeVisible();
  await screenshot('TASK044-menu-mobile.png', undefined, { dismissOverlays: false });

  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: 'Saltar al contenido principal' })).toBeFocused();
  await screenshot('TASK044-foco-teclado.png', undefined, { allowSkipLinkFocus: true });
});
