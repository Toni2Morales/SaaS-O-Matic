# SaaS-O-Matic — frontend

Frontend Angular para el uso comercial interno. TASK042 conecta dashboard, clientes,
alta internacional, ficha e historial. TASK043 añade simulador con previsualización
reactiva y persistencia explícita. FastAPI es la autoridad exclusiva de precios,
impuestos y conversiones; los importes/tipos se conservan como cadenas decimales.
TASK044 refina mensajes, validación, accesibilidad de navegación y controles responsive.
En móvil el resumen de la estimación es compacto y no sticky para evitar tapar campos.
TASK045 auditó el frontend y confirmó observaciones sobre contraste de texto y el estado
accesible tras un error FX. TASK045B corrige esas observaciones y refuerza la cobertura;
TASK045BP publica las correcciones en `feature/mvp-frontend`; aún no están integradas en
`main`.

## Versiones

- Node.js 24 LTS (local verificado: 24.22.0; rango requerido `>=24.15.0 <25`).
- npm 11 (local verificado: 11.19.1; `packageManager` fijado en el manifiesto).
- Angular/CLI/Material/CDK 22.2.6, TypeScript 6.0.3, RxJS 7.8.2.
- Vitest 5.1.1, Playwright Test 1.65.1, axe-playwright 4.14.0 (MPL-2.0, dev) y
  coverage-v8 5.1.1 (MIT, dev).
- ESLint 10.15.0, angular-eslint 22.8.0, Prettier 3.8.1.

Las dependencias directas están fijadas sin rangos y se conserva `package-lock.json`.
Para instalar el árbol reproducible sin ejecutar scripts de terceros (incluidos los
cuatro scripts opcionales aún bloqueados), usa `npm ci --ignore-scripts` desde este
directorio. No se requiere CLI global ni cambiar Node/npm global. El build, los tests y
los browsers Playwright se deben validar después de la instalación.

## Arranque local

Requiere backend Python 3.13 y el entorno `backend/.venv` instalado con sus dependencias.
Terminal 1, desde `backend/`:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn saas_o_matic.bootstrap.main:app --host 127.0.0.1 --port 8000
```

Terminal 2, desde `frontend/`:

```powershell
npm ci --ignore-scripts
npm start
```

Abrir `http://127.0.0.1:4200`. Angular sólo enlaza a loopback. El proxy de desarrollo
reenvía `/api/...` a `http://127.0.0.1:8000/...` quitando el prefijo artificial
`/api`, puesto que los endpoints reales no tienen prefijo. No se ha añadido CORS ni
modificado el backend. El proxy no se incluye en builds de producción; P-05 sigue
pendiente. Angular no llama directamente a Frankfurter: las previews pasan por FastAPI,
que conserva la autoridad económica y obtiene las referencias FX.

TASK045 encontró dos defectos de severidad media (contraste de algunos textos y anuncio de
estado después de error FX); TASK045B los corrige. La integración real utiliza SQLite
temporal con migraciones 0001–0004; no reutilice la base de datos predeterminada para
pruebas. Las auditorías de accesibilidad son parciales y no constituyen certificación
WCAG AA.

No se debe usar la base SQLite predeterminada para pruebas de integración; crear una
SQLite temporal y migrarla hasta `0004_add_simulation_taxes_and_fx`.

## Estructura

- `src/app/core/`: configuración, HTTP, layout y shell.
- `src/app/shared/`: modelos y componentes reutilizables usados.
- `src/app/features/`: dashboard, clientes, simulaciones y página 404.
- `src/app/features/customers/data-access/`: servicios HTTP tipados de clientes e historial.
- `src/app/shared/utils/display-format.ts`: presentación decimal exacta y fechas.
- `src/proxy.conf.json`: proxy de desarrollo validado con Angular CLI 22.
- `e2e/`: pruebas Playwright en Chromium, Firefox y WebKit.

El contrato se copia fielmente del OpenAPI real. Importes y tipos de cambio son
`string`; UUID son strings; fechas son strings ISO; los campos históricos desconocidos
mantienen `null`. Antes de cambiar modelos, contrastar `/openapi.json`. No se usa un
generador OpenAPI en esta base para evitar dependencia adicional; su incorporación
se evaluará si la sincronización manual se vuelve costosa.

## Comandos

Desde `frontend/`:

| Comando                                          | Uso                                                           |
| ------------------------------------------------ | ------------------------------------------------------------- |
| `npm start`                                      | Servidor local en `127.0.0.1:4200`, con proxy API             |
| `npm run build`                                  | Compilación optimizada de producción                          |
| `npm run watch`                                  | Build de desarrollo en modo watch                             |
| `npm run typecheck`                              | TypeScript estricto para la app                               |
| `npm run lint`                                   | ESLint y reglas Angular/plantillas                            |
| `npm test`                                       | Vitest una sola ejecución (CLI Angular)                       |
| `npm run test:coverage`                          | Vitest con V8; coverage texto/resumen JSON                    |
| `npm run test:watch`                             | Vitest interactivo                                            |
| `npm run e2e`                                    | Playwright en tres motores; arranca y detiene el servidor web |
| `npx playwright install chromium firefox webkit` | Instala los tres browsers oficiales de Playwright             |
| `npm run format:check`                           | Verificación Prettier, sin escribir cambios                   |
| `npm audit`                                      | Consulta de advisories del registry; revisar antes de actuar  |

No ejecutar `npm audit fix` automáticamente ni ignorar peer conflicts con force.

## Pruebas y alcance actual

Vitest prueba servicios, cancelación, formularios, errores, formatos, historial y
simulador sin servicios externos. Playwright incluye fixtures interceptados, captura
visual opt-in (`TASK043_SCREENSHOT_DIR`) y un escenario real `TASK042_REAL_API=1` con
FastAPI/SQLite temporal y datos sintéticos. La prueba real usa EUR para el flujo
determinista; USD/GBP se consultan de forma puntual y separada.

Resultados TASK043: **37 unitarias / 11 archivos**. La corrida E2E completa ejecutó
19 tests: 17 pasaron y omitió explícitamente la integración y la captura opt-in; la
integración real y captura visual se ejecutaron en corridas dedicadas (1 pasada cada
una). TypeScript, ESLint, Prettier y build de producción pasan. Backend: 579 pruebas
Pytest superadas. No se midió coverage.

TASK045B incorpora `@axe-core/playwright` 4.14.0 (dev, MPL-2.0; axe-core MPL-2.0) y
`@vitest/coverage-v8` 5.1.1 (dev, MIT; peer exacto Vitest). Las instalaciones se hacen
con `--ignore-scripts`; no se ejecutan scripts de dependencias.

Resultados TASK045B reproducidos en este corte: **Vitest 40/40**; statements 86,20 %,
branches 81,86 %, functions 67,19 %, lines 86,84 %; build inicial 395,13 kB raw.
Playwright en copia limpia: **79 pasadas / 20 skips opt-in de 99 ejecuciones** entre
Chromium, Firefox y WebKit; la integración real y capturas se ejecutaron aparte con
servicios/datos aislados. La auditoría axe pasa en nueve estados representativos de
Chromium. El `npm run e2e` del árbol habitual tuvo una caída del servidor de desarrollo al
cambiar de motor y no se cuenta como PASS; la repetición completa en copia limpia pasó.
A45-01/02 y las incidencias axe confirmadas se corrigieron; no se certifica WCAG AA. La
integración real TASK045B utiliza FastAPI/SQLite migrada y proveedor FX fixture inyectado;
la consulta Frankfurter real se registra por separado. El backend permanece 579/579
Pytest.

Los cuatro scripts previamente pendientes (`@parcel/watcher`, `esbuild`, `lmdb`,
`msgpackr-extract`) siguen bloqueados. No ejecutar `npm audit fix`.

La navegación móvil y los estados funcionales aplican fundamentos de accesibilidad;
WCAG 2.2 AA es objetivo, no conformidad auditada. No hay autenticación, SSR ni
despliegue.

`npm run test:coverage` mide statements, branches, functions y lines sobre
`src/app/**/*.ts`; excluye specs `src/**/*.spec.ts`. Los informes quedan en
`frontend/coverage/` (ignorado por Git). Las pruebas Playwright pueden ejecutarse con
Chromium, Firefox y WebKit. La auditoría axe automatizada se integra en E2E; sus
resultados son controles parciales, no certificación WCAG AA.

Las capturas de TASK042 y TASK043 se guardan fuera del repositorio. Detalle de TASK043:
[SPEC-009](../docs/specs/009-interactive-subscription-simulator/spec.md) e
[informe](../ai-workspace/01-tasks/TASK043-interactive-subscription-simulator.md).
