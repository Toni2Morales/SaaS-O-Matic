import { expect, test } from '@playwright/test';

test('loads the dashboard and navigates to the empty customers list', async ({ page }) => {
  await page.route('**/api/customers**', (route) =>
    route.fulfill({ json: { items: [], total: 0, limit: 20, offset: 0 } }),
  );
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Panel comercial', level: 1 })).toBeVisible();
  await expect(page.getByRole('status', { name: '0 clientes registrados' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Saltar al contenido principal' })).not.toBeFocused();

  await page.getByRole('link', { name: 'Clientes', exact: true }).click();
  await expect(page).toHaveURL(/\/customers$/);
  await expect(page.getByRole('heading', { name: 'Clientes', level: 1 })).toBeVisible();
  await expect(page.locator('#page-title')).toBeFocused();
  const headingGeometry = await page.evaluate(() => ({
    headingTop: document.querySelector('#page-title')?.getBoundingClientRect().top ?? -1,
    topbarBottom: document.querySelector('.topbar')?.getBoundingClientRect().bottom ?? 0,
  }));
  expect(headingGeometry.headingTop).toBeGreaterThanOrEqual(headingGeometry.topbarBottom);
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
  await expect(page.locator('#page-title')).toBeFocused();
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
  const mobileSidebar = await page.locator('.sidebar').boundingBox();
  expect(mobileSidebar?.width).toBeGreaterThan(200);
  await expect(page.getByRole('button', { name: 'Cerrar navegación' })).toBeVisible();
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
  await expect(page.locator('#page-title')).not.toBeFocused();
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
    await page.goto('/');
    const dimensions = await page.evaluate(() => ({
      documentWidth: document.documentElement.scrollWidth,
      viewportWidth: document.documentElement.clientWidth,
    }));
    expect(
      dimensions.documentWidth,
      `horizontal overflow at ${viewport.width}×${viewport.height}`,
    ).toBeLessThanOrEqual(dimensions.viewportWidth);
  }
});
