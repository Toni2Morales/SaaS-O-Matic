import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { expect, test } from '@playwright/test';

const id = '00000000-0000-4000-8000-000000000001';
const evidenceDir = process.env['TASK043_SCREENSHOT_DIR'];
const customer = {
  id,
  legal_name: 'Empresa sintética de demostración',
  tax_id: 'B12345674',
  email: 'qa@example.test',
  country: 'ES',
  plan: 'standard',
  created_at: '2026-11-18T12:00:00Z',
};

function result(currency = 'EUR', users = 15) {
  const reference = {
    0: { subtotal: '0.00', tax: '0.00', total: '0.00' },
    15: { subtotal: '140.00', tax: '29.40', total: '169.40' },
    16: { subtotal: '148.00', tax: '31.08', total: '179.08' },
    1500: { subtotal: '7670.00', tax: '1610.70', total: '9280.70' },
  } as const;
  const amounts = reference[users as keyof typeof reference];
  if (!amounts) throw new Error(`Missing reference fixture for ${users} users.`);
  const converted: Record<string, Record<number, string>> = {
    USD: { 0: '0.00', 15: '186.31', 16: '196.95' },
    GBP: { 0: '0.00', 15: '141.19', 16: '149.26' },
  };
  const convertedTotal = currency === 'EUR' ? amounts.total : converted[currency]?.[users];
  if (convertedTotal === undefined) {
    throw new Error(`Missing ${currency} conversion fixture for ${users} users.`);
  }
  return {
    customer_id: id,
    user_count: users,
    user_subtotal_eur: amounts.subtotal,
    storage_gb: 0,
    api_calls_per_month: 0,
    billing_period: 'monthly',
    tax_country: 'ES',
    tax_rate: '0.21',
    tax_source: 'Agencia Tributaria',
    tax_catalog_version: 'v1',
    tax_verified_on: '2026-11-17',
    tax_territory: 'Península y Baleares',
    tax_effective_from: null,
    tax_amount_eur: amounts.tax,
    total_eur: amounts.total,
    display_currency: currency,
    exchange_rate: currency === 'EUR' ? '1' : currency === 'USD' ? '1.0998' : '0.83348',
    exchange_rate_date: currency === 'EUR' ? null : '2026-11-18',
    exchange_rate_obtained_at: '2026-11-18T12:00:00Z',
    exchange_rate_source: currency === 'EUR' ? 'identity' : 'Frankfurter (fixture)',
    converted_total: convertedTotal,
  };
}

