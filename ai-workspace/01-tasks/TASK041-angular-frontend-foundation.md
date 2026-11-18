# TASK041 — Arquitectura, configuración y diseño base del frontend Angular

| Campo | Valor |
| --- | --- |
| Fecha | 2026-11-18 |
| Estado | Implementada y validada localmente; sin staging ni publicación |
| Rama | `feature/mvp-frontend`, creada desde `origin/main` |
| Base | `23cc43b486d20f7995a2cf29375e3f724f3c7c3f` |
| Merge backend | PR #6, commit integrado `23cc43b486d20f7995a2cf29375e3f724f3c7c3f` |
| Alcance | SPEC-007, ADR 0003 y base Angular; sin flujos comerciales |

## 1. Resumen ejecutivo

TASK041 crea una base frontend Angular reproducible con shell responsive, rutas
preparatorias, modelos TypeScript basados en OpenAPI, cliente HTTP, proxy local,
Problem Details, Vitest y Playwright. Las rutas existen pero no implementan alta,
búsqueda, detalle, historial o simulación. No se inició TASK042, no se tocó código
funcional del backend y no se realizó ninguna operación de publicación.

## 2. Estado Git inicial y final

### Inicial

- Rama: `feature/mvp-backend`; HEAD: `7249b26de86b54fd686a4d1dc63221ffd5451b78`.
- `main` local: `8371f9f608ce6e06984cc501d8240e1b7edf34d5`.
- Índice vacío; único archivo local no seguido:
  `Prueba Devs con IA.docx`.
- `git fetch origin` confirmó `origin/main` en el merge #6 esperado.
- Se capturaron 13 hashes protegidos fuera del repositorio antes de crear rama.

### Rama y estado final

- Rama nueva: `feature/mvp-frontend`, creada con
  `git switch -c feature/mvp-frontend origin/main`.
- HEAD es el commit base `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`; no hay commits.
- Main local no se actualizó ni modificó.
- Índice vacío. El DOCX sigue sin seguimiento, sin modificación y fuera de Git.
- El árbol contiene sólo cambios locales autorizados y el DOCX excluido.

## 3. Rama base e integridad histórica

`origin/main` coincidía con `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`. El remoto
es el repositorio autorizado. Los 13 ficheros protegidos SHA-256 (TASK035–TASK040,
LICENSE, lock backend y migraciones 0001–0004) siguen idénticos. El DOCX mantiene
la huella `63fbd74eed52eb5b8f2495e46ffd82e059c8421892c3b6b8517aaed2a9741cdf`.
Se abrió localmente sólo en modo lectura para extraer texto del reto; no se modificó,
añadió ni publicó.

## 4. Fuentes leídas y contratos contrastados

Se consultaron AGENTS.md, proceso, README raíz/backend, requisitos, trazabilidad,
roadmap, ADR 0001/0002, contexto del proyecto, SPEC-001–006 y TASK035–TASK040.
El `.docx` original se inspeccionó localmente sin escribirlo. La base de verdad del
contrato se contrastó con `create_app().openapi()` y los esquemas/router Python, no
sólo con informes de tarea.

OpenAPI confirma seis rutas backend: `POST /customers`, `GET /customers`,
`GET /customers/{customer_id}`, `GET /customers/{customer_id}/simulations`,
`POST /simulations/preview` y `POST /simulations`. Cuerpos/queries y status se
reflejan en SPEC-007. No se agregó `/api` al backend; el prefijo pertenece sólo al
proxy local Angular.

## 5. Resolución P-01

P-01 se resuelve para esta base frontend mediante ADR 0003. Versiones directas:

| Paquete/entorno | Versión fijada |
| --- | --- |
| Node | 24.22.0 local; `.nvmrc`; engines `>=24.15.0 <25` |
| npm | 11.19.1 local; `packageManager` exacto y engines `>=11 <12` |
| Angular core/CLI/build | 22.2.6 |
| Angular Material/CDK | 22.2.6 |
| TypeScript | 6.0.3, strict |
| RxJS | 7.8.2 |
| Vitest | 5.1.1 |
| Playwright Test | 1.65.1 |
| ESLint / @eslint/js | 10.15.0 / 10.0.1 |
| angular-eslint / typescript-eslint | 22.8.0 / 8.73.0 |
| jsdom / Prettier | 30.1.3 / 3.8.1 |

La selección fue comprobada el 2026-11-18 contra la matriz oficial Angular:
Angular 22 acepta Node `^22.22.3 || ^24.15.0 || ^26`, TS `>=6.0 <6.1`, RxJS 6.5.3/7.4+;
Material/CDK mantienen versiones iguales y peer compatibles; Angular build admite
Vitest 4/5; ESLint/TypeScript-ESLint peers aceptan las versiones fijadas. Angular 22
está en soporte Active. Node 24 está en LTS. No se instaló CLI global ni se modificó
Node/npm del sistema.

Fuentes oficiales con fecha de consulta 2026-11-18:

- https://angular.dev/reference/versions y https://angular.dev/reference/releases
- https://angular.dev/tools/cli/setup-local
- https://angular.dev/tools/cli/build-system-migration
- https://angular.dev/guide/testing y /guide/testing/migrating-to-vitest
- https://angular.dev/tools/cli/serve (proxy Vite/Angular)
- https://angular.dev/guide/http/setup, /guide/routing y /guide/forms/reactive-forms
- https://angular.dev/best-practices/a11y
- https://material.angular.dev/
- https://nodejs.org/en/about/previous-releases
- https://playwright.dev/docs/intro
- Registry npm consultado para versiones y `peerDependencies` exactas.

## 6. Dependencias directas y justificación

**Runtime (10):** `@angular/cdk`, `@angular/material`, `@angular/common`,
`@angular/compiler`, `@angular/core`, `@angular/forms`, `@angular/platform-browser`,
`@angular/router`, `rxjs`, `tslib`. Material/CDK sustentan controles, layout y
breakpoints; el resto es framework/plataforma y reactive HTTP.

**Desarrollo (13):** `@angular/cli`, `@angular/build`, `@angular/compiler-cli`,
`@angular-eslint/schematics`, `@eslint/js`, `@playwright/test`, `angular-eslint`,
`eslint`, `jsdom`, `prettier`, `typescript`, `typescript-eslint`, `vitest`.
CLI/build/compiler para desarrollo; Vitest/jsdom para unidad; Playwright para smoke;
ESLint/Angular ESLint para TS y templates; Prettier para formato. `package-lock.json`
fija el árbol transitivo; `npm ci` reconstruyó 403 paquetes auditados. No se añadió
store global, Tailwind, Bootstrap, generador OpenAPI, icon font, fuente remota ni FX
en navegador.

Durante el primer scaffolding el CLI generó una dependencia Angular animations obsoleta;
se quitó antes del lock final. También se cambió ESLint 9 a ESLint 10.15.0 tras el
aviso de versión no soportada; angular-eslint/TypeScript-ESLint confirman peer range.

## 7. Arquitectura y árbol

```text
frontend/
  src/app/core/config/       API base
  src/app/core/http/         ApiClient, errores, interceptor
  src/app/core/layout/       shell, navegación y layout
  src/app/shared/components/ encabezado, placeholder y error
  src/app/shared/models/     modelos TypeScript OpenAPI
  src/app/features/dashboard/
  src/app/features/customers/
  src/app/features/simulations/
  src/app/features/not-found/
  src/styles.scss            tokens y tema Material
  src/proxy.conf.json        proxy desarrollo
  e2e/                       Playwright Chromium
```

Standalone components, imports por componente, lazy route loading, inyección
Angular, Signals para estado local del menú/título y RxJS para HTTP. No existe un
estado global. Angular usa el builder `application`; no se genera SSR. Modelos están
en `shared/models`; no se trasladan fórmulas del dominio backend.

