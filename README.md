# SaaS-O-Matic

> **Vigente TASK045B:** backend integrado en `main` (PR #6). Dashboard, clientes y
> simulador interactivo en Angular; preview/guardado usan FastAPI y el cálculo económico
> permanece exclusivamente en el backend. TASK044P/TASK045BP publican el frontend
> refinado/corregido en `feature/mvp-frontend`; no está integrado en `main`.
> Cálculo mensual con IVA general de seis
> países y conversión EUR/USD/GBP mediante Frankfurter v2. Decimal exacto, HALF_UP,
> caché en memoria 24 h, timeout5s y snapshots históricos. `display_currency` opcional
> (EUR predeterminado); 503 problem+json si no hay referencia válida. EUR funciona sin red.
> Listado/búsqueda Unicode, detalle e historial paginados y preview sin escritura disponibles.
> TASK039 auditó el backend con observaciones no bloqueantes; TASK039B corrige
> trazabilidad, README, `.env.example`, configuración SQLite compartida y límites FX.
> Estimación simplificada, no factura. Véanse
> [SPEC-005](docs/specs/005-taxes-and-currency-conversion/spec.md) y
> [SPEC-006](docs/specs/006-customer-queries-and-preview/spec.md).

Herramienta interna para que el equipo comercial simule y estime el coste mensual de suscripciones SaaS corporativas: clientes, planes, consumo estimado, tramos de usuarios, impuestos por país y conversión de divisas.

> **Estado real del MVP:** backend integrado en `main` (PR #6, merge `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`). TASK044P/TASK045BP publican el frontend refinado/corregido en `feature/mvp-frontend`; sigue sin integrarse en `main`. TASK045 identificó observaciones medias de contraste/estado FX y TASK045B las corrige y refuerza la QA. P-05, CI y despliegue continúan pendientes. **No se declara listo para producción pública.**
>
> **Estado de publicación:** PR #6 fue fusionado por el propietario; merge commit `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`.
>
> **Decisiones:** Q-18–Q-26 implementadas en alcance backend; P-01 resuelta en TASK041/ADR 0003; P-05 sigue pendiente. Documento original no seguido ni publicado.

## Stack

Resumen; el detalle está en el [ADR 0001](docs/adr/0001-technology-stack.md) y el [ADR 0002](docs/adr/0002-architecture.md).

- **Backend:** Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2, SQLite y Alembic.
- **Calidad backend:** Pytest, HTTPX, Ruff y mypy.
- **Frontend:** Angular 22.2.6, TypeScript 6.0.3, Material/CDK, standalone components, Signals, RxJS, Router y HttpClient. Incrementos TASK044P/TASK045BP publicados en `feature/mvp-frontend`; aún no integrados en `main`.
- **Contrato de API:** OpenAPI. **Divisa base:** EUR.
- **Arquitectura:** monolito modular con dependencias hacia dentro (`presentation → application → domain`, `infrastructure → domain`).

## Estado funcional

| Área                              | Estado                                                                                                                  |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Alta de clientes                  | Seis países, único plan `standard`; genérico no oficial fuera de ES.                                                    |
| Validación fiscal                 | DNI/NIF, NIE y CIF/NIF con algoritmos de control.                                                                       |
| Precios progresivos               | Cero = 0.00; tarifas de los tres tramos intactas.                                                                       |
| Simulaciones                      | Mensuales persistidas, cliente y usuarios.                                                                              |
| Almacenamiento y llamadas API     | Obligatorios nuevos; históricos NULL; sin cargos.                                                                       |
| Impuestos                         | IVA general por país, verificado; alcance simplificado, sin regímenes especiales.                                       |
| Divisas                           | Frankfurter v2, EUR/USD/GBP, caché24h y snapshot.                                                                       |
| Búsqueda, detalle e historial     | GET implementados; paginación20/100/offset, orden estable y NULL históricos.                                            |
| Previsualización sin persistencia | POST /simulations/preview; mismo cálculo y sin escrituras SQLite.                                                       |
| Frontend Angular                  | Incrementos TASK044P/TASK045BP en `feature/mvp-frontend`; no integrado en `main`. FastAPI conserva autoridad económica. |
| CI y despliegue                   | Pendientes.                                                                                                             |

El detalle de la reconciliación con el enunciado original está en la [matriz de trazabilidad](docs/requirements/requirements-traceability.md). La propuesta de entrega está en la [hoja de ruta del MVP](docs/planning/mvp-roadmap.md).

## API actual

La aplicación expone:

- `GET /health`
- `GET /openapi.json`
- `POST /customers`
- `POST /simulations`
- `GET /customers?search=acme&limit=20&offset=0`
- `GET /customers/{customer_id}`
- `GET /customers/{customer_id}/simulations?limit=20&offset=0`
- `POST /simulations/preview`

`POST /customers`: legal_name, tax_id, email, country (ES/PT/FR/DE/IT/NL), plan (standard).

`POST /simulations`: customer_id, user_count (0..1.000.000), storage_gb
(0..1.000.000), api_calls_per_month (0..1.000.000.000), todos obligatorios y enteros
estrictos salvo UUID. Rechaza extras; peticiones anteriores sin consumos ya no son
compatibles. Servidor fija billing_period mensual; devuelve subtotal, IVA, total EUR
y conversión. display_currency opcional EUR/USD/GBP; resto de cálculos solo servidor.

Los errores controlados usan `application/problem+json`.

Las páginas contienen items/total/limit/offset. Búsqueda parcial literal por nombre
o tax_id, Unicode casefold sin quitar acentos; search máximo255 tras recortar.
Historial más reciente primero, sin recalcular datos antiguos ni consultar FX.
Preview reutiliza el cuerpo de creación, devuelve200 sin id ni created_at persistidos;
guardar sigue siendo POST /simulations. Dashboard, alta, búsqueda, ficha e historial
están conectados localmente. El simulador envía preview y guardado explícito; los
cálculos económicos siguen siendo responsabilidad de FastAPI.

## Estructura

```text
.
├─ backend/          # FastAPI, dominio, aplicación, infraestructura, migraciones y pruebas
├─ frontend/         # Angular; TASK041 base, TASK042 clientes, TASK043 simulador (local, no publicado)
├─ docs/             # Requisitos, ADRs, evaluación, proceso, especificaciones y planificación
├─ ai-workspace/     # Trazabilidad del desarrollo asistido por IA
├─ AGENTS.md         # Instrucciones para agentes de IA
└─ .env.example      # Plantilla de configuración local
```

El backend está implementado e integrado en `main`. El frontend implementa localmente dashboard, clientes y simulador (TASK041–043); los cambios siguen sin publicar y esperan revisión independiente. No se declara completo el MVP: P-05/despliegue y CI continúan pendientes. La ubicación definitiva del composition root sigue siendo una propuesta provisional en `backend/src/saas_o_matic/bootstrap/`.

## Puesta en marcha del frontend

Requiere Node.js 24 LTS y npm 11. Desde `frontend/`, instala de forma reproducible sin
ejecutar scripts de terceros mediante `npm ci --ignore-scripts`; después inicia con
`npm start`. Esta modalidad conserva bloqueados los cuatro scripts nativos opcionales.
En otra terminal, iniciar el backend siguiendo [backend/README.md](backend/README.md).
Angular escucha en `127.0.0.1:4200` y usa el proxy `/api` hacia FastAPI en
`127.0.0.1:8000`. Ver [frontend/README.md](frontend/README.md) para scripts, pruebas,
limitaciones y detalles de la configuración. La validación de TASK043 incluye integración
real con FastAPI/SQLite; la instalación limpia, auditoría WCAG formal, revisión
independiente y publicación siguen pendientes.

## Puesta en marcha del backend

Requiere Python 3.13 y PowerShell en Windows. Desde `backend/`:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]" -c requirements.lock
python -m alembic upgrade head
python -m uvicorn saas_o_matic.bootstrap.main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`; la documentación interactiva, en `/docs`.

`DATABASE_URL` afecta tanto a Alembic como al runtime. Si no se define, ambos usan
`backend/var/saas_o_matic.sqlite3`; las rutas SQLite relativas se resuelven desde
`backend/`. El backend no carga `.env` automáticamente: exporta la variable en el
proceso. Solo se admite SQLite de fichero. Véase [`.env.example`](.env.example).

`-c requirements.lock` aplica restricciones de versión; no es un lock estricto con hashes. Las instrucciones detalladas del backend, incluidas las comprobaciones y la solución de problemas, están en [backend/README.md](backend/README.md). El estado funcional vigente es el resumido en este README.

## Pruebas y calidad

Desde `backend/`, con el entorno virtual activado:

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m mypy .
python -m pip check
```

Resultado confirmado en TASK034: **240 pruebas superadas**, Ruff, Ruff format, mypy y `pip check` sin errores.

TASK036: **340 pruebas superadas** (+100 netas), Ruff, formato, mypy y `pip check`
correctos; 35 pines del lock sin discrepancias. Cambios locales todavía sin publicar.

TASK037: **411 pruebas superadas** (+71), Ruff, formato, mypy y pip check correctos;
35 pines intactos. Smoke real EUR/USD/GBP separado de la suite sin Internet.

TASK038: **538 pruebas superadas** (+127), incluidos flujo backend completo,
Unicode/literales, históricos y SQLite authorizer sin DML durante preview. Sin nuevas
migraciones ni dependencias; trabajo local pendiente de revisión.

TASK039B: **579 pruebas superadas** (+41 sobre 538), Ruff, formato, mypy y `pip check`
correctos; 35 pines sin cambios. Añade resolución SQLite compartida runtime/Alembic,
prueba sobre base alternativa, límites FX defensivos, `503` sin filas parciales y
corrupción de historial controlada. Sin publicación.

TASK041 (frontend local): Vitest **9 pruebas superadas**; TypeScript estricto, ESLint,
Prettier y build de producción correctos; Playwright Chromium **4 smoke tests**
superados. El proxy respondió GET `/api/customers` con HTTP 200 frente a FastAPI y
SQLite temporal migrada. El `npm audit` high comunicado entonces se reevaluó en
TASK042: la advisory de picomatch fue retirada por GitHub y la auditoría actual está
limpia; véase [TASK042](ai-workspace/01-tasks/TASK042-customer-management-frontend.md).

TASK042 (frontend local): Vitest **35 pruebas superadas**, 11 archivos; Playwright
Chromium **12 pruebas superadas** en ejecución con integración real contra FastAPI y
SQLite temporal (11 pruebas de UI y un flujo integrado; no depende de Frankfurter).
TypeScript, ESLint, Prettier y build de producción correctos; también pasan las 579
pruebas backend. Sin dependencias nuevas ni cambios backend. En ese corte, TASK043 aún
no se había iniciado.

TASK043 (simulador local): Vitest **37/37**; Playwright general **17 pasadas y 2
opt-in omitidas**; integración real y captura visual opt-in superadas en ejecuciones
dedicadas. TypeScript, ESLint, Prettier y build de producción correctos; Ruff, formato,
mypy, pip check y Pytest **579/579** correctos. `npm audit` y `npm audit --omit=dev`
reportaron cero vulnerabilidades. La integración real cubrió preview no persistente,
guardado explícito, historial/recarga y casos sintéticos ES/PT/cero. Conversión USD/GBP:
consultas puntuales reales, separadas de la suite determinista. Cambios locales sin
publicar; revisión técnica/visual pendiente. No se ejecutó `npm ci`; cuatro scripts de
instalación requieren revisión/autorización. V43-01–07 quedan pendientes de TASK044.

## Documentación

- [Requisitos funcionales](docs/requirements/functional-requirements.md)
- [Matriz de trazabilidad del reto](docs/requirements/requirements-traceability.md)
- [Hoja de ruta optimizada del MVP](docs/planning/mvp-roadmap.md)
- [ADR 0001 — Stack tecnológico](docs/adr/0001-technology-stack.md)
- [ADR 0002 — Arquitectura](docs/adr/0002-architecture.md)
- [ADR 0003 — Stack Angular](docs/adr/0003-angular-frontend-stack.md)
- [Especificación 001 — Alta de clientes](docs/specs/001-customer-registration/spec.md)
- [Especificación 002 — Precios progresivos](docs/specs/002-progressive-pricing/spec.md)
- [Especificación 003 — Simulaciones](docs/specs/003-simulations/spec.md)
- [Especificación 004 — Internacionalización y consumos](docs/specs/004-international-customers-and-simulations/spec.md)
- [Especificación 005 — Impuestos y divisas](docs/specs/005-taxes-and-currency-conversion/spec.md)
- [Especificación 006 — Consultas y previsualización](docs/specs/006-customer-queries-and-preview/spec.md)
- [Especificación 007 — Fundamentos del frontend Angular](docs/specs/007-angular-frontend-foundation/spec.md)
- [Especificación 008 — Gestión frontend de clientes](docs/specs/008-customer-management-frontend/spec.md)
- [Especificación 009 — Simulador interactivo](docs/specs/009-interactive-subscription-simulator/spec.md)
- [Registro TASK041](ai-workspace/01-tasks/TASK041-angular-frontend-foundation.md)
- [Registro TASK042](ai-workspace/01-tasks/TASK042-customer-management-frontend.md)
- [Manifiesto inicial TASK042](ai-workspace/01-tasks/TASK042-initial-hashes.json)
- [Informe TASK043](ai-workspace/01-tasks/TASK043-interactive-subscription-simulator.md)
- [Preparación TASK043P](ai-workspace/01-tasks/TASK043P-frontend-intermediate-publication.md)
- [README frontend](frontend/README.md)
- [Proceso de desarrollo asistido por IA](docs/process/ai-assisted-development.md)
- [Índice de trazabilidad del desarrollo asistido por IA](ai-workspace/README.md)

## Alcance excluido

Salvo decisión posterior del propietario, quedan fuera de alcance:

- Autenticación, JWT, autorización y multi-tenancy.
- Stripe, cobros reales, facturación y conciliación de pagos.
- Microservicios, Kubernetes e infraestructura distribuida.
- Facturas PDF, envío de correos y notificaciones.
- IA integrada en la aplicación.
- Aprovisionamiento real de suscripciones.

La aplicación **estima** costes: no factura, no cobra y no provisiona servicios.

## Convenciones de trabajo

- Ramas: `docs/`, `feature/`, `fix/`, `test/` y `refactor/`.
- Commits en formato [Conventional Commits](https://www.conventionalcommits.org/).
- El propietario define el alcance, decide las cuestiones funcionales y técnicas pendientes, autoriza expresamente las operaciones Git que formen parte de una tarea, revisa los cambios y resultados y conserva la decisión final sobre la integración.
- OpenCode + DeepSeek pueden ejecutar `git add`, `git commit`, `git push` y crear pull requests cuando la tarea incluya expresamente esa operación y el propietario la autorice; también pueden redactar descripciones y resúmenes de PR. La autorización para implementar no implica autorización para publicar.
- El merge de pull requests corresponde exclusivamente al propietario.
- Prohibido el force-push (incluido `--force-with-lease`), `git reset --hard`, `git clean -fd` y cualquier otra operación destructiva.

La fuente principal de estas reglas es el [proceso de desarrollo](docs/process/ai-assisted-development.md).

## Licencia

MIT. Consulta [LICENSE](LICENSE).
