# TASK042 — Dashboard y gestión comercial de clientes

| Campo | Valor |
| --- | --- |
| Fecha | 2026-11-18 |
| Estado | Implementada y validada localmente; sin staging ni publicación |
| Rama | `feature/mvp-frontend` (misma rama de TASK041) |
| Base / HEAD esperado | `23cc43b486d20f7995a2cf29375e3f724f3c7c3f` |
| Main local esperado | `8371f9f608ce6e06984cc501d8240e1b7edf34d5` |
| Especificación | [SPEC-008](../../docs/specs/008-customer-management-frontend/spec.md) |
| Plan / tareas | [plan](../../docs/specs/008-customer-management-frontend/plan.md) · [tasks](../../docs/specs/008-customer-management-frontend/tasks.md) |

## 1. Resumen ejecutivo

TASK042 completa localmente dashboard comercial, listado/búsqueda/paginación de
clientes, alta internacional, ficha e historial paginado, estados de interfaz y
mejoras del shell. El backend sigue siendo la fuente de validación, persistencia,
orden, snapshots y cálculos. Se verificó un recorrido real desde Chromium por el
proxy Angular hasta FastAPI y SQLite temporal, con clientes sintéticos ES/PT, conflicto
fiscal, búsqueda, ficha, simulación preparada mediante el endpoint existente, historial
y persistencia tras recargar.

El simulador no se implementa: TASK043 sigue pendiente. No hubo cambios a dependencias,
`package.json`, `package-lock.json`, backend funcional, migraciones ni `LICENSE`.

## 2. Estado Git y manifiesto inicial

### Verificación inicial

- Rama `feature/mvp-frontend`.
- HEAD, `origin/main`: `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`.
- `main` local: `8371f9f608ce6e06984cc501d8240e1b7edf34d5`.
- Índice vacío; 9 archivos existentes modificados y 50 nuevos candidatos de TASK041
  (59 candidatos acumulados). El DOCX original estaba aparte y sin seguimiento.
- No se creó rama ni se actualizó `main`.

Se materializó [TASK042-initial-hashes.json](TASK042-initial-hashes.json) con SHA-256
de los 59 candidatos de partida, 14 rutas protegidas (incluye el registro TASK041) y
39 ficheros históricos de tarea TASK001–TASK041. Todos los paths son relativos. Los
registros ya versionados se verificaron contra HEAD inicial, y el informe TASK041 sin
seguimiento contra el inventario candidato inicial. El manifiesto identifica el DOCX
sólo por nombre/hash, no lo incorpora al inventario. La huella
`63fbd74eed52eb5b8f2495e46ffd82e059c8421892c3b6b8517aaed2a9741cdf` coincide con la
huella previa documentada; el DOCX no se leyó ni modificó durante TASK042.

### Estado final

- Misma rama y HEAD base; `main` local intacta.
- Índice vacío. Cero staging, commit, push, PR, merge, rebase, stash, reset, clean o
  cambio de rama.
- El DOCX original sigue sin seguimiento y fuera de Git.

## 3. Lectura y contrato contrastado

Se revisaron README raíz/backend/frontend, requisitos, matriz, roadmap, ADR 0001–0003,
SPEC-001–007, tareas TASK035–041, modelos TypeScript, configuración Angular y tests.
Los contratos se confirmaron con `backend/.venv` y el OpenAPI generado desde la
implementación actual, además de schemas/routers Python:

- `GET /customers`: search opcional (trim, hasta 255), limit 1..100 (default 20),
  offset ≥0; devuelve items/total/limit/offset, orden nombre casefold ASC e UUID ASC.
- `POST /customers`: cinco campos requeridos; 201 response, 409 duplicado, 422
  validación, 500 controlado.
- `GET /customers/{customer_id}`: 200, 404 y 422/500 Problem Details.
- `GET /customers/{customer_id}/simulations`: limit/offset reales, orden fecha/id DESC,
  404/422/500; consumos, snapshots y created_at históricos pueden ser null.
- `ProblemDetails`: type/title/status/detail obligatorios; instance/errors nullable u
  opcionales; cada field error requiere field/message.