## 8. Sistema visual y layout

Marca SaaS-O-Matic / “Dynamic Billing & Subscription Optimizer”. La base usa
Material theming API pública SCSS (`mat.theme`) con paletas Material violeta/azure,
y tokens de marca aprobados para navegación `#0F172A`, primario `#4F46E5`, acento
`#6366F1`, fondo `#F8FAFC`, superficie `#FFFFFF`, texto `#334155`, éxito `#059669`,
aviso `#D97706` y error `#DC2626`. Tipografía de sistema; no se descarga font externa.
Tokens de espaciado, radios, borde y sombra en un único stylesheet.

Shell con sidebar desktop, drawer/disclosure móvil por CSS, marca textual, Inicio,
Clientes, indicador de ruta activa, barra superior y área principal. No hay perfil,
campana ni indicadores ficticios. Las pantallas muestran expresamente “pendiente” y
no solicitan datos ni simulan operaciones.

## 9. Rutas y componentes compartidos

Implementadas `/`, `/customers`, `/customers/new`,
`/customers/:customerId`, `/customers/:customerId/simulations/new` y wildcard.
Rutas estáticas antes de parámetro; títulos por ruta; no authentication guards.
La vista simulador sólo explica que depende de un cliente registrado y es futura.

Compartidos concretos: `PagePlaceholderComponent` y `SectionHeadingComponent`.
El estado de error se normaliza en el interceptor/`ApiError`. Loading/empty comerciales no se añadieron al no existir
peticiones/vistas de datos en este alcance. No se crea una librería excesiva.

## 10. Responsive y accesibilidad

E2E comprueba viewport 320, 390, 768 y 1280 px sin overflow horizontal. Sidebar se
adapta; menú móvil abre/cierra por teclado y click, Escape restaura foco, selección de
ruta lo cierra. Landmarks `nav/main`, skip-free headings, `aria-current`, `aria-expanded`,
labels y foco visible; transiciones respetan `prefers-reduced-motion`. Screenshots
reales temporales se inspeccionaron a 1440×1000 y 360×800. Contrastes principales se
revisaron visualmente. No se ejecutó axe ni auditoría WCAG completa; no se declara AA.

## 11. Modelos y HTTP

Tipos reales: Country `ES|PT|FR|DE|IT|NL`; Plan `standard`; Currency `EUR|USD|GBP`;
`billing_period: 'monthly'`. UUID y fechas son strings. Importes/tasas como strings,
nunca `number`; campos antiguos de consumo/fiscal/FX conservan `null`. Requests y
response reflejan OpenAPI para alta, consultas, preview, simulación e historial.
El método `ApiClient` inicial sólo ofrece GET tipado para validar la base y proxy; no
se implementa la lista funcional.

`API_BASE_URL` centraliza `/api`; `src/proxy.conf.json` reescribe a
`http://127.0.0.1:8000` y retira sólo el prefijo. No se añade CORS, se enlaza a loopback
y Angular no llama a Frankfurter. `ProblemDetails` se valida por forma, se normaliza
a mensajes generales españoles por status y no conserva/expone detail de servidor;
422 mantiene errores de campo tipados. Se cubren 400/404/409/422/500/503, conexión
y cuerpo inesperado en mapping; sin retry.

Los tipos deben contrastarse con `/openapi.json` en cada cambio de contrato. No se
añadió codegen por scope/tamaño.

## 12. Pruebas y resultados

Ejecutado con versiones fijadas:

- `npm ci`: correcto; 403 paquetes auditados.
- `npm run typecheck`: correcto (TypeScript app strict).
- `npm run lint`: All files pass linting.
- `npm run format:check`: All matched files use Prettier style.
- `npm test`: **9 passed, 4 test files**, Vitest sin watch.
- `npm run build`: correcto; bundle inicial final 337.14 kB raw y lazy chunks por ruta.
- `npm run e2e`: **4 passed en Chromium (9.6 s)** — inicio, navegación, ruta directa/404,
  teclado/móvil y overflow en cuatro anchuras.
