# TASK023 - Publicación controlada del alta de clientes (PR #3)

| Campo | Valor |
| --- | --- |
| ID | TASK023 |
| Título | Publicación controlada del alta de clientes mediante PR #3 |
| Estado | **Registro previo al commit; publicación pendiente de ejecución** |
| Fecha | 2026-11-16 |
| Rama | `feature/customer-registration` |
| Base | `be755a68a52392fd562eb3901e317bc85b1ed8e9` (`HEAD` y `origin/main`) |
| Autorización Git | `git add` selectivo, un commit, push normal y creación de un PR; merge, force-push, reescritura de historial y escritura en `main` no autorizados |
| Commit / push / PR | Pendientes de ejecución en el momento de crear este registro; los identificadores reales se incluyen en el informe final de la sesión |

## 1. Objetivo y alcance

Publicar la implementación acumulada de TASK018, TASK019, TASK020 y TASK022 en la rama `feature/customer-registration`, mediante un único commit y un PR hacia `main`.

La publicación incluye exclusivamente:

- Dominio, aplicación, infraestructura, presentación y bootstrap del alta de clientes.
- Configuración y migración Alembic `0001_create_customers`.
- Pruebas de clientes, problemas HTTP, salud y migraciones.
- Dependencias justificadas de TASK019.
- Requisitos, especificación, plan y tareas.
- Registros de trazabilidad de TASK017, TASK018, TASK019, TASK020 y TASK022.
- Actualizaciones de README y contexto.
- Este registro TASK023.

No se incluyen `LICENSE`, `TASKS.zip`, `backend/.venv`, bases SQLite, cachés, temporales ni secretos.

## 2. Comprobaciones previas

| Comprobación | Resultado real |
| --- | --- |
| Rama activa | `feature/customer-registration` |
| `HEAD` | `be755a68a52392fd562eb3901e317bc85b1ed8e9` |
| `git fetch origin` | Ejecutado |
| `origin/main` | `be755a68a52392fd562eb3901e317bc85b1ed8e9`; sin cambios inesperados |
| Estado inicial | 11 modificados, 42 no rastreados, 53 entradas; 0 staged |
| `LICENSE` | Sin modificaciones y sin cambios staged |
| `git diff --check` | Sin errores |
| Inventario tras crear TASK023 | 11 modificados, 43 no rastreados, 54 entradas; 0 staged |

El estado inicial coincide con el esperado. La única entrada adicional es este registro TASK023, requerido por la tarea antes del commit.

## 3. Validaciones ejecutadas

Todas las comprobaciones se ejecutaron desde `backend/` con `backend/.venv` y sin usar bases de datos existentes.

| Comprobación | Resultado real |
| --- | --- |
| `python -m pytest` | **100 passed in 2.32s** |
| `python -m ruff check .` | **All checks passed!** |
| `python -m ruff format --check .` | **44 files already formatted** |
| `python -m mypy .` | **Success: no issues found in 42 source files** |
| `python -m pip check` | **No broken requirements found.** |
| Lock frente a `pip freeze` | **35/35 coinciden; 0 diferencias** |
| `git diff --check` | Sin errores |

### 3.1 Migración Alembic

Sobre una base SQLite temporal:

- `alembic upgrade head`: correcto.
- `alembic current`: `0001_create_customers (head)`.
- `alembic downgrade base`: correcto.
- `alembic upgrade head`: correcto.
- Base temporal eliminada al terminar.

No se modificó la migración ni se creó una revisión nueva.

### 3.2 Comprobaciones HTTP

Se usó una base SQLite temporal migrada con Alembic y eliminada al terminar.

| Comprobación | Resultado real |
| --- | --- |
| `GET /health` | `200` con `{"status":"ok"}` |
| `GET /openapi.json` | `200`; `legal_name` con `minLength: 1` y `maxLength: 255` |
| `POST /customers` con `"  Empresa  Ejemplo S.L.  "` y `" b-12345674 "` | `201`; respuesta y SQLite con `"Empresa  Ejemplo S.L."` y `"B12345674"` |
| Duplicado fiscal normalizado | `409` con `application/problem+json` |
| `legal_name` vacío, solo espacios o 256 caracteres | `422` en los tres casos |
| Plan distinto de `standard` | `422` |
| País distinto de `ES` | `422` |
| Identificador fiscal inválido | `422` |
| Persistencia tras los casos inválidos | Se mantiene una única fila válida; los inválidos no se persisten |

La comprobación con `TestClient` emitió un aviso de deprecación de Starlette sobre `httpx`, no bloqueante. Las pruebas del repositorio usan `AsyncClient`.

## 4. Inventario autorizado

El commit debe contener exactamente estas 54 rutas.

### 4.1 Archivos modificados (11)

