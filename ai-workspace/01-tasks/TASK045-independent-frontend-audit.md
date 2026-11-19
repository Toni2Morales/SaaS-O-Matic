# TASK045 — Auditoría técnica independiente del frontend

| Campo               | Resultado                                                                                                      |
| ------------------- | -------------------------------------------------------------------------------------------------------------- |
| Fecha               | 2026-11-19                                                                                                     |
| Rama / HEAD inicial | `feature/mvp-frontend`, `8cd664262ed908e101b19a7de715560e344105ca`                                             |
| Plan                | [Plan de auditoría](TASK045-frontend-audit-plan.md)                                                            |
| Integridad          | [Manifiesto SHA-256](TASK045-initial-hashes.json), 263 archivos tracked                                        |
| Veredicto           | **APTA CON OBSERVACIONES** para revisión/publicación de código; no lista para exposición pública de producción |

## A. Resumen ejecutivo

Auditoría de solo lectura del frontend y su integración, contrastando el resumen original
autorizado con requisitos/SPEC, código, contratos, suites oficiales, una base temporal
migrada, oráculos independientes, seguridad, accesibilidad y dependencias. No se modificó
código, pruebas, dependencias ni configuración del producto.

Resultados TASK045: Pytest 579/579; Vitest 37/37; Playwright general 20 PASS y 3 skips
opt-in; typecheck, ESLint, Prettier, Ruff, Ruff format, mypy, pip check y build pasan.
En copia temporal limpia `npm ci --ignore-scripts` instaló 402 paquetes; typecheck, build,
Vitest 37/37 y Playwright 20/20 (3 skips) pasan en esa copia. `npm audit` y
`npm audit --omit=dev` no reportan advisories. Build inicial 395.14 kB raw y 99.11 kB
estimated transfer.

Dos observaciones reproducibles de severidad MEDIA: contraste de ciertos textos muted
4,43:1 en el fondo gris; estado accesible «Preparando estimación…» simultáneo con el
error terminal FX 503. No se confirmó defecto económico general en los valores probados.
FastAPI sigue siendo la autoridad económica. Firefox/WebKit y axe/coverage no estaban
instalados; no se descargaron. No se declara WCAG AA.

La auditoría se hizo por el mismo agente que participó en tareas previas: independencia
metodológica, no de identidad ni revisión humana externa.

Runtime observado: Python 3.13.17, FastAPI 0.163.1, Pydantic 2.14.3, SQLAlchemy 2.1.8,
Alembic 1.20.1, Pytest 9.2.0; Node 24.22.0, npm 11.19.1, Angular/CLI 22.2.6,
TypeScript 6.0.3, RxJS 7.8.2, Vitest 5.1.1, Playwright 1.65.1, ESLint 10.15.0,
Prettier 3.8.1.

## B. Inventario de hallazgos

| ID     | Severidad / estado                    | Impacto y bloqueo                                                                                                                                                                      |
| ------ | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A45-01 | MEDIA — confirmado                    | Contraste de texto normal secundario en superficies `#f5f7fa`; corregir/revisar antes de afirmar accesibilidad básica completa. No bloquea publicar la rama.                           |
| A45-02 | MEDIA — confirmado                    | El anuncio polite de preview queda en «Preparando…» al concluir con error FX; el alert informa indisponibilidad. No bloquea publicar rama; recomendado antes de entregar UX accesible. |
| A45-03 | INFORMATIVA — condición conocida P-05 | El build de producción no incluye proxy `/api`; necesita reverse proxy/hosting configurado. Bloquea servicio desplegado sin ese componente, no repositorio público.                    |
| A45-04 | INFORMATIVA — limitación de alcance   | Sin auth/autorización; API y datos de empresa/contacto accesibles a quien llegue al backend. Bloquea exponer con datos reales, no aplicación local/repo público.                       |

### A45-01 — Contraste de texto muted

- **Referencia:** `frontend/src/styles.scss:36-45` define `--color-background:#f5f7fa`
  y `--color-text-muted:#64748b`; usos en ayudas y etiquetas pequeñas, por ejemplo
  `frontend/src/app/features/simulations/simulation-page.ts:344-348,384-388`.
- **Reproducción:** fórmula WCAG de luminancia sRGB. `#64748b` sobre `#f5f7fa` =
  **4,43:1**; sobre blanco = 4,76:1. Pares comprobados: primario/blanco 6,29:1;
  texto nav/nav 14,39:1; caption nav 11,95:1; error/fondo error 9,16:1.
- **Resultado:** algunos textos normales aplicados al fondo global quedan bajo 4,5:1;
  los mismos tokens sobre superficie blanca pasan. No todos los componentes fallan.
