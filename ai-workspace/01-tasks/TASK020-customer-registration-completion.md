# TASK020 - Cierre del alta de clientes: plan `standard`, Alembic y `POST /customers`

| Campo | Valor |
| --- | --- |
| ID | TASK020 |
| Título | Completar el alta de clientes con el plan MVP `standard`, migración Alembic y endpoint operativo |
| Estado | **Completada y validada localmente; cambios no publicados** |
| Fecha | 2026-11-15 |
| Rama | `feature/customer-registration` |
| Participantes | Propietario (instrucción y decisión D-02) / OpenCode + DeepSeek (implementación, pruebas y documentación) |
| Autorización Git | Modificar archivos, crear migración, pruebas y documentación, y ejecutar validaciones locales; `git add`, commit, push, PR y merge no autorizados |

## 1. Objetivo y alcance

Completar la primera funcionalidad de negocio de SaaS-O-Matic a partir de TASK018 y TASK019:

- Aprobar y aplicar D-02: catálogo MVP con el único plan `standard`.
- Crear la migración inicial de `customers`.
- Registrar y operar `POST /customers`.
- Persistir clientes en SQLite.
- Validar entradas y traducir errores a `application/problem+json`.
- Añadir pruebas de dominio, aplicación, infraestructura, migración y API.
- Mantener Python 3.13 y las dependencias dentro de `backend/.venv`.
- No publicar cambios.

## 2. Estado Git

### 2.1 Estado inicial

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/customer-registration` |
| HEAD | `be755a68a52392fd562eb3901e317bc85b1ed8e9` |
| `origin/main` | `be755a68a52392fd562eb3901e317bc85b1ed8e9` |
| Archivos staged | Ninguno |
| Cambios de TASK018 y TASK019 | Preservados |
| `LICENSE` | Sin cambios |

### 2.2 Estado final

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/customer-registration` |
| HEAD | `be755a68a52392fd562eb3901e317bc85b1ed8e9` |
| `origin/main` | `be755a68a52392fd562eb3901e317bc85b1ed8e9` |
| Archivos staged | Ninguno |
| `git diff --check` | Sin errores |
| Commit, push, PR o merge | No ejecutados |
| Escritura en `main` | No ejecutada |
| Operaciones destructivas | No ejecutadas |

Los cambios permanecen en el árbol de trabajo local. No se ha creado el PR #3.

## 3. Decisión D-02 aprobada por el propietario

| Aspecto | Decisión aplicada |
| --- | --- |
| Catálogo | Un único plan válido: `standard`. |
| Obligatoriedad | `plan` es obligatorio. |
| Valor por defecto | No existe; el cliente debe enviar el plan. |
| Valores aceptados | Exactamente `standard`. |
| Otros valores | Se rechazan con `422`. |
| Precios y prestaciones | No existen precios ni prestaciones adicionales asociados al plan. |
| Tramos de usuarios | El plan no modifica los tramos progresivos de precio por número de usuarios. |
| Planes futuros | No se introducirán otros planes sin una decisión posterior. |

La validación se centraliza en `PlanCode.parse()` en dominio. `application/customers/catalogs.py` reexporta `CountryCode` y `PlanCode` para que presentación use la misma fuente de verdad sin importar `domain`. La persistencia guarda el valor `standard` y no se crea una tabla de planes para un catálogo fijo de un único valor.

## 4. Contrato definitivo de `POST /customers`

### 4.1 Petición

```json
{
  "legal_name": "Empresa Ejemplo S.L.",
  "tax_id": "B12345674",
  "email": "contacto@ejemplo.es",
  "country": "ES",
  "plan": "standard"
}
```

`B12345674` es un identificador ficticio de prueba, sintáctica y algorítmicamente válido.

### 4.2 Respuesta de éxito

- Código `201 Created`.
- `Content-Type: application/json`.
- Campos: `id`, `legal_name`, `tax_id`, `email`, `country`, `plan`, `created_at`.
- UUID generado por el servidor.
- Identificador fiscal normalizado.
- `created_at` en UTC.
- Sin cabecera `Location`.

### 4.3 Errores

| Caso | Código | Formato |
| --- | --- | --- |
| Campos ausentes, email inválido, DNI/NIF/NIE/CIF inválido, país distinto de `ES`, plan distinto de `standard`, JSON malformado | `422` | `application/problem+json` |
| Identificador fiscal duplicado en el mismo país | `409` | `application/problem+json` |
| Error interno no controlado | `500` | `application/problem+json` sin detalles internos |