```text
README.md
ai-workspace/00-project-context/ai-tools-and-roles.md
ai-workspace/00-project-context/architectural-evolution.md
ai-workspace/README.md
backend/README.md
backend/pyproject.toml
backend/requirements.lock
backend/src/saas_o_matic/bootstrap/main.py
backend/src/saas_o_matic/presentation/app.py
backend/tests/test_health.py
docs/requirements/functional-requirements.md
```

### 4.2 Archivos nuevos (43)

```text
ai-workspace/01-tasks/TASK017-backend-publication.md
ai-workspace/01-tasks/TASK018-customer-registration.md
ai-workspace/01-tasks/TASK019-customer-implementation.md
ai-workspace/01-tasks/TASK020-customer-registration-completion.md
ai-workspace/01-tasks/TASK022-customer-validation-fix.md
ai-workspace/01-tasks/TASK023-customer-publication.md
backend/alembic.ini
backend/migrations/env.py
backend/migrations/script.py.mako
backend/migrations/versions/0001_create_customers.py
backend/migrations/versions/README.md
backend/src/saas_o_matic/application/customers/__init__.py
backend/src/saas_o_matic/application/customers/catalogs.py
backend/src/saas_o_matic/application/customers/dto.py
backend/src/saas_o_matic/application/customers/errors.py
backend/src/saas_o_matic/application/customers/use_cases.py
backend/src/saas_o_matic/bootstrap/customers.py
backend/src/saas_o_matic/domain/customers/__init__.py
backend/src/saas_o_matic/domain/customers/entities.py
backend/src/saas_o_matic/domain/customers/errors.py
backend/src/saas_o_matic/domain/customers/ports.py
backend/src/saas_o_matic/domain/customers/value_objects.py
backend/src/saas_o_matic/infrastructure/customers/__init__.py
backend/src/saas_o_matic/infrastructure/customers/mappers.py
backend/src/saas_o_matic/infrastructure/customers/models.py
backend/src/saas_o_matic/infrastructure/customers/repositories.py
backend/src/saas_o_matic/infrastructure/database.py
backend/src/saas_o_matic/presentation/customers/__init__.py
backend/src/saas_o_matic/presentation/customers/dependencies.py
backend/src/saas_o_matic/presentation/customers/router.py
backend/src/saas_o_matic/presentation/customers/schemas.py
backend/src/saas_o_matic/presentation/problems.py
backend/tests/conftest.py
backend/tests/test_customer_api.py
backend/tests/test_customer_repository.py
backend/tests/test_customer_schemas.py
backend/tests/test_customer_use_case.py
backend/tests/test_migrations.py
backend/tests/test_problems.py
backend/tests/test_spanish_tax_id.py
docs/specs/001-customer-registration/plan.md
docs/specs/001-customer-registration/spec.md
docs/specs/001-customer-registration/tasks.md
```

No se incluyen archivos ajenos al alcance.

## 5. Preparación del commit

Antes del commit se debe comprobar:

- `git diff --cached --name-status` coincide con el inventario anterior.
- No hay archivos staged fuera del alcance.
- `LICENSE` no está staged.
- No hay secretos, bases SQLite, `.venv`, `TASKS.zip`, cachés ni temporales.
- El número de archivos staged es 54.

El commit autorizado es:

```text
feat: implement customer registration with Spanish tax validation
```

Se utiliza la identidad Git configurada:

```text
Antonio Morales
107318721+Toni2Morales@users.noreply.github.com
```

## 6. Push y pull request

- Push normal de `feature/customer-registration`.
- Sin `--force` ni `--force-with-lease`.
- PR único hacia `main`.
- Título: `feat: implement customer registration`.
- Sin merge; el merge corresponde al propietario.

Los identificadores reales de commit, push y PR se verifican después de la publicación y se incluyen en el informe final de la sesión.

## 7. Hallazgos menores pendientes

| ID | Estado | Descripción |
| --- | --- | --- |
| m-01 | Pendiente | Validación de tipos de `plan` y `country` en la entidad de dominio. |
| m-02 | Pendiente | Restricciones `CHECK` de país y plan en base de datos. |
| m-03 | Pendiente | Formato de nombres de campo en errores `422`. |
| m-04 | Pendiente | Logging de excepciones `500` en servidor. |

Son observaciones menores, no defectos bloqueantes de esta entrega. m-05 quedó cubierto por TASK022.

## 8. Verificación posterior al PR

Pendiente de completar tras la publicación:

- Número y URL del PR.
- Rama base `main` y rama origen `feature/customer-registration`.
- SHA del commit publicado.
- Inventario de archivos del PR.
- Estado abierto y ausencia de merge.
- Estado final del árbol de trabajo.

No se realizarán operaciones adicionales sobre GitHub.
