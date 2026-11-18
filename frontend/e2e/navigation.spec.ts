import { expect, test } from '@playwright/test';

test('loads the dashboard and navigates to the empty customers list', async ({ page }) => {
  await page.route('**/api/customers**', (route) =>
    route.fulfill({ json: { items: [], total: 0, limit: 20, offset: 0 } }),
  );
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Panel comercial', level: 1 })).toBeVisible();
  await expect(page.getByRole('status', { name: '0 clientes registrados' })).toBeVisible();

  await page.getByRole('link', { name: 'Clientes', exact: true }).click();
  await expect(page).toHaveURL(/\/customers$/);
  await expect(page.getByRole('heading', { name: 'Clientes', level: 1 })).toBeVisible();
  await expect(page.getByText('Todavía no hay clientes')).toBeVisible();

  await page.goto('/');
  await page.getByRole('link', { name: 'Nueva simulación' }).click();
  await expect(page).toHaveURL(/\/customers$/);
  await expect(page.getByText(/abre la ficha del cliente que corresponda/i)).toBeVisible();
});

test('supports direct route loading and unknown route recovery', async ({ page }) => {
  await page.route('**/api/customers**', (route) =>
    route.fulfill({ json: { items: [], total: 0, limit: 20, offset: 0 } }),
  );
  await page.goto('/customers/new');
  await expect(page.getByRole('heading', { name: 'Nuevo cliente', level: 1 })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Guardar cliente' })).toBeVisible();

  await page.goto('/not/a/real/route');
  await expect(page.getByRole('heading', { name: 'Página no encontrada', level: 1 })).toBeVisible();
  await page.getByRole('link', { name: 'Ir al inicio' }).click();
  await expect(page).toHaveURL('/');
});

test('opens and closes the mobile navigation with keyboard and route changes', async ({ page }) => {
  await page.route('**/api/customers**', (route) =>
    route.fulfill({ json: { items: [], total: 0, limit: 20, offset: 0 } }),
  );
  await page.setViewportSize({ width: 360, height: 800 });
  await page.goto('/');

  const menuButton = page.getByRole('button', { name: 'Menú', exact: true });
  await menuButton.focus();
  await page.keyboard.press('Enter');
  await expect(menuButton).toHaveAttribute('aria-expanded', 'true');
  await page.keyboard.press('Escape');
  await expect(menuButton).toHaveAttribute('aria-expanded', 'false');
  await expect(menuButton).toBeFocused();

  await menuButton.click();
  await expect(page.getByRole('button', { name: 'Cerrar menú' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Cerrar menú' })).toBeFocused();
  await page.getByRole('button', { name: 'Cerrar menú' }).click();
  await expect(menuButton).toBeFocused();
  await menuButton.click();
  await page
    .getByRole('navigation', { name: 'Navegación principal' })
    .getByRole('link', { name: 'Clientes' })
    .click();
  await expect(page).toHaveURL(/\/customers$/);
  await expect(menuButton).toHaveAttribute('aria-expanded', 'false');
});

test('provides a keyboard skip link to the main content', async ({ page }) => {
  await page.route('**/api/customers**', (route) =>
    route.fulfill({ json: { items: [], total: 0, limit: 6, offset: 0 } }),
  );
  await page.goto('/');
  await page.keyboard.press('Tab');
  const skipLink = page.getByRole('link', { name: 'Saltar al contenido principal' });
  await expect(skipLink).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('#main-content')).toBeFocused();
});

test('keeps the shell within mobile, tablet and desktop viewports', async ({ page }) => {
  await page.route('**/api/customers**', (route) =>
    route.fulfill({ json: { items: [], total: 0, limit: 20, offset: 0 } }),
  );
  for (const width of [320, 390, 768, 1280]) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/');
    const dimensions = await page.evaluate(() => ({
      documentWidth: document.documentElement.scrollWidth,
      viewportWidth: document.documentElement.clientWidth,
    }));
    expect(dimensions.documentWidth, `horizontal overflow at ${width}px`).toBeLessThanOrEqual(
      dimensions.viewportWidth,
    );
  }
});