- **Causa probable:** token pensado/contrastado sobre blanco y reutilizado en fondo gris.
- **Propuesta:** revisar combinaciones efectivamente compuestas y ajustar token/superficie
  con margen; revalidar estados y foco. 1–2 h, riesgo visual bajo-medio.
- **Regresión:** contraste de tokens automatizable y revisión manual de estados/colores.
- **Bloqueante:** no para publicar código; sí para afirmar contraste básico completo.

### A45-02 — Estado anunciado durante error FX

- **Referencia:** `SimulationPageComponent.statusMessage()` en
  `frontend/src/app/features/simulations/simulation-page.ts:728-735`; el error terminal
  se establece en líneas 672-680 y se muestra en plantilla 275-282.
- **Reproducción:** Chromium, cliente sintético y preview interceptada con 503
  `application/problem+json`. `.status` dijo «Preparando estimación…» mientras el alert
  dijo «No se pudo obtener un tipo de cambio…». Evidencia externa
  `screenshots/fx-error-status-conflict.png`.
- **Resultado:** `preparing`/`calculating` ya son falsos y guardar queda deshabilitado,
  pero el anuncio polite no representa el error concluido.
- **Causa probable:** `statusMessage()` no prioriza `errorMessage()`/`fxUnavailable()`.
- **Propuesta:** estado único/terminal para error conservando alert, retry y selección EUR;
  cubrir 503 inicial y posterior a preview. 1–2 h, riesgo bajo.
- **Bloqueante:** no para publicar rama; recomendado antes de entregar UX refinada.

### A45-03/04 — Condiciones operativas

`API_BASE_URL` usa `/api` por defecto (`frontend/src/app/core/config/api.config.ts:3-6`);
el proxy existe solo para `serve` development (`frontend/angular.json:58-69`). README ya
documenta que no se incluye en production y P-05 sigue pendiente. Es precondición de
deployment, no defecto oculto. La exclusión aprobada de autenticación implica que no se
deben exponer datos reales sin una decisión posterior de control de acceso; no se prescribe
una arquitectura no aprobada.

## C. Cumplimiento y trazabilidad del reto

Estados independientes al corte: «cumplido» describe el nivel probado, no aplicación
desplegada. La tabla original conserva deltas históricos; se usaron FR y deltas TASK044.

| Requisito del resumen original        | Requisito / SPEC               | Implementación / prueba                                                   | Resultado                                                                                        |
| ------------------------------------- | ------------------------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| API REST y SQLite                     | CON-01/08; SPEC-001–006        | FastAPI/SQLAlchemy/Alembic, API real y migración temporal 0001–0004       | Cumplido con observaciones: despliegue no probado                                                |
| Alta de clientes y datos fiscales     | FR-01/02; SPEC-001/004/008     | Formulario Angular + API; alta ES/PT, inválido 422 y duplicado 409 reales | Cumplido                                                                                         |
| Simulación y persistencia             | FR-03/04; SPEC-003/004/009     | UI envía parámetros; API preview/POST, SQLite e historial                 | Cumplido con observaciones: escalar navegador/API no se cubre íntegro en cada moneda             |
| Tramos acumulativos / 15 = 140 EUR    | FR-05; SPEC-002/005/009        | Backend único cálculo, Angular bandas informativas                        | Cumplido; 13 cotas oracle independientes coinciden                                               |
| Impuesto por país                     | FR-06; SPEC-005                | Catálogo backend seis países, snapshot                                    | Cumplido con observaciones: IVA general simplificado, no asesoría fiscal                         |
| API pública FX y selector dinámico    | FR-10; CH-12/13; SPEC-005/009  | UI → FastAPI → Frankfurter; caché 24h, metadatos y snapshot               | Cumplido con observaciones por ambigüedad «conectar interfaz»; no consulta directa del navegador |
| Dashboard, búsqueda por nombre/tax ID | FR-07; SPEC-008                | Dashboard y búsqueda server-side con debounce/cancelación                 | Cumplido                                                                                         |
| Ficha responsive e historial          | FR-08; SPEC-006/008            | Detalle e historial paginado/snapshot                                     | Cumplido con observaciones: solo Chromium instalado                                              |
| Slider/proyección interactiva         | FR-09/12; SPEC-009/010         | Slider 0–1000, manual 0–1M; preview servidor                              | Cumplido con observaciones de accesibilidad/error                                                |
| Entregables IA/planificación          | CON-12, CH-17–21; SPEC-001–010 | ai-workspace, ADR, specs, planes, informes y trazas                       | Cumplido con observaciones: no fabricar chats retrospectivos                                     |
| README y arranque                     | CON-13/CH-24; NFR-09           | READMEs explican backend, Angular, migración y proxy                      | Parcialmente cumplido: npm install condicionado y hosting no resuelto                            |

