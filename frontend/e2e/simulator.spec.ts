import { expect, test } from '@playwright/test';

const customerId = '00000000-0000-4000-8000-000000000001';
const company = {
  id: customerId,
  legal_name: 'Empresa de prueba',
  tax_id: 'B12345674',
  email: 'contacto@example.test',
  country: 'ES',
  plan: 'standard',
  created_at: '2026-11-18T12:00:00Z',
};

function estimate(currency = 'EUR', users = 15) {
  const subtotal = users === 15 ? '140.00' : users === 16 ? '148.00' : '100.00';
  const tax = users === 16 ? '31.08' : users === 15 ? '29.40' : '21.00';
  const total = users === 16 ? '179.08' : users === 15 ? '169.40' : '121.00';
  return {
    customer_id: customerId,
    user_count: users,
    user_subtotal_eur: subtotal,
    storage_gb: 250,
    api_calls_per_month: 100000,
    billing_period: 'monthly',
    tax_country: 'ES',
    tax_rate: '0.21',
    tax_source: 'Agencia Tributaria',
    tax_catalog_version: 'v1',
    tax_verified_on: '2026-11-17',
    tax_territory: 'Península e Islas Baleares',
    tax_effective_from: null,
    tax_amount_eur: tax,
    total_eur: total,
    display_currency: currency,
    exchange_rate: currency === 'EUR' ? '1' : '0.92',
    exchange_rate_date: currency === 'EUR' ? null : '2026-11-17',
    exchange_rate_obtained_at: '2026-11-18T12:00:00Z',
    exchange_rate_source: currency === 'EUR' ? 'identity' : 'Frankfurter',
    converted_total: currency === 'EUR' ? total : '186.31',
  };
}

test('loads client, previews exact backend data, and explicitly saves', async ({ page }) => {
  const postBodies: unknown[] = [];
  await page.route(`**/api/customers/${customerId}`, (route) => route.fulfill({ json: company }));
  await page.route('**/api/simulations/preview', async (route) => {
    postBodies.push(route.request().postDataJSON());
    await route.fulfill({ json: estimate() });
  });
  await page.route('**/api/simulations', async (route) => {
    postBodies.push(route.request().postDataJSON());
    await route.fulfill({
      status: 201,
      json: {
        ...estimate(),
        id: '00000000-0000-4000-8000-000000000009',
        created_at: '2026-11-18T12:01:00Z',
      },
    });
  });

  await page.goto(`/customers/${customerId}/simulations/new`);
  await expect(page.getByText('Empresa de prueba')).toBeVisible();
  await expect(page.getByText(/Primeros 10: 10 usuarios × 10 € \/ usuario/)).toBeVisible();
  await expect(page.getByText(/11–50: 5 usuarios × 8 € \/ usuario/)).toBeVisible();
  await expect(page.locator('.total')).toHaveText('169,40 €', { timeout: 5000 });
  expect(postBodies[0]).toEqual({
    customer_id: customerId,
    user_count: 15,
    storage_gb: 0,
    api_calls_per_month: 0,
    display_currency: 'EUR',
  });
  await page.getByRole('button', { name: 'Guardar simulación' }).click();
  await expect(page.getByText(/Simulación guardada/)).toBeVisible();
  expect(postBodies).toHaveLength(2);
  await expect(page.getByRole('link', { name: 'Ver ficha e historial' })).toBeVisible();
});

test('does not clamp a manual user value above the slider range and responds to FX 503', async ({
  page,
}) => {
  await page.route(`**/api/customers/${customerId}`, (route) => route.fulfill({ json: company }));
  let failFx = true;
  await page.route('**/api/simulations/preview', async (route) => {
    if (failFx) {
      await route.fulfill({
        status: 503,
        contentType: 'application/problem+json',
        json: { type: 'about:blank', title: 'Unavailable', status: 503, detail: 'FX unavailable' },
      });
      return;
    }
    await route.fulfill({ json: estimate('EUR') });
  });
  await page.goto(`/customers/${customerId}/simulations/new`);
  const users = page.getByRole('spinbutton', { name: 'Usuarios activos' });
  await users.fill('1500');
  await expect(users).toHaveValue('1500');
  await expect(page.getByText(/deslizador se desactiva/i)).toBeVisible();
  await expect(page.getByRole('button', { name: 'Guardar simulación' })).toBeDisabled();
  await users.fill('1000000');
  await expect(users).toHaveValue('1000000');
  await users.fill('1000001');
  await users.blur();
  await expect(page.getByText(/valor máximo es 1\.000\.000/i)).toBeVisible();
  await users.fill('15');
  await expect(page.getByRole('button', { name: 'Reintentar estimación' })).toBeVisible({
    timeout: 5000,
  });
  failFx = false;
  await page.getByRole('button', { name: 'Reintentar estimación' }).click();
  await expect(page.getByText('Estimación actualizada.')).toBeVisible({ timeout: 5000 });
});

