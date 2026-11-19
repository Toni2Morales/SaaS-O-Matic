import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { expect, test, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const customerId = '00000000-0000-4000-8000-000000000045';
const customer = {
  id: customerId,
  legal_name: 'Empresa sintética TASK045B',
  tax_id: 'B12345674',
  email: 'audit@example.com',
  country: 'ES',
  plan: 'standard',
  created_at: '2026-11-19T10:00:00Z',
};

function estimate(currency = 'EUR', users = 15) {
  const amounts =
    users === 16
      ? { subtotal: '148.00', tax: '31.08', total: '179.08' }
      : users === 0
        ? { subtotal: '0.00', tax: '0.00', total: '0.00' }
        : { subtotal: '140.00', tax: '29.40', total: '169.40' };
  const converted =
    currency === 'EUR'
      ? amounts.total
      : currency === 'USD'
        ? users === 16
          ? '196.95'
          : '186.31'
        : users === 16
          ? '149.26'
          : '141.19';
  return {
    customer_id: customerId,
    user_count: users,
    user_subtotal_eur: amounts.subtotal,
    storage_gb: 250,
    api_calls_per_month: 100000,
    billing_period: 'monthly',
    tax_country: 'ES',
    tax_rate: '0.21',
    tax_source: 'Agencia Tributaria (fixture)',
    tax_catalog_version: 'TASK045B-fixture',
    tax_verified_on: '2026-11-17',
    tax_territory: 'Península y Baleares',
    tax_effective_from: null,
    tax_amount_eur: amounts.tax,
    total_eur: amounts.total,
    display_currency: currency,
    exchange_rate: currency === 'EUR' ? '1' : currency === 'USD' ? '1.0998' : '0.83348',
    exchange_rate_date: currency === 'EUR' ? null : '2026-11-18',
    exchange_rate_obtained_at: '2026-11-19T10:00:00Z',
    exchange_rate_source: currency === 'EUR' ? 'identity' : 'Frankfurter (fixture)',
    converted_total: converted,
  };
}

async function installFixtures(page: Page) {
  let history: Array<Record<string, unknown>> = [];
  let fxUnavailable = false;
  await page.route('**/api/customers**', async (route) => {
    const url = new URL(route.request().url());
    if (url.pathname === `/api/customers/${customerId}`) {
      await route.fulfill({ json: customer });
      return;
    }
    await route.fulfill({ json: { items: [customer], total: 1, limit: 20, offset: 0 } });
  });
  await page.route('**/api/customers/*/simulations**', (route) => {
    const url = new URL(route.request().url());
    const limit = Number(url.searchParams.get('limit') ?? 10);
    const offset = Number(url.searchParams.get('offset') ?? 0);
    return route.fulfill({
      json: { items: history.slice(offset, offset + limit), total: history.length, limit, offset },
    });
  });
  await page.route('**/api/simulations/preview', (route) => {
    if (fxUnavailable && route.request().postDataJSON().display_currency !== 'EUR') {
      return route.fulfill({
        status: 503,
        contentType: 'application/problem+json',
        json: {
          type: 'about:blank',
          title: 'Unavailable',
          status: 503,
          detail: 'fixture FX failure',
        },
      });
    }
    const body = route.request().postDataJSON() as { display_currency: string; user_count: number };
    return route.fulfill({ json: estimate(body.display_currency, body.user_count) });
  });
  await page.route('**/api/simulations', (route) => {
    const body = route.request().postDataJSON() as { display_currency: string; user_count: number };
    const result = estimate(body.display_currency, body.user_count);
    const created = {
      ...result,
      id: `00000000-0000-4000-8000-${String(history.length + 1).padStart(12, '0')}`,
      created_at: '2026-11-19T10:01:00Z',
    };
    history = [created, ...history];
    return route.fulfill({
      status: 201,
      json: created,
    });
  });
  return { setFxUnavailable: (value: boolean) => (fxUnavailable = value) };
}

async function textContrast(locator: import('@playwright/test').Locator) {
  return locator.evaluate((element) => {
    const channels = (value: string): number[] =>
      (value.match(/[\d.]+/g) ?? []).slice(0, 4).map(Number);
    const luminance = (color: string): number => {
      const [red, green, blue] = channels(color).map((channel) => {
        const normalized = channel / 255;
        return normalized <= 0.04045 ? normalized / 12.92 : ((normalized + 0.055) / 1.055) ** 2.4;
      });
      if (red === undefined || green === undefined || blue === undefined) {
        throw new Error(`No se pudo parsear el color ${color}.`);
      }
      return 0.2126 * red + 0.7152 * green + 0.0722 * blue;
    };

    const foreground = getComputedStyle(element).color;
    let ancestor: Element | null = element;
    let background = 'rgba(0, 0, 0, 0)';
    while (ancestor) {
      const candidate = getComputedStyle(ancestor).backgroundColor;
      const parsed = channels(candidate);
      if (parsed.length < 4 || (parsed[3] ?? 1) > 0) {
        background = candidate;
        break;
      }
      ancestor = ancestor.parentElement;
    }
    const first = luminance(foreground);
    const second = luminance(background);
    return {
      foreground,
      background,
      ratio: (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05),
      fontSize: getComputedStyle(element).fontSize,
    };
  });
}

async function waitForTransitions(page: Page): Promise<void> {
  await page.evaluate(async () => {
    const running = document
      .getAnimations()
      .filter((animation) => animation.playState === 'running');
    await Promise.all(running.map((animation) => animation.finished.catch(() => undefined)));
  });
}

test('keeps secondary text above 4.5:1 on rendered canvas and card surfaces', async ({ page }) => {
  await installFixtures(page);
  const samples: Array<{ route: string; selector: string }> = [
    { route: '/', selector: 'app-section-heading p' },
    { route: '/customers', selector: '.search-help' },
    { route: '/customers/new', selector: '.privacy-note' },
    { route: `/customers/${customerId}/simulations/new`, selector: '.help' },
  ];
  const measured: Array<{
    route: string;
    selector: string;
    contrast: Awaited<ReturnType<typeof textContrast>>;
  }> = [];
  for (const sample of samples) {
    await page.goto(sample.route);
    const element = page.locator(sample.selector).first();
    await expect(element).toBeVisible();
    const contrast = await textContrast(element);
    measured.push({ ...sample, contrast });
    expect(
      contrast.ratio,
      `${sample.route} ${sample.selector}: ${JSON.stringify(contrast)}`,
    ).toBeGreaterThanOrEqual(4.5);
  }
  console.log('TASK045B contrast checks', JSON.stringify(measured));
});

test('announces a terminal FX error without a pending status and recovers by retry', async ({
  page,
}) => {
  await page.route(`**/api/customers/${customerId}`, (route) => route.fulfill({ json: customer }));
  let failFx = false;
  await page.route('**/api/simulations/preview', (route) => {
    if (failFx) {
      return route.fulfill({
        status: 503,
        contentType: 'application/problem+json',
        json: {
          type: 'about:blank',
          title: 'Unavailable',
          status: 503,
          detail: 'fixture FX failure',
        },
      });
    }
    const body = route.request().postDataJSON() as { display_currency: string; user_count: number };
    return route.fulfill({ json: estimate(body.display_currency, body.user_count) });
  });
  await page.goto(`/customers/${customerId}/simulations/new`);
  await expect(page.locator('.total')).toHaveText('169,40 €');
  failFx = true;
  await page.getByRole('combobox', { name: 'Divisa de visualización' }).click();
  await page.getByRole('option', { name: 'USD — Dólar estadounidense' }).click();
  await expect(
    page.getByRole('alert').getByText(/No se pudo obtener un tipo de cambio/),
  ).toBeVisible();
  await expect(page.locator('.status')).not.toContainText(/preparando|calculando/i);
  await expect(page.getByText(/Estimación anterior: los parámetros han cambiado/)).toBeVisible();
  await expect(page.getByRole('button', { name: 'Guardar simulación' })).toBeDisabled();
  failFx = false;
  await page.getByRole('button', { name: 'Reintentar estimación' }).click();
  await expect(page.locator('.total')).toHaveText('186,31 US$');
  await expect(page.getByText('Estimación actualizada.')).toBeVisible();
});

test('associates 1,000,001 users with an accessible max error and sends no preview', async ({
  page,
}) => {
  await installFixtures(page);
  let previews = 0;
  await page.unroute('**/api/simulations/preview');
  await page.route('**/api/simulations/preview', (route) => {
    previews++;
    return route.fulfill({ json: estimate(route.request().postDataJSON().display_currency) });
  });
  await page.goto(`/customers/${customerId}/simulations/new`);
  await expect(page.locator('.total')).toHaveText('169,40 €');
  const users = page.locator('#user-count');
  const beforeInvalid = previews;
  await users.fill('1000001');
  await users.blur();
  const error = page.locator('#users-error');
  await expect(error).toBeVisible();
  await expect(error).toHaveText('El valor máximo es 1.000.000.');
  await expect(users).toHaveAttribute('aria-describedby', /users-error/);
  await expect(users).toHaveAttribute('aria-invalid', 'true');
  await expect(page.locator('.tiers')).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Guardar simulación' })).toBeDisabled();
  await expect(page.locator('.total')).toHaveText('169,40 €');
  await expect(page.getByText(/Estimación anterior: los parámetros han cambiado/)).toBeVisible();
  expect(previews).toBe(beforeInvalid);
});

test('keeps dashboard, customers, create, detail and simulator within responsive viewports', async ({
  page,
}) => {
  await installFixtures(page);
  const paths = [
    '/',
    '/customers',
    '/customers/new',
    `/customers/${customerId}`,
    `/customers/${customerId}/simulations/new`,
  ];
  for (const width of [320, 375, 390, 768, 1024, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    for (const route of paths) {
      await page.goto(route);
      const readySelector =
        route === '/'
          ? '.dashboard-page'
          : route === '/customers'
            ? '.customers-page'
            : route === '/customers/new'
              ? '.create-page'
              : route.endsWith('/simulations/new')
                ? '.simulator'
                : '.detail-page';
      await expect(page.locator(readySelector)).toBeVisible();
      await page.evaluate(
        () =>
          new Promise<void>((resolveFrame) =>
            requestAnimationFrame(() => requestAnimationFrame(() => resolveFrame())),
          ),
      );
      const dimensions = await page.evaluate(() => ({
        viewport: window.innerWidth,
        document: document.documentElement.scrollWidth,
        body: document.body.scrollWidth,
      }));
      if (dimensions.document > width || dimensions.body > width) {
        console.log(
          `Responsive overflow ${route} at ${width}px`,
          await page.evaluate(() =>
            [...document.querySelectorAll<HTMLElement>('body *')]
              .map((element) => ({
                tag: element.tagName,
                className: element.className,
                rect: element.getBoundingClientRect().toJSON(),
                scrollWidth: element.scrollWidth,
                clientWidth: element.clientWidth,
                display: getComputedStyle(element).display,
                gridTemplateColumns: getComputedStyle(element).gridTemplateColumns,
              }))
              .filter(
                ({ rect, scrollWidth, clientWidth }) =>
                  rect.right > innerWidth + 1 || scrollWidth > clientWidth + 1,
              )
              .slice(0, 12),
          ),
        );
      }
      expect(
        dimensions.document,
        `${route} horizontal document overflow at ${width}px`,
      ).toBeLessThanOrEqual(width);
      expect(
        dimensions.body,
        `${route} horizontal body overflow at ${width}px`,
      ).toBeLessThanOrEqual(width);
    }
  }
});

test('runs axe on representative routes, errors, forms, history and mobile navigation', async ({
  page,
  browserName,
}) => {
  test.skip(
    browserName !== 'chromium',
    'La auditoría axe representativa se ejecuta en Chromium; los flujos E2E se validan en los tres motores.',
  );
  const fixtures = await installFixtures(page);
  const audit = async (state: string) => {
    const result = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    const violations = result.violations.map((violation) => ({
      id: violation.id,
      impact: violation.impact,
      help: violation.help,
      nodes: violation.nodes.map((node) => ({ target: node.target, summary: node.failureSummary })),
    }));
    console.log(`axe ${state}:`, JSON.stringify(violations));
    expect(violations, `axe violations in ${state}`).toEqual([]);
  };

  await page.goto('/');
  await audit('dashboard');
  await page.goto('/customers');
  await audit('customers-list');
  await page.goto('/customers/new');
  await audit('customer-form-empty');
  await page.getByRole('button', { name: 'Guardar cliente' }).click();
  await expect(page.locator('mat-error').first()).toBeVisible();
  await waitForTransitions(page);
  await audit('customer-form-invalid');
  await page.goto(`/customers/${customerId}`);
  await expect(page.getByRole('heading', { name: customer.legal_name })).toBeVisible();
  await audit('customer-detail-empty-history');
  await page.goto(`/customers/${customerId}/simulations/new`);
  await expect(page.locator('.total')).toHaveText('169,40 €');
  await audit('simulator-current');
  const users = page.locator('#user-count');
  await users.fill('1000001');
  await users.blur();
  await expect(page.locator('#users-error')).toBeVisible();
  await waitForTransitions(page);
  await audit('simulator-invalid');
  await users.fill('15');
  await fixtures.setFxUnavailable(true);
  await page.getByRole('combobox', { name: 'Divisa de visualización' }).click();
  await page.getByRole('option', { name: 'USD — Dólar estadounidense' }).click();
  await expect(
    page.getByRole('alert').getByText(/No se pudo obtener un tipo de cambio/),
  ).toBeVisible();
  await waitForTransitions(page);
  await audit('simulator-fx-error');
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.getByRole('button', { name: 'Menú' }).click();
  const sidebar = page.locator('.sidebar');
  await expect(sidebar).toHaveCSS('transform', 'matrix(1, 0, 0, 1, 0, 0)');
  await waitForTransitions(page);
  await audit('mobile-menu-open-stable');
});

test('captures deterministic TASK045B evidence outside the repository', async ({
  page,
  browserName,
}, testInfo) => {
  const directory = process.env['TASK045B_SCREENSHOT_DIR'];
  test.skip(!directory, 'Defina TASK045B_SCREENSHOT_DIR en una carpeta temporal externa.');
  test.skip(browserName !== 'chromium', 'Las capturas comparables se generan una vez en Chromium.');
  mkdirSync(resolve(directory!), { recursive: true });
  await installFixtures(page);
  const capture = async (name: string) =>
    page.screenshot({ path: resolve(directory!, `${testInfo.project.name}-${name}.png`) });

  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Panel comercial', level: 1 })).toBeVisible();
  await capture('dashboard-contraste-fixture');
  await page.goto('/customers');
  await capture('clientes-fixture');
  await page.goto('/customers/new');
  await expect(page.getByLabel('Razón social')).toBeVisible();
  await capture('alta-selectores-cerrados-fixture');
  await page.getByRole('combobox', { name: 'País' }).click();
  await expect(page.getByRole('listbox')).toBeVisible();
  await waitForTransitions(page);
  await page.keyboard.press('Escape');
  await page.getByRole('listbox').waitFor({ state: 'hidden' });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole('combobox', { name: 'País' }).click();
  await expect(page.getByRole('listbox')).toBeVisible();
  await waitForTransitions(page);
  console.log(
    'TASK045B stable country selector',
    await page.getByRole('listbox').evaluate((panel) => ({
      opacity: getComputedStyle(panel).opacity,
      background: getComputedStyle(panel).backgroundColor,
      animationStates: panel
        .getAnimations({ subtree: true })
        .map((animation) => animation.playState),
      bounds: panel.getBoundingClientRect().toJSON(),
    })),
  );
  await capture('alta-selector-movil-abierto-fixture');
  await page.keyboard.press('Escape');
  await page.getByRole('listbox').waitFor({ state: 'hidden' });
  await page.setViewportSize({ width: 1440, height: 900 });

  await page.route(`**/api/customers/${customerId}`, (route) => route.fulfill({ json: customer }));
  await page.goto(`/customers/${customerId}`);
  await expect(page.getByRole('heading', { name: 'Historial' })).toBeVisible();
  await expect(page.getByText('Aún no hay simulaciones guardadas')).toBeVisible();
  await capture('ficha-historial-vacio-fixture');

  let failFx = false;
  await page.route('**/api/simulations/preview', (route) => {
    const body = route.request().postDataJSON() as { display_currency: string; user_count: number };
    if (failFx && body.display_currency !== 'EUR') {
      return route.fulfill({
        status: 503,
        contentType: 'application/problem+json',
        json: {
          type: 'about:blank',
          title: 'Unavailable',
          status: 503,
          detail: 'fixture FX failure',
        },
      });
    }
    return route.fulfill({ json: estimate(body.display_currency, body.user_count) });
  });
  await page.goto(`/customers/${customerId}/simulations/new`);
  await page.getByRole('spinbutton', { name: 'Almacenamiento contratado (GB)' }).fill('250');
  await page.getByRole('spinbutton', { name: 'Llamadas al servicio / mes' }).fill('100000');
  await expect(page.locator('.total')).toHaveText('169,40 €');
  await capture('simulador-15-desktop-fixture');
  const users = page.locator('#user-count');
  await users.fill('16');
  await expect(page.locator('.total')).toHaveText('179,08 €');
  await capture('simulador-16-desktop-fixture');
  await page.setViewportSize({ width: 390, height: 844 });
  await capture('simulador-16-movil-fixture');
  await users.fill('1000001');
  await users.blur();
  await expect(page.locator('#users-error')).toBeVisible();
  await waitForTransitions(page);
  await capture('simulador-validacion-1000001-fixture');

  await users.fill('16');
  failFx = true;
  await page.getByRole('combobox', { name: 'Divisa de visualización' }).click();
  await page.getByRole('option', { name: 'USD — Dólar estadounidense' }).click();
  await expect(
    page.getByRole('alert').getByText(/No se pudo obtener un tipo de cambio/),
  ).toBeVisible();
  await expect(page.locator('.status')).not.toContainText(/preparando|calculando/i);
  await waitForTransitions(page);
  await capture('error-fx-primera-referencia-fixture');

  await page.getByRole('button', { name: 'Cambiar a EUR' }).click();
  await expect(page.locator('.total')).toHaveText('179,08 €');
  await capture('recuperacion-eur-fixture');
  failFx = false;
  await page.getByRole('combobox', { name: 'Divisa de visualización' }).click();
  await page.getByRole('option', { name: 'USD — Dólar estadounidense' }).click();
  await expect(page.locator('.total')).toHaveText('196,95 US$');
  failFx = true;
  await page.getByRole('combobox', { name: 'Divisa de visualización' }).click();
  await page.getByRole('option', { name: 'GBP — Libra esterlina' }).click();
  await expect(
    page.getByRole('alert').getByText(/No se pudo obtener un tipo de cambio/),
  ).toBeVisible();
  await expect(page.getByText(/Estimación anterior: los parámetros han cambiado/)).toBeVisible();
  await waitForTransitions(page);
  await capture('error-fx-con-preview-obsoleta-fixture');
  await page.getByRole('button', { name: 'Cambiar a EUR' }).click();
  await expect(page.locator('.total')).toHaveText('179,08 €');
  await page.getByRole('button', { name: 'Guardar simulación' }).click();
  await expect(page.getByText(/Simulación guardada/)).toBeVisible();
  await waitForTransitions(page);
  await capture('simulacion-guardada-fixture');
  await page.getByRole('link', { name: 'Ver ficha e historial' }).click();
  await expect(page.getByText('1 simulación')).toBeVisible();
  await expect(page.getByText('179,08 €').last()).toBeVisible();
  await page.reload();
  await expect(page.getByText('179,08 €').last()).toBeVisible();
  await capture('historial-tras-reload-fixture');

  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.getByRole('button', { name: 'Menú' }).click();
  const sidebar = page.locator('.sidebar');
  await expect(sidebar).toHaveCSS('transform', 'matrix(1, 0, 0, 1, 0, 0)');
  await expect(page.getByRole('button', { name: 'Cerrar menú' })).toBeVisible();
  await waitForTransitions(page);
  const sidebarBounds = await sidebar.boundingBox();
  expect(sidebarBounds).not.toBeNull();
  expect(sidebarBounds!.width).toBeGreaterThan(100);
  await capture('menu-movil-abierto-estable-fixture');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('button', { name: 'Menú', exact: true })).toBeFocused();
});