### Significado de FX y «tiempo real»

«Tiempo real» se cumple en sentido de **interacción de UI**: cambios válidos activan
preview con debounce 250 ms y actualizan al responder API. No es cotización bursátil
continua: Frankfurter entrega referencias publicadas/fechadas; backend cachea por proceso
24 h desde obtención exitosa, timeout 5 s y no sirve expiradas. Puede mostrar referencia
anterior dentro del TTL (p.ej. festivo/fin de semana). Tasa, fecha, obtención y fuente se
exponen; cambio en una petición nueva puede cambiar el total guardado.

El intermediario backend mantiene autoridad única y redondeo, evita duplicar cálculo,
permite probar proveedor y persiste snapshot sin llamar a Frankfurter desde Angular.
El requisito podría interpretarse como fetch directo frontend. Explicación recomendada
sin ampliar alcance: «Angular solicita la estimación a FastAPI; FastAPI obtiene la tasa
pública de referencia, fechada y cacheada; UI actualiza al responder, no ofrece ticks de
mercado». No describir como FX en vivo continuo.

## D. Arquitectura Angular

- `core` (HTTP, config, shell), `shared` (modelos, formato, componentes), `features`
  (dashboard, customers, simulations, not-found): mantenible/proporcionado a MVP.
- Standalone, rutas lazy `loadComponent`, formularios reactivos, Signals locales, RxJS
  para IO/operadores. Sin store global innecesario.
- `ApiClient` tipado; wrappers de acceso por feature son delgados; DTOs strings/nulls
  reflejan OpenAPI. Sin generador OpenAPI: sincronización manual documentada.
- `switchMap`, debounce 250/300 ms, generación de preview y `takeUntilDestroyed` protegen
  carreras y vida de componentes. Shell Router subscription vive mientras shell raíz vive;
  no se observó acumulación por ruta.
- `SimulationPageComponent` concentra carga cliente, form, preview, save, mensajes y
  estilos (aprox. 823 líneas con template/style): grande, pero feature coherente; extraer
  solo cuando reduzca complejidad concreta, no preferencia arquitectónica.
- Estrictamente tipado y strict templates; `any` no encontrado en código de producto;
  grep sin `innerHTML`, `bypassSecurityTrust`, `DomSanitizer`; assertions puntuales
  dependen de guards o narrowing. No se ejecutó detector formal de ciclos; inspección no
  halló ciclo obvio.
- Dependencias de importación cliente→shared/core; no existe dependencia circular
  identificada por inspección, pero no hay grafo automatizado.
- Errores se normalizan a mensajes seguros y errores de campo solo se mapean para campos
  reconocidos. Interpolación Angular de nombre/email es texto escapado.
- Conclusión: no recomendar NgRx, nueva capa API ni generator por preferencia. Mejoras de
  mantenibilidad son opcionales mientras no haya evidencia de cambios frecuentes.

## E. Integridad económica

Oráculo independiente en céntimos enteros ejecutado contra preview FastAPI real: **13/13**.

|  Usuarios | EUR esperado/observado |
| --------: | ---------------------: |
|         0 |                   0.00 |
|         1 |                  10.00 |
|         9 |                  90.00 |
|        10 |                 100.00 |
|        11 |                 108.00 |
|        15 |                 140.00 |
|        16 |                 148.00 |
|        49 |                 412.00 |
|        50 |                 420.00 |
|        51 |                 425.00 |
|       100 |                 670.00 |
|      1000 |                5170.00 |
| 1.000.000 |           5.000.170.00 |

Para 15: ES subtotal 140,00, 21 % = 29,40, total 169,40. Para 16: 148,00, impuesto
31,08, total 179,08. Catálogo real de auditoría contrastado en preview temporal para
140 EUR: ES 21 %, PT 23 %, FR 20 %, DE 19 %, IT 22 %, NL 21 %; todos los importes de
impuesto/total coinciden.

Frankfurter real por API: USD tasa `1.0997`, referencia 2026-11-19, convertido 186.29;
GBP `0.83348`, 2026-11-19, convertido 141.19. Son consultas puntuales. Fixtures
deterministas de aceptación 1.0998 USD/0.83348 GBP y 15/16 coinciden con importes de
spec/tests; no confundir fixtures con las cotizaciones observadas.

Angular solo muestra strings decimales y formatea; no produce importes alternativos. El
total se convierte incluyendo IVA y el backend redondea HALF_UP. POST 201 prevalece sobre
preview; la tasa no se bloquea. En DB temporal real se guardaron simulaciones 201 en
EUR/USD/GBP y se recuperaron del historial con snapshot: EUR 169.40, tasa 1/identity,
fecha referencia null; USD 186.29 a 1.0997 y GBP 141.19 a 0.83348, ambas referencia
2026-11-19, source frankfurter. El preview previo seguía sin fila persistida.