No se añadieron endpoints, reglas fiscales, consultas SQL desde Angular ni lógica de
precios/impuestos/FX. El prefijo `/api` sólo existe en el proxy local.

## 4. Evaluación de `npm audit` antes del código

Se ejecutaron `npm audit --json`, `npm audit --omit=dev --json`, `npm ls` y `npm
explain` sobre `picomatch`, Vite/esbuild y los cuatro paquetes con install scripts.
El registro de TASK041 reportaba **21 high** —avisos propagados por dependencias
superiores— que se consolidaban en una única advisory:

| Campo | Resultado al inicio de TASK042 |
| --- | --- |
| Advisory única | GHSA-fc5q-39xc-vjpf / CVE-2026-112366 |
| Paquete/versión en lock | `picomatch@4.0.7` |
| Rango publicado originalmente | `<=4.0.7` |
| Severidad original | High, CVSS 8.7 |
| Corrección publicada | Ninguna; `4.0.7` era la última versión disponible en npm |
| Clasificación | Sólo árbol de desarrollo/build/test; no runtime/prod dependency |
| Cadenas | Angular DevKit/build/CLI, Vite/tinyglobby/Sass watcher, Vitest y tooling ESLint |

La descripción original alegaba backtracking ReDoS al procesar patrones extglob
repetidos controlados por un atacante. El upstream del proyecto disputó la premisa y
cerró sin merge el PR correctivo; GitHub retiró la advisory el **2026-11-18**. Fuentes
consultadas en esa fecha:

