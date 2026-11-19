# SPEC-007 — Fundamentos del frontend Angular

| Campo | Valor |
| --- | --- |
| Estado | Aprobada para implementación local por TASK041 |
| Fecha de consulta técnica | 2026-11-18 |
| Decisión de stack | ADR 0003 — Angular 22.2.6 |
| Base de contratos | OpenAPI generado por el backend integrado en `main` |
| Alcance | Base frontend, shell, navegación y servicios técnicos; no flujos comerciales |

## 1. Objetivo

Establecer una base de frontend Angular reproducible, accesible y responsive para
SaaS-O-Matic, organizada por funcionalidades y preparada para consumir la API
FastAPI existente. El backend conserva la autoridad sobre validación y cálculos.

## 2. Usuarios y contexto

Usuarios previstos: equipo comercial interno que registrará y consultará empresas y
preparará estimaciones mensuales. La interfaz inicial se presenta en español. No hay
usuarios autenticados ni roles; no se representa un perfil o datos de negocio ficticios.

## 3. Alcance

- Especificación, plan, tareas y ADR tecnológico.
- Angular standalone, TypeScript estricto, Angular Router, Signals, RxJS,
  Reactive Forms y HttpClient.
- Angular Material/CDK con tema SCSS propio basado en sus APIs públicas.
- Shell responsive, navegación por rutas y pantallas placeholder identificadas como
  preparatorias.
- Configuración central de API y proxy de desarrollo `/api` → FastAPI sin reescritura
  de ruta, porque la API real no tiene prefijo.
- Modelos TypeScript que reproducen el OpenAPI real, incluidos importes en `string`
  y campos históricos nullable.
- Manejo común de errores `application/problem+json` y de transporte, sin retry.
- Vitest para pruebas unitarias y Playwright para smoke E2E de interfaz.
- Comprobación real `GET /api/customers` a través del proxy y SQLite temporal migrada.
- Documentación, exclusiones Git y trazabilidad TASK041.

## 4. Exclusiones

No se implementan listado/alta/detalle/historial funcionales, autenticación,
formularios de negocio, slider, preview, selector de divisa, persistencia de
simulaciones, reglas de negocio en TypeScript, proveedor FX desde navegador,
Docker, despliegue, CI/CD ni cambios al backend. Las pantallas sólo explican que
están pendientes; no simulan resultados o registros.

## 5. Requisitos

### Funcionales

- RF-007-01: mostrar aplicación con marca, navegación Inicio/Clientes y contexto
  accesible de sección.
- RF-007-02: rutas `/`, `/customers`, `/customers/new`,
  `/customers/:customerId`, `/customers/:customerId/simulations/new` y wildcard.
- RF-007-03: navegación hacia simulación sin cliente explica que primero debe
  seleccionarse uno; no crea un cliente ficticio ni simula una operación.
- RF-007-04: navegación móvil abre/cierra menú por teclado y click, y lo cierra al
  navegar.
- RF-007-05: exponer modelos tipados y `ApiClient` configurado para rutas backend.
- RF-007-06: errores remotos se normalizan a mensajes españoles seguros; el POST
  nunca se reintenta automáticamente.
- RF-007-07: mostrar página no encontrada también en acceso directo a URL desconocida.

### No funcionales

- Angular standalone, Angular 22 estable soportado, TypeScript strict, build system
  `application`, estilos SCSS y dependencias con versiones fijadas/lock.
- Responsividad comprobada en 320, 390, 768 y 1280 px, sin scroll horizontal.
- Semántica HTML, teclado, foco visible, `aria-current`, nombre accesible y respeto a
  `prefers-reduced-motion`. WCAG 2.2 AA es objetivo, no declaración de conformidad.
- No incluir secretos ni variables privadas en assets frontend; el proxy solo escucha
  localmente y el backend permanece en loopback.
- Tests offline/deterministas, salvo integración explícita con servicio local.

## 6. Diseño y sistema visual