## F. Concurrencia, formularios e integración

### Análisis adverso y pruebas existentes

- Preview antigua se libera tarde tras terminar nueva: E2E confirma no sobrescritura.
  Formulario inválido cancela pendiente, quita bandas, no envía preview y bloquea save.
- Save congela campos, bloquea doble click/request y espera respuesta; 201 diferente
  reemplaza estimate. Error ambiguo no retry, conserva inputs y deriva a historial.
- **No hay exactly-once:** API carece de idempotency key; si POST se confirma en SQLite
  pero respuesta se pierde, retry manual puede duplicar. UI lo advierte. Limitación MVP,
  no afirmación de garantía transaccional cliente-servidor.
- Búsqueda usa debounce 300 ms, trim, reset offset, `switchMap`; test unitario libera
  búsqueda antigua y verifica no reemplazo. Cancelación cliente no garantiza parar
  trabajo del servidor.
- Forms: required/trim/legal name 255, email sintaxis, tax ID pasa backend; enteros,
  negativos, rango, máximo, manual > slider, uno sobre contrato. CASO 1000001: tests
  existentes bloquean preview/guardar y quitan bandas; el código asocia el error mediante
  `aria-describedby`, pero no hubo verificación independiente con tecnología asistiva.

### Integración real de TASK045

DB `audit.sqlite3` fuera del repo migrada 0001–0004; backend propio `127.0.0.1:8006`,
Angular `127.0.0.1:4201`, proxy temporal fuera del repo. Puerto 8000 de propietario no se
tocó. Se usaron exclusivamente nombres, identificadores y emails sintéticos.

Observado: alta ES válida 201, inválida 422, duplicado 409; alta PT y FR/DE/IT/NL;
búsqueda HTTP por nombre/tax ID, cliente desconocido 404; 13 pricing, tasas de seis
países, preview EUR sin filas y FX USD/GBP HTTP 200. En DB real se guardaron POST 201
EUR/USD/GBP y el historial devolvió los snapshots. En otra SQLite TASK045 se detuvo y
reinició el backend propio; GET recuperó la simulación 169.40 EUR. La DB de reinicio se
eliminó. El servidor Angular real 4201 y Chromium se iniciaron; se verificó el error FX
en navegador con 503 interceptado. El recorrido automatizado amplio de UI real no produjo
resultado final observable antes de limpiar servicios y no se cuenta como PASS. La suite
Playwright general omite integración; TASK044P histórica no se cuenta como TASK045.

No ejecutar consultas masivas FX ni usar DB del propietario. Los casos interceptados en
browser son fixtures, no prueba de persistencia real.

## G. V44-01–07

| ID                          | Estado de auditoría                                                     | Evidencia/interpretación                                                                                                                                        |
| --------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| V44-01 menú parcial         | No verificable estable al redactar; captura previa puede ser transición | drawer usa CSS 160 ms y screenshot de TASK044 captura inmediatamente al abrir. Resultado post-transition externo pendiente de registrar.                        |
| V44-02 labels/selectores    | No reproducido en screenshot disponible, limitado                       | formulario móvil sintético con selector cerrado; se ve ayuda ajustada al siguiente control, sin overlay inequívoco. Selector abierto/transición no exhaustivos. |
| V44-03 espaciado ayuda      | Mejora opcional, no defecto reproducido                                 | texto multilínea visible; separación apretada pero sin solape confirmado. No zoom/AT.                                                                           |
| V44-04 error FX/preparación | **Confirmada**, A45-02                                                  | 503 terminal; status polite sigue «Preparando estimación…», alert da error. Captura externa. No se habilita save.                                               |
| V44-05 icono/texto          | No reproducido como defecto                                             | Flex gap `--space-3` y SVG alineado; si se observa desacuerdo es acabado menor.                                                                                 |
| V44-06 CTA duplicado        | Mejora opcional                                                         | dos enlaces Nueva simulación en ficha e historial, con ubicaciones distintas; redundancia no es defecto funcional por sí sola.                                  |
| V44-07 1.000.001            | Implementación parece coherente; asociación accesible a cerrar          | max error y guard/save sin preview cubiertos por E2E; valor anterior se marca stale. Comprobación propia aria-describedby/blur pendiente de resultado.          |

Capturas de formulario son sintéticas/interceptadas; no son datos de clientes ni prueba
de API. Se evita declarar defecto visual por captura durante transición.

## H. Responsive, accesibilidad y compatibilidad

- Suites Chromium cubren shell 320/390/768/1440 y simulador 320; prueba propia prevista
  a 320/390/768/1024/1440 para dashboard/listado/alta/detalle/simulador. Solo Chromium
  está instalado; Firefox y WebKit no existen en cache Playwright, no descargados.
