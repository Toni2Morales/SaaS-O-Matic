import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { expect, test } from '@playwright/test';

test('integrates the Angular UI with FastAPI and migrated SQLite', async ({
  page,
  request,
}, info) => {
  test.skip(
    process.env['TASK045B_REAL_API'] !== '1',
    'Requires isolated TASK045B FastAPI/SQLite services.',
  );
  test.skip(info.project.name !== 'chromium', 'Persistent integration runs once in Chromium.');
  const api = process.env['TASK045B_API_BASE_URL'] ?? 'http://127.0.0.1:8000';
  const evidence = process.env['TASK045B_REAL_SCREENSHOT_DIR'];
  const companyName = `TASK045B Empresa ES ${Date.now()}`;
  const screenshot = async (name: string): Promise<void> => {
    if (!evidence) return;
    mkdirSync(resolve(evidence), { recursive: true });
    await page.screenshot({ path: resolve(evidence, `real-${name}.png`) });
  };
  const selectCurrency = async (currency: 'EUR' | 'USD' | 'GBP'): Promise<void> => {
    if (currency === 'EUR') return;
    await page.getByRole('combobox', { name: 'Divisa de visualización' }).click();
    await page
      .getByRole('option', {
        name: currency === 'USD' ? 'USD — Dólar estadounidense' : 'GBP — Libra esterlina',
      })
      .click();
  };

  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Panel comercial' })).toBeVisible();
  await screenshot('dashboard');

  await page.goto('/customers/new');
  await page.getByLabel('Razón social').fill(companyName);
  await page.getByRole('combobox', { name: 'País' }).click();
  await page.getByRole('option', { name: 'España' }).click();
  await page.getByLabel('Identificador fiscal').fill('B12345670');
  await page.getByLabel('Email de contacto').fill('audit@example.com');
  await page.getByRole('button', { name: 'Guardar cliente' }).click();
  await expect(page.getByRole('alert')).toBeVisible();
  await expect(page).toHaveURL(/\/customers\/new$/);
  await screenshot('fiscal-es-invalido');
  await page.getByLabel('Identificador fiscal').fill('B12345674');
  await page.getByRole('button', { name: 'Guardar cliente' }).click();
  await expect(page).toHaveURL(/\/customers\/[0-9a-f-]+$/i);
  await expect(page.getByRole('heading', { name: companyName })).toBeVisible();
  await expect(page.getByText('Aún no hay simulaciones guardadas')).toBeVisible();
  const match = /\/customers\/([^/]+)$/.exec(new URL(page.url()).pathname);
  expect(match?.[1]).toBeTruthy();
  const customerId = match![1]!;
  await screenshot('alta-es-ficha-historial-vacio');

  await page.goto('/customers/new');
  await page.getByLabel('Razón social').fill('TASK045B duplicado sintético');
  await page.getByRole('combobox', { name: 'País' }).click();
  await page.getByRole('option', { name: 'España' }).click();
  await page.getByLabel('Identificador fiscal').fill('B12345674');
  await page.getByLabel('Email de contacto').fill('audit@example.com');
  await page.getByRole('button', { name: 'Guardar cliente' }).click();
  await expect(page.getByRole('alert')).toContainText('Ya existe un cliente');

  await page.goto('/customers');
  const search = page.getByRole('searchbox', {
    name: 'Buscar por razón social o identificador fiscal',
  });
  for (const term of [companyName, 'B12345674']) {
    await search.fill(term);
    await expect(page.getByRole('link', { name: companyName })).toBeVisible();
  }
  await screenshot('busqueda-nombre-taxid');
  await page.getByRole('link', { name: companyName }).click();
  await expect(page.getByRole('heading', { name: companyName })).toBeVisible();
  await page.getByRole('link', { name: 'Nueva simulación' }).first().click();
  await page.getByRole('spinbutton', { name: 'Almacenamiento contratado (GB)' }).fill('250');
  await page.getByRole('spinbutton', { name: 'Llamadas al servicio / mes' }).fill('100000');
  await expect(page.locator('.total')).toHaveText('169,40 €');
  const emptyHistory = await request.get(`${api}/customers/${customerId}/simulations`);
  expect(emptyHistory.status()).toBe(200);
  expect((await emptyHistory.json()).total).toBe(0);
  await screenshot('preview-15-eur-no-persistencia');

  const scenarios = [
    { currency: 'EUR', users: 15, display: '169,40 €', converted: '169.40', rate: '1', date: null },
    {
      currency: 'USD',
      users: 16,
      display: '196,95 US$',
      converted: '196.95',
      rate: '1.0998',
      date: '2026-11-18',
    },
    {
      currency: 'GBP',
      users: 15,
      display: '141,19 £',
      converted: '141.19',
      rate: '0.83348',
      date: '2026-11-18',
    },
  ] as const;
  const savedIds: string[] = [];
  for (let index = 0; index < scenarios.length; index++) {
    const scenario = scenarios[index]!;
    if (index > 0) {
      await page.getByRole('link', { name: 'Nueva simulación' }).first().click();
      await page.getByRole('spinbutton', { name: 'Almacenamiento contratado (GB)' }).fill('250');
      await page.getByRole('spinbutton', { name: 'Llamadas al servicio / mes' }).fill('100000');
      await page.getByRole('spinbutton', { name: 'Usuarios activos' }).fill(String(scenario.users));
    }
    await selectCurrency(scenario.currency);
    await expect(page.locator('.total')).toHaveText(scenario.display);
    const beforeSave = await request.get(`${api}/customers/${customerId}/simulations`);
    expect(beforeSave.status()).toBe(200);
    expect((await beforeSave.json()).total).toBe(index);

    const responsePromise = page.waitForResponse(
      (response) =>
        new URL(response.url()).pathname === '/api/simulations' &&
        response.request().method() === 'POST',
    );
    await page.getByRole('button', { name: 'Guardar simulación' }).click();
    const response = await responsePromise;
    expect(response.status()).toBe(201);
    const saved = await response.json();
    const subtotal = scenario.users === 16 ? '148.00' : '140.00';
    const tax = scenario.users === 16 ? '31.08' : '29.40';
    const total = scenario.users === 16 ? '179.08' : '169.40';
    expect(saved).toMatchObject({
      customer_id: customerId,
      user_count: scenario.users,
      storage_gb: 250,
      api_calls_per_month: 100000,
      user_subtotal_eur: subtotal,
      tax_amount_eur: tax,
      total_eur: total,
      display_currency: scenario.currency,
      converted_total: scenario.converted,
      exchange_rate: scenario.rate,
      exchange_rate_date: scenario.date,
      exchange_rate_source: scenario.currency === 'EUR' ? 'identity' : 'frankfurter',
    });
    savedIds.push(saved.id as string);
    await expect(page.getByText(/Simulación guardada/)).toBeVisible();
    await screenshot(`simulacion-guardada-${scenario.currency.toLowerCase()}`);
    await page.getByRole('link', { name: 'Ver ficha e historial' }).click();
    const persisted = await request.get(`${api}/customers/${customerId}/simulations`);
    expect((await persisted.json()).total).toBe(index + 1);
    await expect(page.getByText(scenario.display).last()).toBeVisible();
    if (index < scenarios.length - 1) await screenshot(`historial-${index + 1}`);
  }

  await page.reload();
  await expect(page.getByText('3 simulaciones')).toBeVisible();
  for (const display of ['169,40 €', '196,95 US$', '141,19 £']) {
    await expect(page.getByText(display).last()).toBeVisible();
  }
  await screenshot('historial-eur-usd-gbp-tras-reload');
  expect(savedIds).toHaveLength(3);
  const unsupportedMutation = await request.patch(`${api}/simulations/${savedIds[0]}`, {
    data: { user_count: 999 },
  });
  expect([404, 405]).toContain(unsupportedMutation.status());
  const afterMutation = await request.get(`${api}/customers/${customerId}/simulations`);
  expect((await afterMutation.json()).total).toBe(3);

  await page.getByRole('link', { name: 'Nueva simulación' }).first().click();
  const users = page.getByRole('spinbutton', { name: 'Usuarios activos' });
  await users.fill('0');
  await expect(page.locator('.total')).toHaveText('0,00 €');
  const unchangedHistory = await request.get(`${api}/customers/${customerId}/simulations`);
  expect((await unchangedHistory.json()).total).toBe(3);
  await users.fill('1000000');
  await page.getByRole('spinbutton', { name: 'Almacenamiento contratado (GB)' }).fill('1000000');
  await page.getByRole('spinbutton', { name: 'Llamadas al servicio / mes' }).fill('1000000000');
  await expect(page.locator('.total')).toHaveText('6.050.205,70 €');
  await screenshot('limites-maximos-no-guardado');

  await page.goto('/customers/new');
  await page.getByLabel('Razón social').fill('TASK045B cliente PT sintético');
  await page.getByRole('combobox', { name: 'País' }).click();
  await page.getByRole('option', { name: 'Portugal' }).click();
  await page.getByLabel('Identificador fiscal').fill('PT-AUDIT-045B');
  await page.getByLabel('Email de contacto').fill('audit@example.com');
  await page.getByRole('button', { name: 'Guardar cliente' }).click();
  await expect(page.getByRole('heading', { name: 'TASK045B cliente PT sintético' })).toBeVisible();
  await screenshot('alta-internacional-pt');
  const missing = await request.get(`${api}/customers/00000000-0000-4000-8000-000000000099`);
  expect(missing.status()).toBe(404);
  await page.goto('/customers/00000000-0000-4000-8000-000000000099');
  await expect(page.getByRole('heading', { name: 'Cliente no encontrado' })).toBeVisible();
});

