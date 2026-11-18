# SaaS-O-Matic

> **Vigente TASK040:** el backend se publica en `feature/mvp-backend` mediante un
> Pull Request hacia `main`; integración pendiente de revisión y merge del propietario.
> Cálculo mensual con IVA general de seis
> países y conversión EUR/USD/GBP mediante Frankfurter v2. Decimal exacto, HALF_UP,
> caché en memoria 24 h, timeout5s y snapshots históricos. `display_currency` opcional
> (EUR predeterminado); 503 problem+json si no hay referencia válida. EUR funciona sin red.
> Listado/búsqueda Unicode, detalle e historial paginados y preview sin escritura disponibles.
> TASK039 auditó el backend con observaciones no bloqueantes; TASK039B corrige
> trazabilidad, README, `.env.example`, configuración SQLite compartida y límites FX.
> Sin frontend; estimación simplificada, no factura. Véanse
> [SPEC-005](docs/specs/005-taxes-and-currency-conversion/spec.md) y
> [SPEC-006](docs/specs/006-customer-queries-and-preview/spec.md).

Herramienta interna para que el equipo comercial simule y estime el coste mensual de suscripciones SaaS corporativas: clientes, planes, consumo estimado, tramos de usuarios, impuestos por país y conversión de divisas.

> **Estado real del MVP:** componentes backend funcionales implementados (TASK036–039B) y publicados para revisión en `feature/mvp-backend`; integración en `main` pendiente. **No existe Angular, CI ni despliegue.** TASK039 completada con dictamen APTA CON OBSERVACIONES; TASK039B corrige los defectos autorizados y mantiene riesgos aceptados/diferidos. Desarrollo visual pendiente.
>
> **Estado de publicación:** los PR #1 a #5 fueron fusionados por el propietario. El último merge es `b3c5ca81d23d279b478ed466757bada031aa1e1e` (PR #5, simulaciones).
>
> **Decisiones:** Q-18–Q-26 implementadas en alcance aprobado; historial inmutable por API. P-01/P-05 pendientes. Documento original no seguido ni publicado.

## Stack

Resumen; el detalle está en el [ADR 0001](docs/adr/0001-technology-stack.md) y el [ADR 0002](docs/adr/0002-architecture.md).

- **Backend:** Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2, SQLite y Alembic.
- **Calidad backend:** Pytest, HTTPX, Ruff y mypy.
- **Frontend:** Angular con TypeScript, standalone components, Signals, RxJS, Reactive Forms, Router y HttpClient. **Pendiente de implementación.**
- **Contrato de API:** OpenAPI. **Divisa base:** EUR.
- **Arquitectura:** monolito modular con dependencias hacia dentro (`presentation → application → domain`, `infrastructure → domain`).

## Estado funcional

| Área | Estado |
| --- | --- |
| Alta de clientes | Seis países, único plan `standard`; genérico no oficial fuera de ES. |
| Validación fiscal | DNI/NIF, NIE y CIF/NIF con algoritmos de control. |
| Precios progresivos | Cero = 0.00; tarifas de los tres tramos intactas. |
| Simulaciones | Mensuales persistidas, cliente y usuarios. |
| Almacenamiento y llamadas API | Obligatorios nuevos; históricos NULL; sin cargos. |
| Impuestos | IVA general por país, verificado; alcance simplificado, sin regímenes especiales. |
| Divisas | Frankfurter v2, EUR/USD/GBP, caché24h y snapshot. |
| Búsqueda, detalle e historial | GET implementados; paginación20/100/offset, orden estable y NULL históricos. |
| Previsualización sin persistencia | POST /simulations/preview; mismo cálculo y sin escrituras SQLite. |
| Frontend Angular | Pendiente. |
| CI y despliegue | Pendientes. |

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
guardar sigue siendo POST /simulations. Panel, tarjetas y slider son trabajo de UI pendiente.

## Estructura

```text
.
├─ backend/          # FastAPI, dominio, aplicación, infraestructura, migraciones y pruebas
├─ frontend/         # Pendiente de scaffold
├─ docs/             # Requisitos, ADRs, evaluación, proceso, especificaciones y planificación
├─ ai-workspace/     # Trazabilidad del desarrollo asistido por IA
├─ AGENTS.md         # Instrucciones para agentes de IA
└─ .env.example      # Plantilla de configuración local
```

El backend está implementado. El frontend todavía no se ha creado. La ubicación definitiva del composition root sigue siendo una propuesta provisional en `backend/src/saas_o_matic/bootstrap/`.

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

## Documentación

- [Requisitos funcionales](docs/requirements/functional-requirements.md)
- [Matriz de trazabilidad del reto](docs/requirements/requirements-traceability.md)
- [Hoja de ruta optimizada del MVP](docs/planning/mvp-roadmap.md)
- [ADR 0001 — Stack tecnológico](docs/adr/0001-technology-stack.md)
- [ADR 0002 — Arquitectura](docs/adr/0002-architecture.md)
- [Especificación 001 — Alta de clientes](docs/specs/001-customer-registration/spec.md)
- [Especificación 002 — Precios progresivos](docs/specs/002-progressive-pricing/spec.md)
- [Especificación 003 — Simulaciones](docs/specs/003-simulations/spec.md)
- [Especificación 004 — Internacionalización y consumos](docs/specs/004-international-customers-and-simulations/spec.md)
- [Especificación 005 — Impuestos y divisas](docs/specs/005-taxes-and-currency-conversion/spec.md)
- [Especificación 006 — Consultas y previsualización](docs/specs/006-customer-queries-and-preview/spec.md)
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
