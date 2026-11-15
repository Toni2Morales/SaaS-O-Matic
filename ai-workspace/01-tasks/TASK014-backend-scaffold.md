# TASK014 — Scaffold del backend y entorno virtual Python

| Campo | Valor |
| --- | --- |
| ID | TASK014 |
| Título | Scaffold del backend y entorno virtual Python |
| Estado | En curso; cambios locales preparados, pendiente de revisión del propietario |
| Fecha | 2026-11-15 |
| Participantes | Propietario (solicitud, autorización de rama y cambios, decisión de instalar Python 3.13) / OpenCode + DeepSeek (materialización) |
| Autorización Git | Crear la rama `feature/backend-scaffold` y modificar archivos; `git add`, `git commit`, `git push`, PR y merge no autorizados |

## 1. Objetivo y alcance

Crear la estructura inicial del backend con Python 3.13, FastAPI y arquitectura de monolito modular, con un entorno virtual `.venv` aislado y reproducible. Incluye una aplicación mínima con `GET /health` y OpenAPI, pruebas de infraestructura y reglas de dependencia, y la documentación de instalación y ejecución.

No se implementan funcionalidades de negocio, modelos de datos, migraciones ni acceso real a base de datos.

## 2. Instrucciones y fuentes

| Tipo de fuente | Referencia | Estado |
| --- | --- | --- |
| Instrucción original | Instrucción TASK014 facilitada en la sesión de OpenCode | Disponible en la sesión |
| Requisitos | [functional-requirements.md](../../docs/requirements/functional-requirements.md) | Disponible; pendiente de aprobación formal |
| Stack | [ADR 0001](../../docs/adr/0001-technology-stack.md) | Disponible |
| Arquitectura | [ADR 0002](../../docs/adr/0002-architecture.md) | Disponible; composition root provisional |
| Proceso | [ai-assisted-development.md](../../docs/process/ai-assisted-development.md) | Disponible; utilizado provisionalmente |
| Contexto | [ai-workspace/README.md](../README.md) y `00-project-context/` | Disponible |
| Estado de Git y PR #1 | Git, GitHub CLI y repositorio local | Verificado directamente |

## 3. Herramientas y participantes

- Propietario: definió el alcance, autorizó la rama y los cambios, y eligió instalar Python 3.13 cuando se detectó que no estaba disponible.
- OpenCode + DeepSeek: creó el entorno virtual, materializó el scaffold, ejecutó las pruebas y documentó el resultado.
- ChatGPT: no consta participación directa en TASK014.
- Herramientas: PowerShell, Git, Python 3.13.17, `venv`, pip, Pytest, Ruff, mypy, HTTPX y Uvicorn.

## 4. Plan y decisiones

Plan:

1. Comprobar el estado de `main`, `origin/main`, el PR #1 y el árbol de trabajo.
2. Detectar la ausencia de Python 3.13 y consultar al propietario antes de sustituirlo.
3. Instalar Python 3.13.17 con autorización expresa del propietario.
4. Crear `feature/backend-scaffold` desde `origin/main`, sin escribir en `main`.
5. Crear `backend/.venv` con `py -3.13 -m venv .venv`.
6. Crear la estructura de paquetes, la aplicación FastAPI mínima y las pruebas.
7. Instalar dependencias con `python -m pip` dentro de `.venv` y generar `requirements.lock`.
8. Ejecutar Pytest, Ruff, mypy y comprobaciones de aislamiento.
9. Actualizar la documentación y la trazabilidad.

Decisiones:

- La rama se creó desde `origin/main` (`50f80470eafc9517a277b652252391880b4a491e`), no desde `main` local, que estaba dos commits por detrás.
- Se retiró el upstream heredado de `origin/main` para evitar que un `git push` accidental publicara la rama de trabajo en `main`; no se configuró un upstream remoto porque el push no está autorizado.
- `backend/.venv` es local y está excluido por la regla `.venv` del `.gitignore` raíz.
- Las dependencias directas se fijan con versiones exactas en `pyproject.toml`; `requirements.lock` fija las versiones resueltas de las dependencias transitivas.
- `bootstrap/` se usa como composition root provisional. La ubicación definitiva sigue pendiente.
- Las pruebas usan `httpx.ASGITransport` con `asyncio.run`, evitando el aviso de deprecación de `TestClient` observado con las versiones instaladas.
- No se añaden dependencias de negocio ni se implementan funcionalidades fuera del scaffold.

## 5. Archivos afectados

Creados (sin incluir el contenido de `.venv`, que no se versiona):

