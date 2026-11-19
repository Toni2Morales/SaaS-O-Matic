# SaaS-O-Matic

**Herramienta interna para estimar suscripciones SaaS corporativas.** El equipo comercial
registra clientes, configura consumo y consulta una proyección mensual en EUR/USD/GBP.
FastAPI es la autoridad de precios, impuestos, conversión y persistencia; Angular ofrece la
interfaz. Es un MVP local para evaluación técnica, no un sistema de facturación.

> **Estado de entrega:** MVP integrado en `main` por PR #7 (merge commit
> `99c0ebac984c70521c4e3c94226b35c15303f572`). Repositorio público. Quick Start, manuales,
> diagramas, workflows CI y trazabilidad están en preparación en `docs/final-delivery`.
> No se declara aptitud para exposición pública en producción.

## Quick Start

Requisitos ya instalados: Git, Python **3.13** (`>=3.13,<3.14`), Node.js **24**
(`>=24.15,<25`) y npm **11** (`>=11,<12`). Los scripts no instalan runtimes ni modifican
políticas/permisos. Internet se requiere para dependencias y tasas FX USD/GBP.

### Windows (PowerShell; probado localmente)

```powershell
git clone https://github.com/Toni2Morales/SaaS-O-Matic.git
cd SaaS-O-Matic
.\start.ps1
```

### Linux (Ubuntu; validación de CI pendiente) / macOS (no probado)

```bash
git clone https://github.com/Toni2Morales/SaaS-O-Matic.git
cd SaaS-O-Matic
bash start.sh
```

Frontend: <http://127.0.0.1:4200> · Swagger: <http://127.0.0.1:8000/docs> · Health:
<http://127.0.0.1:8000/health>.

Detener los procesos propios registrados con `.\start.ps1 -Stop` (Windows) o
`bash start.sh --stop` (Bash), desde otra terminal en la raíz. Reiniciar con el
comando de arranque de la plataforma. Los procesos escuchan en loopback; si 4200/8000 están
ocupados, el script aborta sin detener ni modificar procesos ajenos. SQLite se conserva en
`backend/var/saas_o_matic.sqlite3`; no se crean clientes de demo automáticamente.

> Linux/macOS y la detención/reinicio deben considerarse verificados solo cuando el run de
> Quick Start CI termine satisfactoriamente. Esta rama aún está en validación.

Guía [manual, solución de problemas y límites de plataforma](docs/guides/local-development.md).

## Funcionalidades

- Alta de clientes ES/PT/FR/DE/IT/NL, plan único `standard`, validación algorítmica de
  DNI/NIF/NIE/CIF españoles y validación genérica no oficial en otros países.
- Dashboard, búsqueda por nombre o identificador fiscal, ficha e historial paginado.
- Simulador mensual con preview sin persistencia y guardado explícito.
- Pricing progresivo por usuario, impuestos generales de país, divisas EUR/USD/GBP y
  snapshots históricos inmutables.
- Almacenamiento y llamadas API se registran como datos informativos, sin cargos.
- Estados de validación, carga, error, navegación por teclado y layouts responsive.

Detalles: [pricing, impuestos y FX](docs/guides/pricing-and-limits.md).

## Arquitectura

Monolito modular: Angular → FastAPI → casos de uso/dominio → adaptadores SQLAlchemy/SQLite y
Frankfurter. FastAPI es la autoridad económica. El frontend usa un proxy de desarrollo
local; no se ha implementado ni validado un proxy productivo.

[Diagramas Mermaid de contexto, capas, frontend, datos y secuencias](docs/architecture/solution-overview.md).

## Stack verificado

| Componente                                | Versión declarada                                     |
| ----------------------------------------- | ----------------------------------------------------- |
| Python                                    | `>=3.13,<3.14` (local: 3.13.17)                       |
| FastAPI / Pydantic / SQLAlchemy / Alembic | 0.163.1 / 2.14.3 / 2.1.8 / 1.20.1                     |
| Node.js / npm                             | `>=24.15,<25` / `>=11,<12` (local: 24.22.0 / 11.19.1) |
| Angular / TypeScript / RxJS               | 22.2.6 / 6.0.3 / 7.8.2                                |
| Vitest / Playwright Test                  | 5.1.1 / 1.65.1                                        |
| Persistencia                              | SQLite, Alembic 0001–0004                             |

Fuentes: `backend/pyproject.toml`, `backend/requirements.lock`, `frontend/package.json`,
`frontend/package-lock.json`, `.nvmrc` y ADR-0001/0003.

## Instalación manual

La guía [local-development](docs/guides/local-development.md) contiene comandos completos
para backend y frontend, pruebas, browsers Playwright y troubleshooting. Resumen:

- Backend: crear `backend/.venv`, instalar `.[dev]` con `-c requirements.lock`, aplicar
  `alembic upgrade head`, luego iniciar `python -m uvicorn` en loopback 8000.