- `npx playwright install chromium`: navegador instalado en cache del usuario, no Git.
- Screenshots temporales reales: desktop y móvil, guardados bajo el temp aprobado.
- Integración local: SQLite temporal migrada 0001→0004; GET `/api/customers` a través
  del proxy respondió **HTTP 200 application/json**, `{items:[], total:0, limit:20,
  offset:0}`. Se detuvieron ambos procesos y se eliminaron DB y logs temporales.
- Backend: **579 passed en 46.37s** usando exclusivamente `backend/.venv`.

No se ejecutaron pruebas en Firefox/WebKit, axe, SAST/DAST ni cobertura. Smoke E2E no
es prueba del flujo comercial completo.

## 13. npm audit y scripts

`npm audit` terminó con status no-cero y reportó **21 high, 0 critical, 0 moderate,
0 low**. Advisories se agrupan principalmente por `picomatch` ReDoS
GHSA-fc5q-39xc-vjpf (la versión resoluble era 4.0.7 y el registry consultado aún no
ofrecía 4.0.8), propagado por Angular CLI/build, Vite, Vitest, angular-eslint y
typescript-eslint. `npm audit` no ofrece una actualización compatible directa para
Angular build/Vitest; algunas “fixAvailable” implican downgrades de Angular ESLint o
typescript-eslint. No se ejecutó `npm audit fix`, no se añadió override ni se ocultó
el resultado. Es riesgo pendiente de revisión y actualización compatible upstream.

npm 11 avisó de cuatro install scripts no aprobados (`@parcel/watcher`, `esbuild`,
`lmdb`, `msgpackr-extract`). No se aprobó ni ejecutó una allowlist de scripts; con
los paquetes instalados, ci, build, Vitest y Playwright se ejecutaron correctamente.
El aviso queda registrado para confirmar si alguna instalación limpia futura necesita
permitir scripts específicos.

## 14. Archivos, exclusiones y seguridad

Inventario: **59 candidatos publicables** (9 ficheros existentes modificados y 50
nuevos), más el DOCX original excluido. Nuevos: `frontend/` (fuentes, package.json,
package-lock, configuración, tests y README), SPEC-007, ADR 0003 y este registro.
Modificados: `.gitignore`, README raíz/backend, ai-workspace README/contexto, ADR 0001,
requisitos, matriz y roadmap. No se cambiaron backend source/tests, migraciones,
requirements.lock ni LICENSE. No se modificaron TASK035–TASK040. El archivo del reto
y archivos de entorno locales siguen excluidos; build/cache/node_modules/Playwright
output están ignorados.

Escaneo dirigido de candidatos no encontró credenciales, claves privadas, tokens
reconocibles ni rutas privadas. Revisión dirigida, no SAST ni garantía absoluta.
`git diff --check` limpio; 13 hashes históricos protegidos idénticos. SQLite temporal
eliminada; base predeterminada no se modificó.

## 15. Estado de criterios y pendientes

Completados localmente: base desde merge correcto, rama autorizada, SPEC-007 antes
del scaffold, P-01/ADR 0003, versiones/lock reproducibles, standalone/strict,
arquitectura modular, Material/theming, tokens, shell, rutas/404, responsive, foco y
landmarks, contratos HTTP fieles, proxy e integración real, errores seguros, Vitest,
Playwright, build, README, backend 579 tests y protección de históricos.

Pendientes/limitados: pantallas/flows comerciales, E2E funcional, auditoría WCAG AA,
assistive tech, browsers adicionales, resolución de advisories npm, aprobación de
scripts opcionales si procediera, CI/CD, P-05/despliegue y fase TASK042. No hay
staging, commit, push, PR ni merge. TASK042 no se inició.

## 16. Próximos pasos

Esperar revisión del propietario. TASK042 — listado/alta funcional de clientes — sólo
comenzará tras autorización expresa. No iniciar formularios de negocio ni otras
features en TASK041.