- Shell: nav/main landmarks, skip link, `aria-current`, nombres accesibles, labels,
  `aria-describedby`, live regions, error alerts, focus trap CDK, Escape, return focus y
  `prefers-reduced-motion`. E2E teclado/menu/slider pasa.
- No se instaló axe; axe y coverage provider no están disponibles. Sin lector de pantalla,
  auditoría total de tab order, zoom OS/200-400 % ni high contrast. No afirmar WCAG AA.
- Conteo de contraste limitado en A45-01 no es auditoría completa; focos no se recomiendan
  eliminar por estética.

## I. Seguridad, supply chain y npm

### Seguridad

No se halló `innerHTML`/bypass sanitizer, secretos, tokens, cookies ni browser storage en
código de app. Angular interpola contenido de cliente como texto; API paths se construyen
con base fija y UUID codificado. Se muestran identificadores/emails de cliente por
requisito. No SAST/DAST ni escaneo ofensivo. Proxy de desarrollo loopback; build de
producción requiere reverse proxy; sin auth/CORS global/rate limits está documentado.

### Dependencias y scripts

`npm ls`/lock confirma presencia transitiva dev:

| Paquete                  | Cadena / script exacto                                                                  | Lectura no ejecutada / recomendación                                                                                                                                                                                                                  |
| ------------------------ | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `@parcel/watcher@2.6.0`  | `@angular/build → sass → @parcel/watcher`; `install: node scripts/build-from-source.js` | Script inicia `node-gyp rebuild` solo si `npm_config_build_from_source === 'true'`; no red directa, proceso/build de addon nativo. Mantener bloqueado por defecto; permitir sólo en build controlado si se necesita.                                  |
| `esbuild@0.28.2`         | `@angular/build`/Vite/Vitest; `postinstall: node install.js`                            | Verifica binario, puede fallback a `npm install` del binario de plataforma por HTTPS, escribir/renombrar archivos y ejecutar `--version`. Es necesario al flujo build normal, pero scripts no se habilitan sin allowlist explícita/entorno confiable. |
| `lmdb@3.5.6`             | `@angular/build`, dev optional; `install: node-gyp-build-optional-packages`             | Selección/carga o build opcional nativo. El build observado funciona sin scripts; conservar bloqueado salvo necesidad/aprobación.                                                                                                                     |
| `msgpackr-extract@3.0.7` | `lmdb → msgpackr → msgpackr-extract`, dev optional; mismo instalador nativo             | Extensión opcional de extracción; conservar bloqueado salvo necesidad/aprobación.                                                                                                                                                                     |

No se autorizó ni ejecutó ninguno. Revisar localmente scripts no garantiza origen de
binarios ni seguridad completa. `npm audit` ambos modos 0 avisos al 2026-11-19; no es
SAST ni garantía de riesgo cero.

### Instalación

Copia externa con manifiestos y fuentes: `npm ci --ignore-scripts --no-audit --no-fund`
agregó 402 paquetes; npm ls root limpio; typecheck, build (395.14 kB), Vitest 37/37 y
Playwright 20 PASS/3 skips pasan. Instalación estándar no probada ni autorizada. Esta
variante reproduce las validaciones del checkout sin activar scripts. READMEs deben
presentar explícitamente esa modalidad segura mientras scripts sigan pendientes.

## J. Pruebas, cobertura y calidad

| Check TASK045                          | Resultado                                                      |
| -------------------------------------- | -------------------------------------------------------------- |
| Frontend typecheck / ESLint / Prettier | PASS / PASS / PASS                                             |
| Vitest                                 | 37/37, 11 files PASS                                           |
| Playwright general                     | 20 PASS; 3 skips opt-in                                        |
| Playwright fixture visual              | 1 PASS; screenshots externos, APIs deterministas               |
| Integración real TASK045               | PASS; DB/migraciones y guardados EUR/USD/GBP; reinicio aislado |
| Pytest (solo `backend/.venv`)          | 579 PASS                                                       |
| Ruff check / format                    | PASS / PASS (90 files)                                         |
| mypy                                   | PASS (88 fuentes)                                              |
| pip check                              | PASS, sin requisitos rotos                                     |
| Build producción                       | PASS, 395.14 kB initial raw                                    |
| npm audit / omit dev                   | 0 vulnerabilidades notificadas en cada uno                     |
| Cobertura Vitest / axe                 | Provider ausente; no medida/no instalada                       |

