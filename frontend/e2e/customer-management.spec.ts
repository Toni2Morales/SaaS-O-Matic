import { expect, test } from '@playwright/test';
import { resolve } from 'node:path';

const customerId = '00000000-0000-4000-8000-000000000001';

function customer(overrides: Record<string, unknown> = {}) {
  return {
    id: customerId,
    legal_name: 'Empresa de prueba',
    tax_id: 'B12345674',
    email: 'contacto@example.com',
    country: 'ES',
    plan: 'standard',
    created_at: '2026-11-18T12:00:00Z',
    ...overrides,
  };
}

function historyRecord(id: string, overrides: Record<string, unknown> = {}) {
  return {
    id,
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

test('shows real-shaped dashboard data and only the supplied count and capabilities', async ({
  page,
}) => {
  await page.route('**/api/customers**', (route) =>
    route.fulfill({
      json: {
        items: [customer()],
        total: 37,
        limit: 6,
        offset: 0,
      },
    }),
  );
  await page.goto('/');

  await expect(page.getByRole('heading', { name: 'Panel comercial', level: 1 })).toBeVisible();
  await expect(page.getByRole('status', { name: '37 clientes registrados' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Empresa de prueba' })).toBeVisible();
  await expect(
    page.getByText('España, Portugal, Francia, Alemania, Italia y Países Bajos'),
  ).toBeVisible();
  await expect(page.getByText('EUR, USD y GBP para las simulaciones')).toBeVisible();
  await expect(page.getByText(/MRR|ingresos|crecimiento comercial/i)).toHaveCount(0);
});

test('searches with debounce, keeps server pagination, and requests the current page', async ({
  page,
}) => {
  const requests: string[] = [];
  await page.route('**/api/customers**', async (route) => {
    const url = new URL(route.request().url());
    requests.push(`${url.pathname}${url.search}`);
    const offset = Number(url.searchParams.get('offset') ?? '0');
    const search = url.searchParams.get('search');
    if (search === 'École') {
      const items =
        offset === 0
          ? [customer({ legal_name: 'École Internationale', id: customerId })]
          : [customer({ legal_name: 'École du Sud', id: '00000000-0000-4000-8000-000000000002' })];
      await route.fulfill({ json: { items, total: 21, limit: 20, offset } });
      return;
    }
    await route.fulfill({ json: { items: [], total: 0, limit: 20, offset } });
  });

  await page.goto('/customers');
  await expect(page.getByText('No hay clientes')).toHaveCount(0);
  const search = page.getByRole('searchbox', {
    name: 'Buscar por razón social o identificador fiscal',
  });
  await search.fill('  École  ');
  await expect(page.getByText('École Internationale')).toBeVisible();
  await expect(page.getByText('21 resultados')).toBeVisible();
  await page.getByRole('button', { name: 'Página siguiente' }).click();
  await expect(page.getByText('École du Sud')).toBeVisible();
  expect(
    requests.some(
      (request) => request.includes('search=%C3%89cole') && request.includes('offset=0'),
    ),
  ).toBe(true);
  expect(
    requests.some(
      (request) => request.includes('search=%C3%89cole') && request.includes('offset=20'),
    ),
  ).toBe(true);
  await search.fill('No existe');
  await expect(page.getByText('No hay coincidencias')).toBeVisible();
  await expect(page.getByText('0 resultados')).toBeVisible();
});

test('registers an international customer and navigates only after a successful response', async ({
  page,
}) => {
  let receivedBody: Record<string, unknown> | null = null;
  await page.route('**/api/customers**', async (route) => {
    const request = route.request();
    const url = new URL(request.url());
    if (request.method() === 'POST' && url.pathname === '/api/customers') {
      receivedBody = request.postDataJSON() as Record<string, unknown>;
      await route.fulfill({
        status: 201,
        json: customer({ legal_name: 'Empresa Portugal', tax_id: 'PT-ACME 2026', country: 'PT' }),
      });
      return;
    }
    if (url.pathname === `/api/customers/${customerId}/simulations`) {
      await route.fulfill({ json: { items: [], total: 0, limit: 10, offset: 0 } });
      return;
    }
    if (url.pathname.startsWith('/api/customers/')) {
      await route.fulfill({
        json: customer({ legal_name: 'Empresa Portugal', tax_id: 'PT-ACME 2026', country: 'PT' }),
      });
      return;
    }
    await route.fulfill({ json: { items: [], total: 0, limit: 20, offset: 0 } });
  });

  await page.goto('/customers/new');
  await page.getByLabel('Razón social').fill('  Empresa Portugal  ');
  await page.getByRole('combobox', { name: 'País' }).click();
  await page.getByRole('option', { name: 'Portugal' }).click();
  await page.getByLabel('Identificador fiscal').fill('PT-ACME 2026');
  await page.getByLabel('Email de contacto').fill(' contacto@example.com ');
  await page.getByRole('button', { name: 'Guardar cliente' }).click();

  await expect(page).toHaveURL(new RegExp(`/customers/${customerId}$`));
  await expect(page.getByRole('status').filter({ hasText: 'creado correctamente' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Empresa Portugal' })).toBeVisible();
  expect(receivedBody).toEqual({
    legal_name: 'Empresa Portugal',
    tax_id: 'PT-ACME 2026',
    email: 'contacto@example.com',
    country: 'PT',
    plan: 'standard',
  });
  await expect(page.getByText('Aún no hay simulaciones guardadas')).toBeVisible();
});

test('shows 409 and 422 responses without clearing or exposing unknown error extensions', async ({
  page,
}) => {
  let submission = 0;
  await page.route('**/api/customers', async (route) => {
    if (route.request().method() !== 'POST') {
      await route.fulfill({ json: { items: [], total: 0, limit: 20, offset: 0 } });
      return;
    }
    submission += 1;
    if (submission === 1) {
      await route.fulfill({
        status: 409,
        contentType: 'application/problem+json',
        body: JSON.stringify({
          type: 'about:blank',
          title: 'Duplicado',
          status: 409,
          detail: 'Duplicate internal detail',
        }),
      });
    } else {
      await route.fulfill({
        status: 422,
        contentType: 'application/problem+json',
        body: JSON.stringify({
          type: 'about:blank',
          title: 'Invalid',
          status: 422,
          detail: 'Revisa los datos introducidos.',
          errors: [
            { field: 'body.tax_id', message: 'Identificador sintético inválido' },
            { field: 'internal.password', message: 'secret' },
          ],
        }),
      });
    }
  });

  await page.goto('/customers/new');
  await page.getByLabel('Razón social').fill('Empresa Sintética');
  await page.getByRole('combobox', { name: 'País' }).click();
  await page.getByRole('option', { name: 'España' }).click();
  await page.getByLabel('Identificador fiscal').fill('B12345674');
  await page.getByLabel('Email de contacto').fill('contacto@example.com');
  await page.getByRole('button', { name: 'Guardar cliente' }).click();
  await expect(page.getByRole('alert')).toContainText('Ya existe un cliente');
  await expect(page.getByLabel('Razón social')).toHaveValue('Empresa Sintética');

  await page.getByRole('button', { name: 'Guardar cliente' }).click();
  await expect(page.getByText('Identificador sintético inválido')).toBeVisible();
  await expect(page.getByText('secret')).toHaveCount(0);
  await expect(page.getByLabel('Identificador fiscal')).toHaveValue('B12345674');
});

test('renders historical nulls as unknown while preserving real zeros and exact snapshots', async ({
  page,
}) => {
  const records = [
    historyRecord('00000000-0000-4000-8000-000000000003', {
      user_count: 0,
      storage_gb: 0,
      api_calls_per_month: 0,
      user_subtotal_eur: '0.00',
      created_at: '2026-11-18T12:00:00Z',
    }),
    historyRecord('00000000-0000-4000-8000-000000000002', {
      user_count: 15,
      storage_gb: 250,
      api_calls_per_month: 100000,
      user_subtotal_eur: '140.00',
      created_at: '2025-04-12T10:00:00Z',
    }),
    historyRecord('00000000-0000-4000-8000-000000000001', {
      user_count: 5,
      user_subtotal_eur: '50.00',
      created_at: '2024-01-02T10:00:00Z',
      total_eur: '60.50',
      tax_amount_eur: '10.50',
      display_currency: 'USD',
      exchange_rate: '1.234567890123456789',
      exchange_rate_date: '2026-11-17',
      converted_total: '74.69',
      tax_country: 'ES',
      tax_rate: '0.21',
      tax_source: 'fixture',
      tax_catalog_version: 'test-v1',
      tax_verified_on: '2026-11-18',
      tax_territory: 'Península y Baleares',
      exchange_rate_obtained_at: '2026-11-18T11:00:00Z',
      exchange_rate_source: 'Frankfurter (fixture)',
    }),
  ];
  await page.route(`**/api/customers/${customerId}`, (route) =>
    route.fulfill({ json: customer() }),
  );
  await page.route(`**/api/customers/${customerId}/simulations**`, (route) =>
    route.fulfill({ json: { items: records, total: 3, limit: 10, offset: 0 } }),
  );
  await page.goto(`/customers/${customerId}`);

  await expect(page.getByRole('heading', { name: 'Empresa de prueba' })).toBeVisible();
  await expect(page.getByText('0,00\u00a0€').first()).toBeVisible();
  await expect(page.getByText('0 GB', { exact: true })).toBeVisible();
  await expect(page.getByText('No registrado').first()).toBeVisible();
  await page.getByText('Ver datos del snapshot').last().click();
  await expect(page.getByText('1,234567890123456789')).toBeVisible();
  await expect(page.getByText('74,69\u00a0US$')).toBeVisible();
  await expect(page.getByText('2 ene 2024')).toBeVisible();
});

test('keeps detail available when history returns an error', async ({ page }) => {
  await page.route(`**/api/customers/${customerId}/simulations**`, (route) => route.abort());
  await page.route(`**/api/customers/${customerId}`, (route) =>
    route.fulfill({ json: customer() }),
  );
  await page.goto(`/customers/${customerId}`);
  await expect(page.getByRole('heading', { name: 'Empresa de prueba' })).toBeVisible();
  await expect(
    page.getByRole('alert').filter({ hasText: 'No se pudo conectar con el servidor' }),
  ).toBeVisible();
});

test('integrates customer registration, lookup, detail, history, and persistence with FastAPI and SQLite', async ({
  page,
  request,
}) => {
  test.skip(
    process.env['TASK042_REAL_API'] !== '1',
    'Requires the isolated FastAPI/SQLite test services.',
  );
  const register = async (legalName: string, country: 'ES' | 'PT', taxId: string) => {
    await page.goto('/customers/new');
    await page.getByLabel('Razón social').fill(legalName);
    await page.getByRole('combobox', { name: 'País' }).click();
    await page.getByRole('option', { name: country === 'ES' ? 'España' : 'Portugal' }).click();
    await page.getByLabel('Identificador fiscal').fill(taxId);
    await page.getByLabel('Email de contacto').fill('qa@example.com');
    await page.getByRole('button', { name: 'Guardar cliente' }).click();
    await expect(page).toHaveURL(/\/customers\/[0-9a-f-]+$/i);
    await expect(page.getByRole('heading', { name: legalName })).toBeVisible();
    await expect(page.getByText('Aún no hay simulaciones guardadas')).toBeVisible();
    const match = /\/customers\/([^/]+)$/.exec(new URL(page.url()).pathname);
    if (!match?.[1]) throw new Error('The created customer route did not include an id.');
    return match[1];
  };

  const spanishId = await register('TASK042 Empresa de Prueba ES', 'ES', 'B 123-45674');
  await page.goto('/customers');
  await page
    .getByRole('searchbox', { name: 'Buscar por razón social o identificador fiscal' })
    .fill('TASK042 Empresa de Prueba ES');
  await expect(page.getByRole('link', { name: 'TASK042 Empresa de Prueba ES' })).toBeVisible();
  await page.getByRole('link', { name: 'TASK042 Empresa de Prueba ES' }).click();
  await expect(page.getByRole('heading', { name: 'TASK042 Empresa de Prueba ES' })).toBeVisible();
  await page.reload();
  await expect(page.getByRole('heading', { name: 'TASK042 Empresa de Prueba ES' })).toBeVisible();

  await page.goto(`/customers/${spanishId}/simulations/new`);
  await expect(page.getByText('España')).toBeVisible();
  const referenceUsers = page.locator('#user-count');
  await referenceUsers.fill('15');
  await page.getByRole('spinbutton', { name: 'Almacenamiento contratado (GB)' }).fill('250');
  await page.getByRole('spinbutton', { name: 'Llamadas API mensuales' }).fill('100000');
  await page.getByRole('combobox', { name: 'Divisa de visualización' }).click();
  await page.getByRole('option', { name: 'EUR — Euro' }).click();
  await expect(page.locator('.total')).toHaveText('169,40 €');
  await expect(page.getByText('29,40 €')).toBeVisible();
  await page.keyboard.press('Escape');
  await page.locator('h1').last().click();
  if (process.env['TASK043_SCREENSHOT_DIR']) {
    await page.screenshot({
      path: resolve(process.env['TASK043_SCREENSHOT_DIR'], 'TASK043-simulador-desktop.png'),
      fullPage: true,
    });
  }
  const emptyHistory = await request.get(
    `http://127.0.0.1:8000/customers/${spanishId}/simulations`,
  );
  expect(emptyHistory.status()).toBe(200);
  expect((await emptyHistory.json()).total).toBe(0);
  await referenceUsers.fill('20');
  await referenceUsers.fill('30');
  await expect(page.locator('.total')).toHaveText('314,60 €');
  const stillEmptyHistory = await request.get(
    `http://127.0.0.1:8000/customers/${spanishId}/simulations`,
  );
  expect((await stillEmptyHistory.json()).total).toBe(0);
  await referenceUsers.fill('15');
  await expect(page.locator('.total')).toHaveText('169,40 €');
  await page.getByRole('button', { name: 'Guardar simulación' }).click();
  await expect(page.getByText(/Simulación guardada/)).toBeVisible();
  await page.getByRole('link', { name: 'Ver ficha e historial' }).click();
  await expect(page.getByRole('heading', { name: 'Historial de simulaciones' })).toBeVisible();
  await expect(
    page.locator('app-simulation-history').getByRole('link', { name: 'Nueva simulación' }),
  ).toHaveAttribute('href', `/customers/${spanishId}/simulations/new`);
  const savedHistory = await request.get(
    `http://127.0.0.1:8000/customers/${spanishId}/simulations`,
  );
  expect((await savedHistory.json()).total).toBe(1);
  await expect(page.getByText('169,40 €').last()).toBeVisible();
  if (process.env['TASK043_SCREENSHOT_DIR']) {
    await page.screenshot({
      path: resolve(process.env['TASK043_SCREENSHOT_DIR'], 'TASK043-historial-actualizado.png'),
      fullPage: true,
    });
  }
  await page.reload();
  await expect(page.getByText('169,40 €').last()).toBeVisible();

  await page.goto(`/customers/${spanishId}/simulations/new`);
  await referenceUsers.fill('0');
  await expect(page.locator('.total')).toHaveText('0,00 €');

  await page.goto('/customers/new');
  await page.getByLabel('Razón social').fill('Empresa duplicada sintética');
  await page.getByRole('combobox', { name: 'País' }).click();
  await page.getByRole('option', { name: 'España' }).click();
  await page.getByLabel('Identificador fiscal').fill('B12345674');
  await page.getByLabel('Email de contacto').fill('qa@example.com');
  await page.getByRole('button', { name: 'Guardar cliente' }).click();
  await expect(page.getByRole('alert')).toContainText('Ya existe un cliente');
  await expect(page.getByLabel('Identificador fiscal')).toHaveValue('B12345674');

  const internationalId = await register(
    'TASK042 Empresa Sintética PT',
    'PT',
    'PT-TASK042-TEST-001',
  );
  expect(internationalId).not.toBe(spanishId);
  await page.goto(`/customers/${internationalId}/simulations/new`);
  await expect(page.getByText('Portugal')).toBeVisible();
  await expect(page.locator('.total')).toHaveText('172,20 €');

  const response = await request.post('http://127.0.0.1:8000/simulations', {
    data: {
      customer_id: spanishId,
      user_count: 5,
      storage_gb: 10,
      api_calls_per_month: 100,
      display_currency: 'EUR',
    },
  });
  expect(response.status()).toBe(201);
  for (const currency of ['USD', 'GBP'] as const) {
    const fxResponse = await request.post('http://127.0.0.1:8000/simulations/preview', {
      data: {
        customer_id: spanishId,
        user_count: 15,
        storage_gb: 250,
        api_calls_per_month: 100000,
        display_currency: currency,
      },
      timeout: 10000,
    });
    expect([200, 503]).toContain(fxResponse.status());
    console.log(
      `TASK043 puntual FX ${currency}: HTTP ${fxResponse.status()} ${fxResponse.status() === 200 ? JSON.stringify(await fxResponse.json()) : JSON.stringify(await fxResponse.json())}`,
    );
  }
  await page.goto(`/customers/${spanishId}`);
  await page.reload();
  await expect(page.getByText('50,00\u00a0€')).toBeVisible();
  await expect(page.getByText('60,50\u00a0€').first()).toBeVisible();
});
