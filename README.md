# SaaS-O-Matic

Herramienta interna para que el equipo comercial simule y estime el coste de suscripciones SaaS corporativas: clientes, planes, consumo estimado, tramos de usuarios, impuestos por país y conversión de divisas.

> **Estado:** fase de definición y fundamentos del repositorio. Todavía no existe código de aplicación, dependencias instaladas ni entorno desplegado.
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

## Estructura prevista

```text
.
├─ backend/          # API FastAPI, dominio, persistencia y migraciones
├─ frontend/         # Aplicación Angular
├─ docs/             # Requisitos, ADRs, evaluación y proceso
├─ ai-workspace/     # Contexto para sesiones de desarrollo asistido por IA
├─ AGENTS.md         # Instrucciones para agentes de IA
└─ .env.example      # Plantilla de configuración local
```

La estructura definitiva se fijará en el scaffold de cada aplicación. No se ha creado código todavía.

## Documentación

- [Requisitos funcionales](docs/requirements/functional-requirements.md)
- [Evaluación inicial del repositorio](docs/assessment/001-repository-assessment.md)
- [ADR 0001 — Stack tecnológico](docs/adr/0001-technology-stack.md)
- [ADR 0002 — Arquitectura](docs/adr/0002-architecture.md)
- [Proceso de desarrollo asistido por IA](docs/process/ai-assisted-development.md)
- [Instrucciones para agentes de IA](AGENTS.md)
- [Índice de trazabilidad del desarrollo asistido por IA](ai-workspace/README.md)

## Puesta en marcha

Pendiente. El scaffold de backend y frontend se abordará en pull requests posteriores, una vez aprobada esta base documental. En esta fase no se instalan dependencias ni se inicializan proyectos.

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