Tests tienen aserciones de request, datos y estados; fixtures explícitas y reales
separadas. Concurrencia y errores FX se prueban con latencias/intercepts. Selectores
predominan role/label, aunque CSS class se usa en algunos asserts. Sin pruebas de Firefox/
WebKit. Recomendaciones permanentes: anuncio de 503, contrast tokens, V44-07 aria/blur,
latencias invertidas búsqueda/preview, persistencia FX EUR/USD/GBP sin proveedor en test,
POST ambiguo sin falsa idempotencia.

## K. Rendimiento y mantenibilidad

Build inicial: 395.14 kB raw (JS 385.07, CSS 10.07), `estimated transfer` 99.11 kB; no
medición real de gzip/Brotli/producción. Presupuesto 500 kB warning / 1 MB error. Rutas
lazy; chunk compartido framework mostrado 214.10 kB raw fuera del initial. Debounce
250/300 ms, paginación y cancelación implementados. No se midieron Lighthouse, tiempos de
carga, SLA, tráfico real ni volumetría. Búsqueda UDF lineal es A39-11 aceptada para MVP.

## L. Deuda TASK039

| ID     | Estado histórico TASK039B                                               | Evaluación de impacto                                               |
| ------ | ----------------------------------------------------------------------- | ------------------------------------------------------------------- |
| A39-05 | riesgo aceptado: histórico corrupto da 500 controlado, no oculta/repara | deuda aceptable documentada                                         |
| A39-07 | pendiente: error inesperado no se registra                              | recomendar logging antes operación sostenida; requiere autorización |
| A39-08 | pendiente: CustomerRepository amplio para lectura de país               | deuda arquitectura baja; no bloqueante                              |
| A39-09 | aceptado por Q-26: extras cliente ignore vs simulación forbid           | riesgo aceptado documentado                                         |
| A39-10 | aceptado: análisis arquitectura estático no cubre import dinámico       | riesgo residual bajo                                                |
| A39-11 | diferido: LIKE/UDF escanea linealmente                                  | aceptable para volumen MVP; medir al crecer                         |
| A39-12 | diferido: no auth/CORS/global limits                                    | bloqueante para desplegar con datos reales                          |
| A39-13 | riesgo aceptado: DDL SQLite no transaccional                            | backup/prueba previa en migración real                              |
| A39-14 | riesgo aceptado: lock FX global serializa pares                         | tolerable MVP; reexaminar con latencia/concurrencia observada       |
| A39-15 | riesgo aceptado: cache FX por proceso                                   | no compartida/reinicia vacía; tolerable monoproceso                 |

No se cambió backend. A39-07/08 requieren autorización; A39-12 debe resolverse antes de
exposición con datos reales.

## M. Evaluación orientativa de la rúbrica original

No constituye calificación oficial.

| Categoría / ponderación       | Orientación | Justificación                                                                                                                            |
| ----------------------------- | ----------: | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Planificación y diseño / 35 % |       29/35 | Diez SPEC, ADR, reglas y trazabilidad con secuencia; explicación histórica de deltas y semántica FX se puede simplificar para evaluador. |
| Criterio técnico y QA / 25 %  |       20/25 | Suites, auditorías, hashes y revisión de concurrencia; resta no CI/cobertura/multibrowser y A45-01/02.                                   |
| Calidad software / 30 %       |       24/30 | End-to-end local, precisión, persistencia, responsive; limitaciones accesibilidad/FX, no deployment ni auth (fuera MVP).                 |
| README/despliegue / 10 %      |        7/10 | Arranque local claro, migración/proxy documentados; instalación normal condicionada y P-05/deploy abierto.                               |
| **Total orientativo**         |  **80/100** | Supuesto auditor; no evaluar oficial.                                                                                                    |

Entregables relevantes presentes: repo público, código, `ai-workspace`, specs, ADR, diseño
DB y READMEs de arranque. CI/deploy no entregados. Las evidencias de IA son registros
históricos reales; no crear chats/prompt retroactivos. Para TASK047 seleccionar screenshots
con timestamp/viewport/browser, fixture o integración real claramente indicada: alta,
inválido/duplicado, preview sin escritura, guardado/reload, 15/16, FX con tasa/fecha,
teclado/skip/menú estable y responsive. No incluir DOCX ni clientes reales.

## N. Propuesta TASK045B (no iniciada)

| Prioridad                                    | Acción propuesta                                                                                  | Esfuerzo / riesgo                                |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Imprescindible para afirmar contraste básico | Ajustar A45-01 por superficie y verificar pares de texto/estado                                   | 1–2 h; riesgo visual bajo-medio                  |
| Recomendada                                  | Resolver A45-02 y añadir test status/alert/error recovery                                         | 1–2 h; riesgo bajo                               |
| Recomendada antes de entrega UX              | Cerrar V44-07 con asociación aria/blur/teclado y nota stale                                       | 1–3 h; bajo                                      |
| Antes de producción                          | Aprobar P-05/reverse proxy y auth/access control con decisión del propietario                     | esfuerzo arquitectónico no estimado; riesgo alto |
| Opcional                                     | Inspección stable menu/form transitions; extraer lógica del simulador solo si reduce acoplamiento | 2–6 h; regresión media                           |
| Aceptable/deuda                              | A39-05/09/10/11/13/14/15 según §L                                                                 | se conserva documentada                          |
| Fuera de alcance actual                      | Auth/backend logging, idempotency, cambios API/FX/deps/scripts                                    | requiere TASK/autorización nueva                 |