OpenAPI documenta la ruta, `CustomerCreateRequest`, `CustomerResponse`, `ProblemDetails`, `ProblemFieldError` y las respuestas `201`, `409`, `422` y `500`.

## 5. Componentes implementados

### 5.1 Dominio

- `PlanCode.STANDARD = "standard"` y `PlanCode.parse()`.
- `CountryCode.parse()`.
- `InvalidPlan`.
- `Customer.plan` tipado como `PlanCode`.
- Validación fiscal existente de DNI/NIF, NIE y CIF/NIF preservada.

### 5.2 Aplicación

- `application/customers/catalogs.py` como reexportación de los catálogos de dominio.
- `CustomerResult` con `CountryCode` y `PlanCode`.
- `CreateCustomer` valida país y plan, normaliza el identificador fiscal, genera UUID y `created_at`, comprueba duplicados y persiste.
- `InvalidCustomerData` para plan inválido.

### 5.3 Infraestructura

- `CustomerModel` alineado con la migración: longitudes explícitas, campos no nulos y restricción única `(country, tax_id)`.
- Mapeadores con `PlanCode.parse()` al leer y `plan.value` al escribir.
- Migración `0001_create_customers`.
- `alembic.ini` con `path_separator = os`.

### 5.4 Presentación

- `CustomerCreateRequest` y `CustomerResponse` usan `CountryCode` y `PlanCode` reexportados desde aplicación.
- `presentation/customers/dependencies.py` define la dependencia sustituible del caso de uso.
- `presentation/customers/router.py` registra `POST /customers` con `201`, respuestas `problem+json` y sin `Location`.
- `presentation/app.py` incluye el router de clientes.

### 5.5 Composition root

- `bootstrap/main.py` crea la fábrica de sesiones de forma perezosa.
- Sustituye `get_create_customer_use_case` por una sesión SQLAlchemy por petición.
- `bootstrap/customers.py` construye `CreateCustomer` con el repositorio SQLAlchemy.
- Importar la aplicación no crea `backend/var` ni una base SQLite.

## 6. Migración Alembic

Revisión creada:

```text
backend/migrations/versions/0001_create_customers.py
```

Esquema:

- `id`: UUID compatible con SQLite, clave primaria.
- `legal_name`, `tax_id`, `email`, `country`, `plan`, `created_at`: no nulos.
- `created_at`: `DateTime(timezone=True)`.
- Restricción única `uq_customers_country_tax_id` sobre `(country, tax_id)`.
- `downgrade()` elimina `customers`.

Resultados reales del ciclo CLI sobre una SQLite temporal aislada:

| Comprobación | Resultado |
| --- | --- |
| `alembic heads` | `0001_create_customers (head)` |
| `alembic upgrade head` desde base vacía | Exit 0; revisión aplicada |
| `alembic current` | `0001_create_customers (head)` |
| `alembic downgrade base` | Exit 0; tabla eliminada |
| Nueva `alembic upgrade head` | Exit 0 |
| `alembic current` final | `0001_create_customers (head)` |

La prueba automatizada de migración verifica además tabla, columnas, nulabilidad, restricción única, persistencia, rechazo de duplicados y ciclo completo de downgrade/upgrade. No se usa `create_all()` como sustituto de Alembic.

## 7. Pruebas ejecutadas

| Comprobación | Resultado real |
| --- | --- |
| `python -m pytest` | **73 pruebas superadas** en 2,14 s |
| `python -m ruff check .` | Sin hallazgos |
| `python -m ruff format --check .` | 44 archivos ya formateados |
| `python -m mypy .` | Sin incidencias en 42 archivos fuente |
| `python -m pip check` | Sin dependencias rotas |

Cobertura funcional añadida:

- Dominio: plan `standard`, plan desconocido, plan vacío y normalización fiscal.
- Aplicación: creación, UUID de servidor, unicidad, errores y límites transaccionales.
- Infraestructura: SQLite temporal, restricción única, integridad de campos y migración.
- API: `201`, persistencia, campos, `409`, `422` por cada campo ausente, email inválido, DNI/NIF/NIE/CIF inválido, país inválido, plan inválido, JSON malformado, `500` sin detalles internos, OpenAPI y `/health`.

## 8. Comprobaciones HTTP

Ejecutadas contra `bootstrap.main.app` con una SQLite temporal migrada y la dependencia del caso de uso sustituida para la prueba:

| Petición | Resultado |
| --- | --- |
| `GET /health` | `200`; `{"status":"ok"}` |
| `GET /openapi.json` | `200`; OpenAPI `3.1.0` |
| `POST /customers` válido | `201`; `application/json`; sin `Location` |
| `POST /customers` duplicado | `409`; `application/problem+json` |
| `POST /customers` sin `plan` | `422`; `application/problem+json` |
| `POST /customers` con JSON malformado | `422`; `application/problem+json` |
| Persistencia | Cliente encontrado en SQLite con `plan = standard` |
| OpenAPI `/customers` | Respuestas `201`, `409`, `422`, `500`; `problem+json` en `409`, `422` y `500` |

## 9. Entorno virtual y dependencias

| Comprobación | Resultado |
| --- | --- |
| Intérprete | Python 3.13.17 desde `backend/.venv/Scripts/python.exe` |
| `sys.prefix` | `backend\.venv` |
| `sys.base_prefix` | Python 3.13 global |
| Aislamiento | `sys.prefix != sys.base_prefix`; `ENABLE_USER_SITE=False` |
| Lock frente a `pip freeze` | 35/35 coinciden; 0 diferencias |
| Nuevas dependencias | Ninguna |
| `pyproject.toml` y `requirements.lock` | Sin cambios de TASK020; se preservan los de TASK019 |

## 10. Arquitectura y exclusiones

- `domain` no importa FastAPI, Pydantic ni SQLAlchemy.
- `presentation` no importa `domain` ni `infrastructure`; usa los catálogos reexportados por aplicación.
- `infrastructure` implementa el puerto de dominio y no es importada por las capas superiores.
- `bootstrap` actúa como composition root.
- `tests/test_architecture.py` pasa dentro de la suite.
- `.venv`, `TASKS.zip`, cachés y bases SQLite no aparecen en el estado de Git.
- `LICENSE` no se ha modificado.
- No se han versionado archivos `.sqlite`, `.db` ni auxiliares.

## 11. Archivos creados y modificados

### 11.1 Creados en TASK020

- `backend/migrations/versions/0001_create_customers.py`
- `backend/src/saas_o_matic/application/customers/catalogs.py`
- `backend/src/saas_o_matic/presentation/customers/dependencies.py`
- `backend/src/saas_o_matic/presentation/customers/router.py`
- `backend/tests/conftest.py`
- `backend/tests/test_customer_api.py`
- `backend/tests/test_migrations.py`
- `ai-workspace/01-tasks/TASK020-customer-registration-completion.md`

### 11.2 Modificados en TASK020

- `backend/src/saas_o_matic/domain/customers/__init__.py`
- `backend/src/saas_o_matic/domain/customers/entities.py`
- `backend/src/saas_o_matic/domain/customers/errors.py`
- `backend/src/saas_o_matic/domain/customers/value_objects.py`
- `backend/src/saas_o_matic/application/customers/dto.py`
- `backend/src/saas_o_matic/application/customers/use_cases.py`
- `backend/src/saas_o_matic/infrastructure/customers/mappers.py`
- `backend/src/saas_o_matic/infrastructure/customers/models.py`
- `backend/src/saas_o_matic/presentation/customers/schemas.py`
- `backend/src/saas_o_matic/presentation/app.py`
- `backend/src/saas_o_matic/presentation/problems.py`
- `backend/src/saas_o_matic/bootstrap/main.py`
- `backend/src/saas_o_matic/bootstrap/customers.py`
- `backend/alembic.ini`
- `backend/migrations/versions/README.md`
- `backend/tests/test_customer_repository.py`
- `backend/tests/test_customer_schemas.py`
- `backend/tests/test_customer_use_case.py`
- `backend/tests/test_health.py`
- `docs/requirements/functional-requirements.md`
- `docs/specs/001-customer-registration/spec.md`
- `docs/specs/001-customer-registration/plan.md`
- `docs/specs/001-customer-registration/tasks.md`
- `README.md`
- `backend/README.md`
- `ai-workspace/README.md`
- `ai-workspace/00-project-context/architectural-evolution.md`
- `ai-workspace/00-project-context/ai-tools-and-roles.md`

### 11.3 Inventario completo para el futuro PR #3

El PR #3 incluiría, además de los archivos de TASK020, los cambios todavía no publicados de TASK018 y TASK019:

**Modificados**

- `README.md`
- `ai-workspace/00-project-context/ai-tools-and-roles.md`
- `ai-workspace/00-project-context/architectural-evolution.md`
- `ai-workspace/README.md`
- `backend/README.md`
- `backend/pyproject.toml`
- `backend/requirements.lock`
- `backend/src/saas_o_matic/bootstrap/main.py`
- `backend/src/saas_o_matic/presentation/app.py`
- `backend/tests/test_health.py`
- `docs/requirements/functional-requirements.md`