Producto: **SaaS-O-Matic — Dynamic Billing & Subscription Optimizer**. Paleta inicial:
nav `#0F172A`, primary `#4F46E5`, accent `#6366F1`, fondo `#F8FAFC`, superficie
`#FFFFFF`, texto `#334155`, éxito `#059669`, aviso `#D97706`, error `#DC2626`.
Se validará contraste antes de asignar combinaciones de texto. Tipografía del sistema.
SCSS tokens centralizados para color, espaciado, radio, sombra, tamaño y breakpoints.
La aplicación Material usa el theming API público; no altera selectores internos.

Shell: navegación lateral persistente en escritorio; menú lateral modal en móvil;
barra superior con botón de menú y título de ruta; región principal con `main`,
`router-outlet` y encabezado de página. No hay usuario, campana, notificaciones ni
contadores no respaldados.

## 7. Navegación

| Ruta | Vista de TASK041 | Estado visible |
| --- | --- | --- |
| `/` | Inicio | Base visual/preparatoria, sin métricas |
| `/customers` | Clientes | Listado pendiente de TASK042 |
| `/customers/new` | Nuevo cliente | Formulario pendiente de TASK042 |
| `/customers/:customerId` | Detalle | Detalle/historial pendiente de TASK043 |
| `/customers/:customerId/simulations/new` | Simulación | Simulador pendiente de incremento posterior |
| `**` | No encontrada | Página real de error de navegación |

Las rutas de feature se cargarán de forma diferida donde aporte valor y compartirán
layout y metadatos de título. No hay guards de autenticación. Las vistas placeholder
no disparan peticiones ni ofrecen acciones que aparenten funcionar.

## 8. Arquitectura

```text
frontend/src/app/
  core/       config, http, layout
  shared/     componentes/modelos/utilidades realmente compartidos
  features/   dashboard, customers, simulations, not-found
```

Presentación en componentes standalone; `core/http` contiene cliente tipado,
normalización de errores e interceptor funcional; `core/config` centraliza
`/api`; `shared/models` refleja OpenAPI; `features` agrupa rutas y placeholders.
Signals para estado local de menú/título; RxJS para HttpClient y secuencias
asíncronas. No se añade store global. Formularios de negocio quedan para TASK042.

## 9. Contrato backend

OpenAPI fue generado localmente desde `create_app().openapi()` el 2026-11-18.
Rutas actuales (sin `/api` en servidor):

- `POST /customers`: payload `legal_name`, `tax_id`, `email`, `country`, `plan`;
  respuesta `CustomerResponse`; 201/409/422/500.
- `GET /customers?search=&limit=20&offset=0`: `CustomerPageResponse`, limit 1..100,
  offset ≥0; 200/422/500.
- `GET /customers/{customer_id}`: `CustomerResponse`; 200/404/422/500.
- `GET /customers/{customer_id}/simulations?limit=20&offset=0`:
  `SimulationHistoryPageResponse`; valores antiguos nullable.
- `POST /simulations/preview`: request compartida, respuesta sin id ni created_at;
  200/404/422/500/503.
- `POST /simulations`: respuesta `SimulationResponse`; 201/404/422/500/503.

Enums reales: CountryCode `ES|PT|FR|DE|IT|NL`; PlanCode `standard`; Currency
`EUR|USD|GBP`. `user_subtotal_eur`, todos los importes, tasas y `converted_total`
son strings exactas; UUID son strings; fechas ISO/UTC strings; historial permite
null para consumos y datos fiscales/FX. `billing_period` es el literal `monthly`.
La configuración de `/api` sólo añade el prefijo del proxy en el navegador y lo
quita al reenviar; ninguna URL lleva `/api` al servidor.

No se usa `number` para dinero, no se recalcula subtotal/impuesto/FX en el cliente,
ni se llama a Frankfurter desde Angular. La futura sincronización de tipos debe
verificar diferencias contra `/openapi.json`; generación automática se evalúa en
una tarea posterior, no se añade generador en este scaffold.

## 10. HTTP y errores

`HttpClient` usa raíz central `/api`. Interceptor funcional convierte errores en
`ApiError` con status y campos conocidos de Problem Details (`type`, `title`,
`status`, `detail`, `instance`, `errors[]`). Para conexión sin response y payload
inesperado se producen mensajes generales en español. No se presenta la response
completa, stack ni detail interno 500. Errores de campo se mantienen como texto
de servidor y sólo se exponen en contexto del error controlado. No hay reintentos.