No se ha corregido nada ni iniciado TASK045B, TASK046 o TASK047.

## O. Criterios de aceptación CA01–CA45

|  CA | Estado                     | Evidencia                                                                            |
| --: | -------------------------- | ------------------------------------------------------------------------------------ |
|  01 | CUMPLIDO                   | Git inicial coincide.                                                                |
|  02 | CUMPLIDO CON OBSERVACIONES | Plan previo a pruebas técnicas; parte del preflight ocurrió antes de materializarlo. |
|  03 | CUMPLIDO                   | 263 hashes generados; DOCX no leído.                                                 |
|  04 | CUMPLIDO                   | Requisitos del resumen owner contrastados.                                           |
|  05 | CUMPLIDO CON OBSERVACIONES | Matriz evaluada con deltas/historia.                                                 |
|  06 | CUMPLIDO                   | Arquitectura Angular inspeccionada.                                                  |
|  07 | CUMPLIDO                   | Responsabilidades y tamaño mantenibilidad evaluados.                                 |
|  08 | CUMPLIDO                   | Angular solo envía parámetros; importes response backend.                            |
|  09 | CUMPLIDO                   | 13 cotas reales/oracle coinciden.                                                    |
|  10 | CUMPLIDO                   | Seis países y tasas contrastados.                                                    |
|  11 | CUMPLIDO CON OBSERVACIONES | Conversión/format y FX reales; guardado real por FX separados limitado.              |
|  12 | CUMPLIDO CON OBSERVACIONES | Proveedor público real por backend; fechada/cacheada, no continuous.                 |
|  13 | CUMPLIDO                   | Cancelación de preview revisada/test existente.                                      |
|  14 | CUMPLIDO                   | Respuesta antigua no pisa actual.                                                    |
|  15 | CUMPLIDO CON OBSERVACIONES | Doble click bloqueado; ambiguo no reintenta.                                         |
|  16 | CUMPLIDO CON OBSERVACIONES | Idempotencia backend ausente documentada; riesgo evaluado.                           |
|  17 | CUMPLIDO                   | Search switchMap, test de carrera y HTTP búsqueda real.                              |
|  18 | CUMPLIDO CON OBSERVACIONES | API/SQLite reales, Chromium iniciado; flujo UI completo no confirmado como PASS.     |
|  19 | CUMPLIDO                   | Preview EUR no persiste.                                                             |
|  20 | CUMPLIDO CON OBSERVACIONES | Tres snapshots e historial; EUR recuperado tras reinicio; API sin rutas mutadoras.   |
|  21 | CUMPLIDO                   | POST real 201 y snapshots EUR/USD/GBP; FX externo puntual disponible.                |
|  22 | CUMPLIDO CON OBSERVACIONES | Validación examinada; exponente no browser case individual.                          |
|  23 | CUMPLIDO CON OBSERVACIONES | Suite menú y transición inspeccionada; captura TASK044 se toma durante transición.   |
|  24 | CUMPLIDO CON OBSERVACIONES | Form móvil, sin overlap inequívoco; no todas transiciones.                           |
|  25 | CUMPLIDO CON OBSERVACIONES | Textos wrap sin overlap confirmado; tight spacing.                                   |
|  26 | CUMPLIDO                   | A45-02 reproduce error FX/status contradictorio.                                     |
|  27 | CUMPLIDO CON OBSERVACIONES | Flex/gap revisado; acabado no confirmado defectuoso.                                 |
|  28 | CUMPLIDO CON OBSERVACIONES | Dos CTA constatados; redundancia opcional.                                           |
|  29 | CUMPLIDO CON OBSERVACIONES | Tests max/disabled/stale; asociación aria revisada, sin AT.                          |
|  30 | CUMPLIDO CON OBSERVACIONES | Pruebas responsive parciales; matriz propia de 5 rutas/anchos no confirmada.         |
|  31 | CUMPLIDO CON OBSERVACIONES | DOM/teclado/contraste parcial; no axe/AT/zoom/WCAG.                                  |
|  32 | CUMPLIDO CON OBSERVACIONES | Chromium; Firefox/WebKit no disponibles y no instalados.                             |
|  33 | CUMPLIDO CON OBSERVACIONES | Static checks clean; no SAST, auth limit recognized.                                 |
|  34 | CUMPLIDO CON OBSERVACIONES | Cuatro scripts inspeccionados, no ejecutados.                                        |
|  35 | CUMPLIDO CON OBSERVACIONES | `ci --ignore-scripts` limpio; estándar no.                                           |
|  36 | CUMPLIDO CON OBSERVACIONES | Calidad tests revisada; coverage unavailable.                                        |
|  37 | CUMPLIDO CON OBSERVACIONES | Bundle/lazy budgets; no real load metrics.                                           |
|  38 | CUMPLIDO                   | A39-05/07–15 reconciliados.                                                          |
|  39 | CUMPLIDO CON OBSERVACIONES | Rúbrica orientativa justificada.                                                     |
|  40 | CUMPLIDO                   | Suites oficial ejecutadas; limitaciones anotadas.                                    |
|  41 | CUMPLIDO                   | A45 findings clasificados con evidencias.                                            |
|  42 | CUMPLIDO                   | Comandos/capturas y recorrido real sintético registrados.                            |
|  43 | CUMPLIDO                   | Rehash 263/263 sin cambios ni faltantes.                                             |
|  44 | CUMPLIDO                   | Sin Git prohibido, cambios de producto o procesos ajenos.                            |
|  45 | CUMPLIDO CON OBSERVACIONES | Informe y próximos pasos entregados; servicios propios ya detenidos.                 |