**Nuevos**

- `ai-workspace/01-tasks/TASK017-backend-publication.md`
- `ai-workspace/01-tasks/TASK018-customer-registration.md`
- `ai-workspace/01-tasks/TASK019-customer-implementation.md`
- `ai-workspace/01-tasks/TASK020-customer-registration-completion.md`
- `backend/alembic.ini`
- `backend/migrations/env.py`
- `backend/migrations/script.py.mako`
- `backend/migrations/versions/0001_create_customers.py`
- `backend/migrations/versions/README.md`
- `backend/src/saas_o_matic/application/customers/__init__.py`
- `backend/src/saas_o_matic/application/customers/catalogs.py`
- `backend/src/saas_o_matic/application/customers/dto.py`
- `backend/src/saas_o_matic/application/customers/errors.py`
- `backend/src/saas_o_matic/application/customers/use_cases.py`
- `backend/src/saas_o_matic/bootstrap/customers.py`
- `backend/src/saas_o_matic/domain/customers/__init__.py`
- `backend/src/saas_o_matic/domain/customers/entities.py`
- `backend/src/saas_o_matic/domain/customers/errors.py`
- `backend/src/saas_o_matic/domain/customers/ports.py`
- `backend/src/saas_o_matic/domain/customers/value_objects.py`
- `backend/src/saas_o_matic/infrastructure/customers/__init__.py`
- `backend/src/saas_o_matic/infrastructure/customers/mappers.py`
- `backend/src/saas_o_matic/infrastructure/customers/models.py`
- `backend/src/saas_o_matic/infrastructure/customers/repositories.py`
- `backend/src/saas_o_matic/infrastructure/database.py`
- `backend/src/saas_o_matic/presentation/customers/__init__.py`
- `backend/src/saas_o_matic/presentation/customers/dependencies.py`
- `backend/src/saas_o_matic/presentation/customers/router.py`
- `backend/src/saas_o_matic/presentation/customers/schemas.py`
- `backend/src/saas_o_matic/presentation/problems.py`
- `backend/tests/conftest.py`
- `backend/tests/test_customer_api.py`
- `backend/tests/test_customer_repository.py`
- `backend/tests/test_customer_schemas.py`
- `backend/tests/test_customer_use_case.py`
- `backend/tests/test_migrations.py`
- `backend/tests/test_problems.py`
- `backend/tests/test_spanish_tax_id.py`
- `docs/specs/001-customer-registration/plan.md`
- `docs/specs/001-customer-registration/spec.md`
- `docs/specs/001-customer-registration/tasks.md`

El inventario debe revisarse de nuevo antes de crear el PR #3. No se ha ejecutado `git add`.

## 12. Limitaciones y riesgos pendientes

- No hay frontend.
- No hay endpoints de listado, detalle, edición o eliminación.
- No se publica `Location` porque no existe endpoint de detalle aprobado.
- SQLite limita la concurrencia y no reproduce producción (P-05).
- La estructura global por capas puede no ser la frontera modular definitiva (P-06).
- El lock de dependencias no es estricto ni usa hashes.
- No hay CI configurada.
- No consta una revisión independiente humana de TASK020.
- Los cambios permanecen locales y no publicados.

## 13. Resultado y siguiente paso

- Resultado: alta de clientes MVP completada y validada localmente.
- D-02: aprobada y aplicada.
- Migración: `0001_create_customers` verificada en ciclo completo.
- Endpoint: `POST /customers` operativo con `201`, `409` y `422` controlados.
- Estado Git: cambios locales, sin staged, sin commit, sin push y sin PR.
- Siguiente paso: revisión del propietario y, si la autoriza, preparación del PR #3. El merge corresponde exclusivamente al propietario.

## 14. Referencias

- [SPEC-001](../../docs/specs/001-customer-registration/spec.md)
- [PLAN-001](../../docs/specs/001-customer-registration/plan.md)
- [TASKS-001](../../docs/specs/001-customer-registration/tasks.md)
- [Requisitos funcionales](../../docs/requirements/functional-requirements.md)
- [ADR 0002 - Arquitectura](../../docs/adr/0002-architecture.md)
- [TASK018 - Primera funcionalidad: alta de clientes](TASK018-customer-registration.md)
- [TASK019 - Implementación de clientes con decisiones aprobadas](TASK019-customer-implementation.md)