test('captures real browser evidence with clearly intercepted deterministic API responses', async ({
  page,
}) => {
  test.skip(!evidenceDir, 'Set TASK043_SCREENSHOT_DIR to an external temporary folder.');
  mkdirSync(resolve(evidenceDir!), { recursive: true });
  let fxError = false;
  let delayed = false;
  let releasePreview: (() => void) | undefined;
  await page.route('**/api/customers**', (route) => {
    if (
      route.request().method() === 'GET' &&
      new URL(route.request().url()).pathname.endsWith(`/customers/${id}`)
    ) {
      return route.fulfill({ json: customer });
    }
    return route.fulfill({ json: { items: [customer], total: 1, limit: 6, offset: 0 } });
  });
  await page.route('**/api/customers/*/simulations**', (route) =>
    route.fulfill({
      json: {
        items: [{ ...result('USD', 16), id: 'sim-1', created_at: '2026-11-18T12:00:00Z' }],
        total: 1,
        limit: 10,
        offset: 0,
      },
    }),
  );
  await page.route('**/api/simulations/preview', async (route) => {
    if (delayed) await new Promise<void>((resolveRequest) => (releasePreview = resolveRequest));
    if (fxError)
      return route.fulfill({
        status: 503,
        contentType: 'application/problem+json',
        json: { type: 'about:blank', title: 'Unavailable', status: 503, detail: 'FX unavailable' },
      });
    const body = route.request().postDataJSON() as { display_currency: string; user_count: number };
    return route.fulfill({ json: result(body.display_currency, body.user_count) });
  });
  await page.route('**/api/simulations', (route) => {
    const body = route.request().postDataJSON() as { display_currency: string; user_count: number };
    return route.fulfill({
      status: 201,
      json: {
        ...result(body.display_currency, body.user_count),
        id: '00000000-0000-4000-8000-000000000009',
        created_at: '2026-11-18T12:01:00Z',
      },
    });
  });
  const shot = async (name: string) => {
    await page.keyboard.press('Escape');
    await expect(page.getByRole('listbox')).toHaveCount(0);
    await page.evaluate(() => window.scrollTo(0, 0));
    await expect(page.locator('#page-title')).toBeInViewport();
    await expect(
      page.getByRole('link', { name: 'Saltar al contenido principal' }),
    ).not.toBeFocused();
    await page.screenshot({ path: resolve(evidenceDir!, name), fullPage: false });
  };

  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto(`/customers/${id}/simulations/new`);
  await expect(page.locator('.total')).toHaveText('169,40 €');
  await shot('TASK043-simulador-desktop.png');

  for (const viewport of [
    { width: 320, height: 568 },
    { width: 390, height: 844 },
    { width: 768, height: 1024 },
    { width: 1024, height: 768 },
    { width: 1280, height: 800 },
    { width: 1440, height: 900 },
    { width: 1920, height: 1080 },
  ]) {
    await page.setViewportSize(viewport);
    expect(
      await page.locator('body').evaluate((element) => element.scrollWidth <= window.innerWidth),
      `horizontal overflow at ${viewport.width}×${viewport.height}`,
    ).toBe(true);
  }

  await page.setViewportSize({ width: 390, height: 844 });
  await shot('TASK043-simulador-mobile.png');
  await page.setViewportSize({ width: 1440, height: 1000 });

  const currency = page.getByRole('combobox', { name: 'Divisa de visualización' });
  await currency.click();
  await page.getByRole('option', { name: 'USD — Dólar estadounidense' }).click();
  await expect(page.locator('.total')).toHaveText('186,31 US$');
  await shot('TASK043-simulador-usd.png');
  await currency.click();
  await page.getByRole('option', { name: 'GBP — Libra esterlina' }).click();
  await expect(page.locator('.total')).toHaveText('141,19 £');
  await shot('TASK043-simulador-gbp.png');
  await currency.click();
  await page.getByRole('option', { name: 'EUR — Euro' }).click();
  await expect(page.locator('.total')).toHaveText('169,40 €');

  await page.locator('#user-count').fill('0');
  await expect(page.locator('.total')).toHaveText('0,00 €');
  await shot('TASK043-simulador-cero-usuarios.png');
  await page.locator('#user-count').fill('1500');
  await expect(page.getByText(/deslizador se desactiva/i)).toBeVisible();
  await shot('TASK043-simulador-usuario-manual.png');
  await page.locator('#user-count').fill('1000001');
  await page.locator('#user-count').blur();
  await expect(page.getByText(/valor máximo/i)).toBeVisible();
  await shot('TASK043-simulador-validacion.png');

  await page.locator('#user-count').fill('15');
  delayed = true;
  await page.locator('#user-count').fill('16');
  await expect(page.getByText('Calculando estimación…')).toBeVisible();
  await shot('TASK043-simulador-calculando.png');
  delayed = false;
  releasePreview?.();
  await expect(page.locator('.total')).toHaveText('179,08 €');

  fxError = true;
  await currency.click();
  await page.getByRole('option', { name: 'USD — Dólar estadounidense' }).click();
  await expect(page.getByText(/No se pudo obtener un tipo de cambio/)).toBeVisible();
  await shot('TASK043-simulador-error-fx.png');
  fxError = false;
  await page.getByRole('button', { name: 'Reintentar estimación' }).click();
  await expect(page.locator('.total')).toHaveText('196,95 US$');
  await page.getByRole('button', { name: 'Guardar simulación' }).click();
  await expect(page.getByText(/Simulación guardada/)).toBeVisible();
  await shot('TASK043-simulacion-guardada.png');
  await page.getByRole('link', { name: 'Ver ficha e historial' }).click();
  await expect(page.getByRole('heading', { name: 'Historial de simulaciones' })).toBeVisible();
  await shot('TASK043-historial-actualizado.png');

  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Panel comercial' })).toBeVisible();
  await shot('TASK043-dashboard-tema-unificado.png');
});