test('cancels an obsolete preview and never lets a late response replace current inputs', async ({
  page,
}) => {
  let releaseOld: (() => void) | undefined;
  await page.route(`**/api/customers/${customerId}`, (route) => route.fulfill({ json: company }));
  await page.route('**/api/simulations/preview', async (route) => {
    const payload = route.request().postDataJSON() as { user_count: number };
    if (payload.user_count === 15) await new Promise<void>((resolve) => (releaseOld = resolve));
    await route.fulfill({ json: estimate('EUR', payload.user_count) }).catch(() => undefined);
  });
  await page.goto(`/customers/${customerId}/simulations/new`);
  await expect.poll(() => releaseOld !== undefined).toBe(true);
  await page.locator('#user-count').fill('16');
  await expect(page.locator('.total')).toHaveText('179,08 €', { timeout: 5000 });
  releaseOld?.();
  await expect(page.locator('.total')).toHaveText('179,08 €');
});

test('an invalid form immediately cancels an in-flight preview', async ({ page }) => {
  let releasePreview: (() => void) | undefined;
  await page.route(`**/api/customers/${customerId}`, (route) => route.fulfill({ json: company }));
  await page.route('**/api/simulations/preview', async (route) => {
    await new Promise<void>((resolve) => (releasePreview = resolve));
    await route.fulfill({ json: estimate() }).catch(() => undefined);
  });
  await page.goto(`/customers/${customerId}/simulations/new`);
  await expect.poll(() => releasePreview !== undefined).toBe(true);
  const users = page.locator('#user-count');
  await users.fill('1000001');
  await users.blur();
  await expect(page.getByText('Completa los campos correctamente para calcular.')).toBeVisible();
  await expect(page.locator('.tiers')).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Guardar simulación' })).toBeDisabled();
  releasePreview?.();
  await expect(page.locator('.total')).toHaveCount(0);
});

test('shows field-specific numeric errors and sends no preview for invalid inputs', async ({
  page,
}) => {
  let previewCount = 0;
  await page.route(`**/api/customers/${customerId}`, (route) => route.fulfill({ json: company }));
  await page.route('**/api/simulations/preview', async (route) => {
    previewCount++;
    await route.fulfill({ json: estimate() });
  });
  await page.goto(`/customers/${customerId}/simulations/new`);
  await expect(page.locator('.total')).toHaveText('169,40 €');

  const users = page.locator('#user-count');
  await users.fill('-1');
  await users.blur();
  await expect(page.getByText('El valor mínimo es 0.')).toBeVisible();
  await users.fill('15.5');
  await users.blur();
  await expect(page.getByText('Introduce un número entero.')).toBeVisible();
  await users.fill('');
  await users.blur();
  await expect(page.getByText('Este campo es obligatorio.')).toBeVisible();

  const storage = page.getByRole('spinbutton', { name: 'Almacenamiento contratado (GB)' });
  await storage.fill('-1');
  await storage.blur();
  await expect(page.getByText('El valor mínimo es 0.')).toBeVisible();
  const calls = page.getByRole('spinbutton', { name: 'Llamadas al servicio / mes' });
  await calls.fill('1000000001');
  await calls.blur();
  await expect(page.getByText('El valor máximo es 1.000.000.000.')).toBeVisible();
  await expect(page.locator('.tiers')).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Guardar simulación' })).toBeDisabled();
  expect(previewCount).toBe(1);
});

test('locks the form while save is in flight and issues only one create request', async ({
  page,
}) => {
  await page.route(`**/api/customers/${customerId}`, (route) => route.fulfill({ json: company }));
  await page.route('**/api/simulations/preview', (route) => {
    const body = route.request().postDataJSON() as { user_count: number };
    return route.fulfill({ json: estimate('EUR', body.user_count) });
  });
  let finishSave: (() => void) | undefined;
  let creates = 0;
  await page.route('**/api/simulations', async (route) => {
    creates++;
    await new Promise<void>((resolve) => (finishSave = resolve));
    await route.fulfill({
      status: 201,
      json: { ...estimate(), id: 'saved-once', created_at: '2026-11-18T12:01:00Z' },
    });
  });
  await page.goto(`/customers/${customerId}/simulations/new`);
  const save = page.getByRole('button', { name: 'Guardar simulación' });
  await expect(save).toBeEnabled({ timeout: 5000 });
  await save.click();
  await expect(page.getByRole('button', { name: 'Guardando…' })).toBeDisabled();
  await expect(page.locator('#user-count')).toBeDisabled();
  expect(creates).toBe(1);
  finishSave?.();
  await expect(page.getByText(/Simulación guardada/)).toBeVisible();
  expect(creates).toBe(1);
});