test('recovers the history after the isolated backend restarts', async ({ page }, info) => {
  test.skip(
    process.env['TASK045B_AFTER_RESTART'] !== '1',
    'Runs only after restarting the TASK045B backend on the same temporary SQLite file.',
  );
  test.skip(
    info.project.name !== 'chromium',
    'The post-restart integration check runs once in Chromium.',
  );
  const customerId = process.env['TASK045B_RESTART_CUSTOMER_ID'];
  if (!customerId)
    throw new Error('TASK045B_RESTART_CUSTOMER_ID is required for the post-restart check.');
  const evidence = process.env['TASK045B_REAL_SCREENSHOT_DIR'];

  await page.goto(`/customers/${customerId}`);
  await expect(page.getByRole('heading', { name: 'Historial' })).toBeVisible();
  await expect(page.getByText('3 simulaciones')).toBeVisible();
  for (const amount of ['169,40 €', '196,95 US$', '141,19 £']) {
    await expect(page.getByText(amount).last()).toBeVisible();
  }
  if (evidence) {
    mkdirSync(resolve(evidence), { recursive: true });
    await page.screenshot({ path: resolve(evidence, 'real-historial-tras-reinicio-backend.png') });
  }
  await page.reload();
  await expect(page.getByText('3 simulaciones')).toBeVisible();
  await expect(page.getByText('196,95 US$').last()).toBeVisible();
});
