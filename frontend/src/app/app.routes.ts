import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    title: 'Panel comercial',
    data: { title: 'Panel comercial' },
    loadComponent: () =>
      import('./features/dashboard/dashboard-page').then((module) => module.DashboardPageComponent),
  },
  {
    path: 'customers',
    title: 'Clientes',
    data: { title: 'Clientes' },
    loadComponent: () =>
      import('./features/customers/customers-page').then((module) => module.CustomersPageComponent),
  },
  {
    path: 'customers/new',
    title: 'Nuevo cliente',
    data: { title: 'Nuevo cliente' },
    loadComponent: () =>
      import('./features/customers/customer-create-page').then(
        (module) => module.CustomerCreatePageComponent,
      ),
  },
  {
    path: 'customers/:customerId/simulations/new',
    title: 'Simulador de suscripción',
    data: { title: 'Simulador de suscripción' },
    loadComponent: () =>
      import('./features/simulations/simulation-page').then(
        (module) => module.SimulationPageComponent,
      ),
  },
  {
    path: 'customers/:customerId',
    title: 'Detalle del cliente',
    data: { title: 'Detalle del cliente' },
    loadComponent: () =>
      import('./features/customers/customer-detail-page').then(
        (module) => module.CustomerDetailPageComponent,
      ),
  },
  {
    path: '**',
    title: 'Página no encontrada',
    data: { title: 'Página no encontrada' },
    loadComponent: () =>
      import('./features/not-found/not-found-page').then((module) => module.NotFoundPageComponent),
  },
];
