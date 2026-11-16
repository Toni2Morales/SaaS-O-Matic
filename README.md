# SaaS-O-Matic

Herramienta interna para que el equipo comercial simule y estime el coste de suscripciones SaaS corporativas: clientes, planes, consumo estimado, tramos de usuarios, impuestos por país y conversión de divisas.

> **Estado:** alta de clientes implementada y validada localmente. Existe una aplicación FastAPI con `/health`, `POST /customers`, dominio fiscal, catálogo MVP con el único plan `standard`, migración Alembic de `customers`, persistencia SQLite, pruebas y un entorno virtual local. Los cambios de TASK020 y la corrección de TASK022 no están publicados. No hay frontend ni entorno desplegado.
>
> **Estado documental:** las decisiones de stack y alcance fueron aceptadas por el propietario. Los documentos de requisitos, ADRs, proceso y evaluación siguen pendientes de revisión o aprobación formal. El proceso se utiliza provisionalmente como referencia de trabajo hasta su aprobación.

## Stack decidido por el propietario

Resumen; el detalle, las alternativas y las decisiones pendientes están en el [ADR 0001](docs/adr/0001-technology-stack.md).

- **Backend:** Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2, SQLite y Alembic.
- **Calidad backend:** Pytest, HTTPX, Ruff y mypy.
- **Frontend:** Angular con TypeScript, standalone components, Signals, RxJS, Reactive Forms, Router y HttpClient.
- **Testing frontend:** Vitest, pendiente de confirmar su compatibilidad con la versión de Angular que se elija.
- **Contrato de API:** OpenAPI. **Divisa base:** EUR.

## Alcance

Incluido en el alcance definido por el propietario:

- Alta de clientes con razón social, identificador fiscal, email, país y plan seleccionado.
- Validación de identificadores fiscales españoles (DNI/NIF/CIF).
- Simulaciones persistidas y asociadas a un cliente.
- Cálculo del coste de usuarios mediante tramos progresivos acumulativos.
- Impuesto aplicable según el país del cliente, con reglas configurables.
- Panel de clientes con búsqueda por razón social o identificador fiscal.
- Detalle de cliente con tarjetas resumen e historial de simulaciones.
- Simulador interactivo con control deslizante de usuarios.
- Conversión de divisas a partir de una API pública de tipos de cambio.

Fuera de alcance salvo decisión posterior del propietario:

- Autenticación, autorización y multi-tenancy.
- Cobros reales, Stripe, generación de PDF y envío de correo.
- Aprovisionamiento real de suscripciones.

La aplicación **estima** costes: no factura, no cobra y no provisiona servicios.

## Estructura actual

```text
.
├─ backend/          # Scaffold FastAPI, dominio, aplicación, infraestructura y bootstrap
├─ frontend/         # Pendiente de scaffold
├─ docs/             # Requisitos, ADRs, evaluación, proceso y especificaciones
├─ ai-workspace/     # Contexto para sesiones de desarrollo asistido por IA
├─ AGENTS.md         # Instrucciones para agentes de IA
└─ .env.example      # Plantilla de configuración local
```

El backend ya dispone del alta de clientes completa a nivel de MVP, además del scaffold inicial. El frontend todavía no se ha creado. La ubicación definitiva del composition root sigue pendiente; `backend/src/saas_o_matic/bootstrap/` es una propuesta provisional.

## Documentación

- [Requisitos funcionales](docs/requirements/functional-requirements.md)
- [Evaluación inicial del repositorio](docs/assessment/001-repository-assessment.md)
- [ADR 0001 — Stack tecnológico](docs/adr/0001-technology-stack.md)
- [ADR 0002 — Arquitectura](docs/adr/0002-architecture.md)
- [Especificación 001 - Alta de clientes](docs/specs/001-customer-registration/spec.md) (implementada y validada en TASK020; cambios locales no publicados)
- [Proceso de desarrollo asistido por IA](docs/process/ai-assisted-development.md)
- [Instrucciones para agentes de IA](AGENTS.md)
- [Índice de trazabilidad del desarrollo asistido por IA](ai-workspace/README.md)

## Puesta en marcha

El backend requiere Python 3.13 y un entorno virtual local. Desde `backend/`:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]" -c requirements.lock
python -m uvicorn saas_o_matic.bootstrap.main:app --reload
```

`-c requirements.lock` aplica restricciones de versión; no es un lock estricto. La verificación de dependencias y sus límites se detallan en [backend/README.md](backend/README.md).

La aplicación expone `GET /health`, `GET /openapi.json` y `POST /customers`. Las instrucciones completas, las pruebas y las reglas de dependencia están en [backend/README.md](backend/README.md).

El frontend se abordará en una tarea posterior. El alta de clientes usa el plan MVP `standard` y una migración Alembic; no se ha creado una base SQLite de desarrollo versionada.

## Convenciones de trabajo

- Ramas: `docs/`, `feature/`, `fix/`, `test/` y `refactor/`.
- Commits en formato [Conventional Commits](https://www.conventionalcommits.org/).
- El propietario define el alcance, decide las cuestiones funcionales y técnicas pendientes, autoriza expresamente las operaciones Git que formen parte de una tarea, revisa los cambios y resultados y conserva la decisión final sobre la integración.
- OpenCode + DeepSeek pueden ejecutar `git add`, `git commit`, `git push` y crear pull requests cuando la tarea incluya expresamente esa operación y el propietario la autorice; también pueden redactar descripciones y resúmenes de PR. La autorización debe identificar la operación y los cambios o la rama afectados. La autorización para implementar no implica autorización para publicar; si la tarea no contempla expresamente commit, push o creación de PR, el agente se limita a preparar los cambios y presentar el resultado.
- El merge de pull requests corresponde exclusivamente al propietario.
- Prohibido el force-push (incluido `--force-with-lease`), `git reset --hard`, `git clean -fd` y cualquier otra operación destructiva. Los agentes no las ejecutan; esta prohibición es absoluta y no admite excepciones por autorización escrita. Si consideran que alguna es necesaria, se detienen y consultan al propietario.

La fuente principal de estas reglas es el [proceso de desarrollo](docs/process/ai-assisted-development.md).

## Licencia

MIT. Consulta [LICENSE](LICENSE).