- [GitHub Advisory GHSA-fc5q-39xc-vjpf / CVE-2026-112366](https://github.com/advisories/GHSA-fc5q-39xc-vjpf) — estado Withdrawn.
- [Comentario del mantenedor en picomatch PR #235](https://github.com/micromatch/picomatch/pull/235#issuecomment-6315749381) — disputa del reporte y condición de no aceptar patrones/reglas no confiables.
- [NVD CVE-2026-112366](https://nvd.nist.gov/vuln/detail/CVE-2026-112366) — referencia listada por el advisory histórico.

### Exposición y mitigación

- TASK042 no instala paquetes ni ejecuta `npm update`, `npm audit fix`, `--force`,
  overrides ni downgrades. `package.json` y `package-lock.json` se mantienen.
- La aplicación terminada es assets estáticos. `picomatch` aparece en ramas de
  dependencias de desarrollo; `npm audit --omit=dev` queda limpio y
  `npm ls picomatch --omit=dev` no devuelve paquete. No hay evidencia de `picomatch`
  en el bundle de runtime ni de que la búsqueda de clientes se convierta en glob:
  usa `HttpParams` y el servidor realiza búsqueda literal/Unicode.
- Las condiciones originales requerían que un actor pudiera introducir patrones
  extglob a un proceso que ejecutase `picomatch`. La UI no acepta esos patrones. El
  tooling sí usa patrones de archivos/configuración durante build y tests: un actor
  que controle localmente código/config o un proyecto de build podría influir en ese
  contexto. No se afirma inmunidad absoluta por ser dev dependency; el dev server es
  loopback por configuración. No se demostró exposición remota del producto.
- No se presenta la controversia como aceptación definitiva del propietario. Riesgo
  de supply-chain/criterio de advisory a reevaluar en TASK045 y si cambia el feed.

### Resultado de auditoría al cierre

El feed vigente ya no reporta la advisory retirada:

- `npm audit --json`: **0 info, 0 low, 0 moderate, 0 high, 0 critical; total 0**.
- `npm audit --omit=dev --json`: **0 en todas las severidades**.
- No hay advisory activa única relevante ni corrección de versión que aplicar.

Cuatro install scripts siguen sin autorización npm: `@parcel/watcher@2.6.0`
(`node-gyp rebuild`, optional Sass/build watcher), `esbuild@0.28.2` (`postinstall: node
install.js`, compilación), `lmdb@3.5.6` (optional Angular build cache) y
`msgpackr-extract@3.0.7` (optional native acceleration bajo lmdb/msgpackr). No son parte
del runtime de clientes; build, Vitest, Playwright e integración real funcionaron con
la política de scripts actual. No se aprobó ninguno. Se revaluarán en TASK045; la
revisión no equivale a aceptación definitiva.

## 5. Especificación previa

Antes de iniciar el código funcional se crearon `docs/specs/008-customer-management-frontend/{spec,plan,tasks}.md`.
El incremento conserva decisiones comerciales: único plan `standard`, seis países,
validación fiscal oficial sólo ES, valores no-ES genéricos, búsquedas Unicode del
servidor, estados históricos null y ausencia de estadísticas inexistentes.

## 6. Arquitectura y acceso a datos

- Se conserva `core/shared/features`, standalone, lazy routes, Signals, RxJS,
  Reactive Forms, HttpClient y Material; sin store global ni nueva dependencia.
- `CustomersApiService` y `SimulationHistoryApiService` separan acceso por feature;
  el estado pertenece a las páginas y no se concentra en el servicio.
- `ApiClient` compone query con `HttpParams` y usa la raíz `/api`; métodos tipados
  list/create/detail/history. No logging de email, tax_id ni cuerpo de POST.
- Listado y búsqueda server-side; debounce 300ms, trim, distinct, `switchMap` cancela
  lecturas previas, errores atrapados dentro del stream, page request actual controla
  `loading`; offset vuelve a cero en filtro/tamaño y una corrección de offset fuera de
  rango no buclea.
- Submit Reactive Form impide doble llamada, sólo muestra éxito tras 201, navega a
  ficha y nunca reintenta automáticamente. 409/422/transporte conservan campos; una
  respuesta de transporte ambigua aconseja verificar el listado.
- Detail e history tienen cargas y errores independientes; no mostrar un 404 como
  ficha vacía.

## 7. Dashboard

El título del shell es “Panel comercial”. Dashboard hace una consulta acotada
`GET /customers?limit=6&offset=0`; el total procede exclusivamente de `response.total`.
Muestra capacidades de seis países y EUR/USD/GBP derivadas de contratos. La selección
respeta el orden backend y aclara que no representa últimas altas. Acciones Nuevo
cliente, Buscar clientes y Nueva simulación. La última conduce a seleccionar cliente
y explica que el simulador llega en TASK043.

No hay facturación/MRR, clientes activos, crecimiento, simulaciones globales ni
descarga masiva. Cuando falla la lectura el total se marca no disponible y la lista
presenta un único estado de error recuperable.

## 8. Listado, búsqueda y paginación

Listado muestra razón social, tax_id, país, email, plan y enlace a ficha. Se adapta a
cards con grid responsive; no incorpora edición, borrado, orden arbitrario, selección
masiva ni exportación. Search conserva acentos/puntuación, usa búsqueda remota y
discrimina empty global vs sin coincidencias. Paginación remota tamaños 10/20/50,
total distinto de count de items, botones anterior/siguiente accesibles y offset
reparado si el total cae durante la navegación.

## 9. Alta de cliente

Reactive Forms tipado para legal_name, tax_id, email, country, plan; los seis países y
único `standard` explícito. Nombre trim 1–255 como backend; tax_id se envía sin
normalización frontend; email valida sintaxis básica tras trim y se envía trim. Ayuda
explica que el servidor valida ID español con algoritmo y que países restantes usan
validación genérica, no fiscal oficial. No se duplicó algoritmo fiscal.

HTTP 409 conflict, 422 errores `ProblemDetails.errors` asociados sólo a campos
conocidos, 500 y status 0 con mensaje español seguro. Detail/password/SQL no se
exponen; 422 extensión desconocida se ignora. Se conservan datos. Confirmación se
muestra en ficha de cliente tras el éxito.

## 10. Ficha e historial

La ficha usa GET por UUID, presenta legal name, tax_id, email, país, plan, fecha UTC
localizada, vuelta a lista y acción de simulación contextual. UUID malformado no
dispara request; 404 es estado independiente.

El historial usa GET paginado (10/offset, respeta máximo 100) y se recupera
independientemente de detalle. Tarjeta principal muestra fecha, mensualidad, consumos,
subtotal EUR, total EUR y total convertido, con detalle expandible de tasas/fuente/
fechas fiscales y FX. Se prueban tres generaciones sintéticas: datos legacy null;
consumos cero sin snapshot; snapshot completo. `0` se presenta como cero, `null` como
No registrado/no disponible, subtotal nunca se presenta como total y no se consulta
el tipo de cambio vigente ni recalcula historia.

## 11. Precisión y fechas

Importes y tipos permanecen strings hasta presentación; utility agrupa los dígitos
del string exacto con separadores `es-ES`, conserva toda la fracción, muestra códigos/
símbolos EUR/USD/GBP, usa “No registrado” para null y “No disponible” para texto
inesperado. No hay `Number`, `parseFloat`, aritmética de dinero, redondeo o truncado.
Se prueban EUR/USD/GBP, cero, null, tipo de cambio con 18 decimales y valores inválidos.

`created_at` UTC date-time se muestra en zona local del navegador. `reference_date`,
`tax_verified_on` y `tax_effective_from` son calendar dates: se validan/parsean por
componentes UTC para que no cambie el día por timezone. Fechas inválidas/null son
“No disponible”/“No registrado”. No se modifica el valor recibido.

## 12. Shell, responsive y accesibilidad

Se añadieron iconos SVG inline propios para Inicio/Clientes, indicador activo,
`Saltar al contenido principal`, botón visible de cierre del drawer, dialog aria
modal sólo abierto en móvil, CDK focus trap, Escape, restore focus, cierre al navegar
y al redimensionar a desktop, reduced-motion. No hay icon font ni dependencia nueva.

Playwright prueba 320/390/768/1280; screenshots manuales 1440×1000 y 390×844. Cards
no generan overflow horizontal; nombres/emails largos tienen overflow-wrap. Form
labels, hints, mat-errors y role alert/status. Se probó el skip link y teclado en
navegación. **No se ejecutó auditoría axe ni WCAG completa**; no se declara AA.

## 13. Validaciones ejecutadas

Versiones: Node 24.22.0, npm 11.19.1, Angular 22.2.6, TS 6.0.3, Vitest 5.1.1,
Playwright Test 1.65.1. Scripts finales:

- `npm run typecheck`: PASS.
- `npm run lint`: PASS, Angular/TS templates.
- `npm run format:check`: PASS.
- `npm ci`: no se repitió porque `package.json` y `package-lock.json` permanecen
  byte-identical a TASK041; se verificó inventario/árbol instalado y no se añadieron
  ni actualizaron dependencias.
- `npm test`: **35 passed, 11 archivos, Vitest 5.1.1; 4.74 s**.
- `npm run build`: PASS, **4.95 s**, producción; initial 394.56 kB raw, 98.88 kB transfer estimate.
- `npm run e2e` sin backend: **11 passed, 1 integración real skip explícito; 17.8 s**.
- `TASK042_REAL_API=1 npm run e2e` con backend/SQLite temporal: **12 passed** (11
  tests de interfaz/mock/navigation y un escenario integrado real; **13.7 s**).
- `.\backend\.venv\Scripts\python.exe -m pytest`: **579 passed en 54.39 s**.
- Auditoría npm complete + `--omit=dev`: 0 issues actual; audit json/referencias en §4.
- Playwright browser Chromium ya disponible local; no se añadieron artefactos binarios
  a Git.

Typecheck, lint, Prettier y npm audit pasaron; esos comandos no informan duración y
no se midieron con cronómetro. No se midió coverage, no Firefox/WebKit, no SAST/DAST
ni axe. E2E no cubre slider,
preview ni guardar simulaciones desde UI.

## 14. Integración real y capturas

FastAPI se inició con `backend/.venv`, Angular en loopback, y `DATABASE_URL` apuntó a
una DB bajo carpeta temporal dedicada. Alembic aplicó 0001→0004. E2E real registró por
UI `TASK042 Empresa de Prueba ES` con NIF sintético válido, buscó/abrió, confirmó
historial vacío, recargó persistencia y verificó 409 duplicado; registró `TASK042
Empresa Sintética PT` con tax_id genérico sintético. Una simulación se creó únicamente
con el API de backend existente (EUR, sin Frankfurter); se recargó la ficha y se
mostraron subtotal 50.00 y total 60.50 persistidos. Procesos, DB y logs temporales se
eliminaron tras cada corrida; no se tocó la base predeterminada.

Se generaron y revisaron fuera del repo capturas reales, datos sintéticos:

- `TASK042-dashboard-desktop.png`
- `TASK042-listado-desktop.png`
- `TASK042-registro-desktop.png`
- `TASK042-ficha-historial-desktop.png`
- `TASK042-listado-mobile.png`
- `TASK042-registro-mobile.png`
- `TASK042-ficha-historial-mobile.png`
- `TASK042-menu-mobile.png`
- `TASK042-error-dashboard.png`
- `TASK042-conflicto-formulario.png`
- `TASK042-listado-vacio-desktop.png` (fixture interceptado de respuesta vacía)
- `TASK042-busqueda-sin-coincidencias.png` (fixture interceptado)
- `TASK042-validacion-formulario.png` (validación cliente antes del POST)

Las ubicaciones exactas están en la comunicación final de esta tarea; no se versionan
ni se guardan rutas de máquina en este registro.

## 15. Archivos y protección

Inventario final relativo a `main`: **81 candidatos publicables** (9 rutas
versionadas modificadas y 72 sin seguimiento), además del DOCX original excluido.
De los 59 candidatos iniciales, 21 cambiaron de contenido durante TASK042 y 38
permanecen idénticos. Los 7 docs vigentes editados son README raíz/backend,
ai-workspace README/contexto, roadmap, requisitos y matriz; `.gitignore` y ADR 0001
siguen en el diff acumulado de TASK041 pero TASK042 los dejó byte-identicales al inicio.
14 archivos frontend inicialmente sin seguimiento se actualizaron y 36 del scaffold
TASK041 quedaron idénticos. Se añadieron 22 rutas nuevas: SPEC-008 (3), informe,
manifiesto y 17 servicios/componentes/utilidades/páginas/tests/E2E Angular. No se
modificó ningún informe histórico TASK001–TASK041.

Archivos del scaffold TASK041 cuyo contenido se amplió: `frontend/README.md`,
`frontend/e2e/navigation.spec.ts`, `frontend/src/app/app.routes(.spec).ts`,
`frontend/src/app/core/http/api-client(.spec).ts`,
`frontend/src/app/core/layout/app-shell.{html,scss,ts}`,
`frontend/src/app/features/customers/{customer-create-page,customer-detail-page,customers-page}.ts`,
`frontend/src/app/features/dashboard/dashboard-page.ts` y
`frontend/src/app/features/simulations/simulation-page.ts`.

Integridad final verificada contra [manifiesto inicial](TASK042-initial-hashes.json):
14 rutas protegidas y los 39 ficheros históricos TASK001–TASK041 sin cambios,
incluyendo TASK035–TASK041, `LICENSE`,
`backend/requirements.lock` y migraciones 0001–0004. `package.json`/lock conservan sus
hashes iniciales; 10 runtime + 13 development direct dependencies, sin añadidos. El
DOCX conserva SHA-256 anotado. Ningún cambio en `backend/src`, tests, migraciones o
dependencias Python.

`git diff --check`, referencias Markdown relativas y escaneo dirigido de secretos,
rutas privadas y artefactos generados pasan; manifests/build/cache/results quedan
fuera o ignorados. Revisiones de seguridad son dirigidas, no SAST/DAST.

## 16. Criterios, límites y cierre

Completados localmente: dashboard real sin métricas inventadas; acciones rápidas;
listado/búsqueda remota/debounce/cancelación/paginación; alta Reactive Forms y seis
países; validación/409/422/conservación de campos; ficha/historial independiente;
compatibilidad histórica/cadenas monetarias/fechas; responsive/keyboard/shell; 35
unitarias, 12 E2E en corrida integrada, backend 579, build y lint; SPEC-008 y
documentación; flujo real, hashes e índice limpio.

Pendiente: simulador/preview/guardado desde UI (TASK043), auditoría WCAG formal,
axe/SAST/DAST, CI, despliegue/P-05, reevaluación de dependencias/scripts en TASK045.
El frontend se implementó **localmente y no se publicó**.

TASK043 no se inició. Se debe esperar revisión del propietario y autorización expresa.