- `backend/pyproject.toml`
- `backend/README.md`
- `backend/requirements.lock`
- `backend/src/saas_o_matic/__init__.py`
- `backend/src/saas_o_matic/domain/__init__.py`
- `backend/src/saas_o_matic/application/__init__.py`
- `backend/src/saas_o_matic/infrastructure/__init__.py`
- `backend/src/saas_o_matic/presentation/__init__.py`
- `backend/src/saas_o_matic/presentation/health.py`
- `backend/src/saas_o_matic/presentation/app.py`
- `backend/src/saas_o_matic/bootstrap/__init__.py`
- `backend/src/saas_o_matic/bootstrap/main.py`
- `backend/tests/test_health.py`
- `backend/tests/test_architecture.py`
- `ai-workspace/01-tasks/TASK013-documentation-publication.md`
- `ai-workspace/01-tasks/TASK014-backend-scaffold.md`

Modificados:

- `README.md`
- `docs/adr/0001-technology-stack.md`
- `docs/adr/0002-architecture.md`
- `ai-workspace/README.md`
- `ai-workspace/00-project-context/architectural-evolution.md`

No modificados:

- `LICENSE`
- `TASKS.zip` (sin seguimiento y fuera de Git)

## 6. Validaciones ejecutadas

| Comprobación | Resultado |
| --- | --- |
| Python 3.13 | 3.13.17; `py -3.13` apunta a la instalación local |
| Intérprete del entorno | `backend\.venv\Scripts\python.exe`; `sys.prefix` = `backend\.venv`; `base_prefix` = Python 3.13 del sistema |
| Instalación | `python -m pip install -e ".[dev]"` completada dentro de `.venv` |
| Reinstalación con restricciones | `python -m pip install -e ".[dev]" -c requirements.lock` completada |
| `requirements.lock` frente a `pip freeze` | 33 paquetes; 0 diferencias |
| `pip check` | Sin dependencias rotas |
| Pytest | 4 pruebas superadas |
| Ruff check | Sin hallazgos |
| Ruff format check | 12 archivos ya formateados |
| mypy | Sin errores en 11 archivos fuente |
| `/health` real con Uvicorn | HTTP 200; `{"status":"ok"}` |
| `/openapi.json` real con Uvicorn | OpenAPI 3.1.0; título `SaaS-O-Matic API`; ruta `/health` presente |
| Aislamiento de `.venv` | `git check-ignore` confirma la regla `.venv` para `backend/.venv/pyvenv.cfg` |
| `TASKS.zip` | Sin seguimiento y fuera de Git |
| Staging | Ninguno; no se ejecutaron `git add`, commit, push, PR ni merge |

Dependencias directas instaladas:

| Dependencia | Versión |
| --- | --- |
| FastAPI | 0.163.1 |
| Pydantic | 2.14.3 |
| SQLAlchemy | 2.1.8 |
| Alembic | 1.20.1 |
| Uvicorn | 0.54.0 |
| Pytest | 9.2.0 |
| HTTPX | 0.28.1 |
| Ruff | 0.17.5 |
| mypy | 2.4.1 |

## 7. Hallazgos y correcciones

- **Python 3.13 no disponible inicialmente:** se detuvo la implementación y se consultó al propietario. El propietario autorizó la instalación; se instaló Python 3.13.17 con `winget`.
- **`main` local desactualizado:** `main` estaba en `8371f9f` y `origin/main` en `50f8047`. La rama se creó desde `origin/main` para no escribir en `main`.
- **Aviso de deprecación de `TestClient`:** se sustituyó por `httpx.ASGITransport` con `asyncio.run` en las pruebas.
- **Composition root provisional:** `bootstrap/` se documenta como propuesta, no como decisión cerrada.

## 8. Autorizaciones Git

Se autorizaron únicamente la creación de `feature/backend-scaffold` y la modificación de archivos para TASK014. No se autorizaron `git add`, `git commit`, `git push`, creación de PR ni merge. No se modificó `main` y no se ejecutaron operaciones destructivas.

## 9. Resultado y decisiones pendientes

- Resultado: scaffold local del backend preparado; entorno virtual aislado; aplicación, pruebas y documentación creadas; comprobaciones superadas.
- Decisiones pendientes: revisión del propietario, autorización de commit/push/PR y confirmación de la ubicación definitiva del composition root.
- Riesgos: no existe todavía frontend ni lógica de negocio; `main` local sigue por detrás de `origin/main`; las dependencias transitivas dependen de `requirements.lock`; no consta revisión independiente de TASK014.

## 10. Referencias

- Instrucción TASK014 en la sesión de OpenCode
- [ADR 0001 — Stack tecnológico](../../docs/adr/0001-technology-stack.md)
- [ADR 0002 — Arquitectura](../../docs/adr/0002-architecture.md)
- [Requisitos funcionales](../../docs/requirements/functional-requirements.md)
- [Proceso de desarrollo asistido por IA](../../docs/process/ai-assisted-development.md)
- [TASK013-documentation-publication.md](TASK013-documentation-publication.md)
- [PR #1](https://github.com/Toni2Morales/SaaS-O-Matic/pull/1)
- [backend/README.md](../../backend/README.md)