- Frontend: `npm ci --ignore-scripts`, `npm start`; proxy `/api` hacia backend 8000.
- Playwright solo se necesita para QA: instalar browsers oficiales desde el workspace con
  `npx playwright install chromium firefox webkit`.

El lock Python aplica constraints, no fija hashes ni build isolation. npm respeta el lockfile
y omite scripts de instalación.

## Calidad e integración continua

**Histórico TASK046 (no CI):** Pytest 579/579; Ruff/formato/mypy/pip check PASS; Vitest
40/40; coverage statements 86,20 %, branches 81,86 %, functions 67,19 %, lines 86,84 %;
Playwright 79 PASS y 20 opt-in skips; integración dedicada 1 PASS; audits npm sin
vulnerabilidades notificadas. Véase el
[informe TASK046](ai-workspace/01-tasks/TASK046-final-frontend-pull-request.md).

**TASK047, clon limpio Windows del commit inicial Quick Start `b7341e3`:** backend Pytest
579/579, Ruff/formato/mypy/pip check PASS; frontend typecheck/lint/Prettier, Vitest 40/40,
build y ambos audits PASS; cobertura statements 86,27 %, branches 81,86 %, functions
67,72 %, lines 86,93 %. Playwright: 79 PASS/20 skips, sin fallos; se observaron dos
mensajes no fatales de importación dinámica durante WebKit. Integración real determinista
1/1 y verificación de historial tras reinicio 1/1 PASS (tasas fixture, no FX vivo). Los
resultados son TASK047 local en clon Windows, no GitHub Actions.

GitHub Actions de esta rama validarán backend, frontend, Playwright y Quick Start Windows/
Linux. **Ejecuciones reales: pendientes** hasta comprobar runs de GitHub; no se muestran
badges como satisfactorios antes de esa evidencia. Axe en nueve estados Chromium sin
violaciones detectadas durante TASK046 no es certificación WCAG; responsive se comprobó en
cinco viewports/rutas en Chromium, Firefox y WebKit.

## Desarrollo asistido por IA

Secuencia: requisitos → ADR/SPEC → plan/tasks → aprobación humana → implementación y
pruebas → auditoría/correcciones → commits/pushes controlados → PR y merge humano. Véanse el
[proceso de desarrollo asistido](docs/process/ai-assisted-development.md) y el
[plan TASK047](ai-workspace/01-tasks/TASK047-final-delivery-plan.md). No se inventan
conversaciones; las interacciones privadas no disponibles deben aportarse por el propietario.
Capturas funcionales requieren aprobación y no se publican en esta fase. El índice de
trazabilidad IA y el inventario de evidencias se enlazarán al completar esos entregables.

## Limitaciones

- Seis países, un plan `standard`; IVA general simplificado; validación fiscal algorítmica
  no verifica existencia/titularidad.
- Monedas EUR/USD/GBP. Referencias fechadas Frankfurter con caché backend 24 h y timeout
  5 s; no son cotizaciones continuas y el proveedor puede fallar.
- SQLite local tiene límites de concurrencia. Sin autenticación, autorización,
  multi-tenancy, facturación real ni aprovisionamiento.
- Exposición pública/producción, hosting, CI/CD y seguridad de despliegue no están
  validados; P-05 sigue abierto. Axe no constituye certificación integral WCAG.
- Almacenamiento y llamadas API no se cobran. No se certifican escalabilidad ni idoneidad
  operativa para datos reales.

## Requisitos y documentación

- [Requisitos funcionales](docs/requirements/functional-requirements.md) ·
  [trazabilidad del reto](docs/requirements/requirements-traceability.md) ·
  [matriz final TASK047](docs/requirements/final-delivery-traceability.md).
- [ADR-0001 stack](docs/adr/0001-technology-stack.md) ·
  [ADR-0002 arquitectura](docs/adr/0002-architecture.md) ·
  [ADR-0003 Angular](docs/adr/0003-angular-frontend-stack.md).
- Especificaciones: [001](docs/specs/001-customer-registration/spec.md),
  [002](docs/specs/002-progressive-pricing/spec.md), [003](docs/specs/003-simulations/spec.md),
  [004](docs/specs/004-international-customers-and-simulations/spec.md),
  [005](docs/specs/005-taxes-and-currency-conversion/spec.md),
  [006](docs/specs/006-customer-queries-and-preview/spec.md),
  [007](docs/specs/007-angular-frontend-foundation/spec.md),
  [008](docs/specs/008-customer-management-frontend/spec.md),
  [009](docs/specs/009-interactive-subscription-simulator/spec.md),
  [010](docs/specs/010-frontend-refinement-and-e2e/spec.md).
- [Guía de instalación](docs/guides/local-development.md) ·
  [arquitectura](docs/architecture/solution-overview.md) ·
  [pricing/FX](docs/guides/pricing-and-limits.md).
- [README backend](backend/README.md) · [README frontend](frontend/README.md).

## Licencia

Distribuido bajo licencia [MIT](LICENSE).