## P. Estado Git e integridad

HEAD inicial/final verificado: `8cd664262ed908e101b19a7de715560e344105ca`; refs esperadas:
origin feature igual, `origin/main` `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`, main
local `8371f9f608ce6e06984cc501d8240e1b7edf34d5`. Índice inicial y final vacío. Hash
SHA-256 final: **263/263 coinciden, 0 modificados, 0 faltantes**. Únicos ficheros
permanentes autorizados: este informe, plan y manifiesto. DOCX sigue sin seguimiento.

Servicios TASK045 propios 8006/4201 detenidos; SQLite `audit.sqlite3`, base de reinicio,
proxy temporal y copia limpia npm retirados. Las capturas de auditoría permanecen fuera
del repo para revisión; logs/results con datos sintéticos quedan en la carpeta temporal
aprobada. Puerto 8000 y DB TASK044 bloqueada intactos; ningún proceso del propietario se
detuvo.

## Q. Veredicto

**APTA CON OBSERVACIONES.** La evidencia no mostró cálculo monetario incorrecto en la
matriz probada ni caída general del flujo local. Los hallazgos A45-01/02 son reproducibles
y deben priorizarse en TASK045B, pero no invalidan publicación controlada del código.

**No apta para declarar aplicación lista para producción pública:** no hay autorización,
auth, estrategia P-05 ni proxy de producción validados; cobertura de navegador/accesibilidad
es parcial. El reto requiere repo público; no requiere que la aplicación se exponga
públicamente. Mantener esa distinción.

## R. Evidencias externas y reproducción

Carpeta externa no versionada `%LOCALAPPDATA%\Temp\opencode\TASK045`. `fixture-screenshots`
contiene 21 PNG de `TASK044` (dashboard/clientes/registro/ficha/simulador, mobile, 15/16,
USD/GBP, invalidación/error FX, guardado/historial, menú/foco). Son capturas de Chromium
con APIs interceptadas; no demuestran persistencia. Evidencia A45-02:
`screenshots/fx-error-status-conflict.png`, con 503 interceptado. Capturas del recorrido
de API real se anotan por separado, no usar datos reales. No se publican PNGs.

Reproducción frontend desde `frontend/`:

```powershell
npm run typecheck
npm run lint
npm run format:check
npm test
npm run e2e
npm run build
npm audit
npm audit --omit=dev
```

Backend, exclusivamente `backend/.venv`:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m mypy .
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest
```

Instalación limpia estudiada: copia temporal + `npm ci --ignore-scripts`; no estándar ni
scripts enabled. Backend/Angular isolated: 8006/4201; no reutilizar como configuración
de producto.

## S. Confirmación

- No se modificó código funcional, pruebas, dependencias, lock/manifests o configuración.
- No se leyó/alteró/publicó `Prueba Devs con IA.docx`.
- Sin Git add/commit/push/pull/reset/clean/stash/rebase/merge/cherry-pick, ramas ni PR;
  `main` no se modificó.
- No se ejecutaron scripts npm de los cuatro paquetes ni se instalaron herramientas en repo.
- TASK045B, TASK046 y TASK047 no se iniciaron.
- TASK045 espera únicamente la confirmación de los recorridos temporales activos, rehash
  final y limpieza exclusiva de sus propios procesos/DB antes de emitir el cierre final.