test('shows the saved result when it differs from the preview', async ({ page }) => {
  await page.route(`**/api/customers/${customerId}`, (route) => route.fulfill({ json: company }));
  await page.route('**/api/simulations/preview', (route) => {
    const body = route.request().postDataJSON() as { display_currency: string };
    const currency = body.display_currency;
    return route.fulfill({
      json: {
        ...estimate(currency),
        exchange_rate: currency === 'EUR' ? '1' : '1.0998',
        converted_total: currency === 'EUR' ? '169.40' : '186.31',
      },
    });
  });
  let creates = 0;
  await page.route('**/api/simulations', async (route) => {
    creates++;
    await route.fulfill({
      status: 201,
      json: {
        ...estimate('USD'),
        converted_total: '186.32',
        exchange_rate: '1.09986',
        id: 'saved-with-new-fx-rate',
        created_at: '2026-11-19T12:01:00Z',
      },
    });
  });
  await page.goto(`/customers/${customerId}/simulations/new`);
  await page.getByRole('combobox', { name: 'Divisa de visualización' }).click();
  await page.getByRole('option', { name: 'USD — Dólar estadounidense' }).click();
  await expect(page.locator('.total')).toHaveText('186,31 US$');
  await page.getByRole('button', { name: 'Guardar simulación' }).click();
  await expect(page.getByText(/importe definitivo se ha actualizado/i)).toBeVisible();
  await expect(page.locator('.total')).toHaveText('186,32 US$');
  await expect(page.getByText(/Resultado definitivo: 186,32 US\$/)).toBeVisible();
  expect(creates).toBe(1);
});

test('does not retry an ambiguous create failure and preserves inputs for history review', async ({
  page,
}) => {
  await page.route(`**/api/customers/${customerId}`, (route) => route.fulfill({ json: company }));
  await page.route('**/api/simulations/preview', (route) => route.fulfill({ json: estimate() }));
  let creates = 0;
  await page.route('**/api/simulations', async (route) => {
    creates++;
    await route.abort('failed');
  });
  await page.goto(`/customers/${customerId}/simulations/new`);
  await expect(page.getByRole('button', { name: 'Guardar simulación' })).toBeEnabled();
  await page.locator('#user-count').fill('15');
  await expect(page.locator('.total')).toHaveText('169,40 €');
  await page.getByRole('button', { name: 'Guardar simulación' }).click();
  await expect(page.getByText(/La simulación podría haberse guardado/)).toBeVisible();
  await expect(page.getByRole('link', { name: 'Consultar historial' })).toBeVisible();
  await expect(page.locator('#user-count')).toHaveValue('15');
  await expect(page.getByRole('button', { name: 'Guardar simulación' })).toBeEnabled();
  expect(creates).toBe(1);
});

test('adapts the simulator to a 320px viewport without horizontal overflow', async ({ page }) => {
  await page.route(`**/api/customers/${customerId}`, (route) => route.fulfill({ json: company }));
  await page.route('**/api/simulations/preview', (route) => {
    const body = route.request().postDataJSON() as { user_count: number };
    return route.fulfill({ json: estimate('EUR', body.user_count) });
  });
  await page.setViewportSize({ width: 320, height: 760 });
  await page.goto(`/customers/${customerId}/simulations/new`);
  await expect(page.getByRole('heading', { name: 'Simulador de suscripción' })).toBeVisible();
  await expect(page.locator('h1')).toHaveCount(1);
  const mobileEstimate = page.locator('.mobile-estimate');
  await expect(mobileEstimate).toBeVisible();
  await expect(mobileEstimate).toContainText('169,40 €');
  expect(
    await page.locator('body').evaluate((element) => element.scrollWidth <= window.innerWidth),
  ).toBe(true);
  const slider = page.getByRole('slider');
  await slider.focus();
  await slider.press('ArrowRight');
  await expect(page.locator('#user-count')).toHaveValue('16');
  await expect.poll(() => page.locator('.total').textContent()).toBe('179,08 €');
  await expect.poll(() => mobileEstimate.textContent()).toContain('179,08 €');
  await page.evaluate(() => window.scrollTo(0, 900));
  await expect(mobileEstimate).toHaveCSS('position', 'static');
  await page.locator('#user-count').fill('1000001');
  await page.locator('#user-count').blur();
  await expect(mobileEstimate).toContainText('Estimación no disponible');
  await expect(mobileEstimate).not.toContainText('179,08 €');
});