## 11. Accesibilidad y responsive

Un skip link lleva a `main`; regiones `header/nav/main`; niveles de headings
ordenados; links con destinos reales; `aria-current="page"`; toggle con nombre y
estado `aria-expanded`; drawer gestionado por CDK con Escape y restauración de foco.
Foco de navegación se traslada al heading de la ruta. Contraste se verificará con
herramienta; tamaño de targets y zoom se comprobarán manualmente. No se afirma WCAG
conforme sin auditoría externa.

Breakpoints funcionales: móvil 320–390 px, tablet 768 px, escritorio 1280–1440 px.
El sidebar colapsa a drawer y el header evita overflow. `prefers-reduced-motion`
desactiva transiciones no esenciales.

## 12. Pruebas y criterios de aceptación

- Vitest: arranque, rutas/títulos, wildcard, menú responsive/teclado, error mapping,
  URL base y servicios HTTP mockeados. Ningún test llama internet.
- Playwright Chromium: aplicación carga, navegación primary, URL directa, wildcard,
  menú móvil y teclado. Servidor web local reproducible. Smoke E2E, no MVP comercial.
- Integración local: servicio FastAPI backend/.venv, DB SQLite temporal migrada a
  0004, request GET /api/customers via proxy, confirmar status y JSON; cerrar proceso.
- `npm ci`, lint/TypeScript, Vitest sin watch, build production, Playwright y npm audit.
- Inspección responsive/teclado visual con Chromium disponible; cualquier limitación
  se informa sin declarar conformidad no comprobada.

## 13. Dependencias elegidas

Según documentación oficial y registry consultado 2026-11-18: Angular/Core/CLI/Build
22.2.6; Material/CDK 22.2.6; TypeScript 6.0.3; RxJS 7.8.2; Vitest 5.1.1; Playwright
Test 1.65.1; ESLint 10.15.0 con angular-eslint 22.8.0/typescript-eslint 8.73.0;
Prettier 3.8.1 y jsdom 30.1.3. Angular 22 requiere Node `^22.22.3 || ^24.15.0 || ^26`; local
24.22.0 es compatible y es Node LTS. Angular 22 admite TypeScript `>=6.0 <6.1`,
RxJS 6.5.3/7.4+, Vitest 4.0.8/5+, y Material/CDK coincidentes. Material, CDK, Angular
CLI y build son dependencias de producción/desarrollo según su rol; `npm` es el gestor.
Playwright instala Chromium solo cuando se ejecuta su instalador explícito.

Fuentes oficiales/versionadas y consultadas 2026-11-18:
[Angular releases](https://angular.dev/reference/releases),
[Angular compatibility](https://angular.dev/reference/versions),
[local setup](https://angular.dev/tools/cli/setup-local),
[CLI serving/proxy](https://angular.dev/tools/cli/serve),
[Vitest testing](https://angular.dev/guide/testing),
[HTTP](https://angular.dev/guide/http/setup),
[routing](https://angular.dev/guide/routing),
[reactive forms](https://angular.dev/guide/forms/reactive-forms),
[a11y](https://angular.dev/best-practices/a11y),
[application builder](https://angular.dev/tools/cli/build-system-migration),
[Node releases](https://nodejs.org/en/about/previous-releases),
[Playwright install/system requirements](https://playwright.dev/docs/intro),
[Material](https://material.angular.dev/).
Material peer metadata and package versions were additionally checked via npm registry.

## 14. Restricciones y decisiones pendientes

- No P-05: deployment/SQLite production unresolved.
- No autenticación, CORS backend, SSR, internacionalización framework, app state
  library, CSS framework parallel, real customers or commercial operation.
- No claim of full WCAG AA, visual E2E, production security or full MVP.
- Confirmar con owner si desea branding/contraste alternativo antes de feature UI.
- Confirmar futura política de URLs por environment si aparece un entorno distinto
  al proxy local.
