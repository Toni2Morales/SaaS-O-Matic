# TASK019 - Implementación de clientes con decisiones aprobadas

| Campo | Valor |
| --- | --- |
| ID | TASK019 |
| Título | Implementación de clientes con decisiones aprobadas y catálogo de planes pendiente |
| Estado | **Parcial:** base técnica implementada; `POST /customers` y migración de `customers` bloqueados por D-02 |
| Fecha | 2026-11-15 |
| Rama | `feature/customer-registration` |
| Participantes | Propietario (instrucción y decisiones) / OpenCode + DeepSeek (implementación, pruebas y documentación) |
| Autorización Git | Modificar archivos, crear código/pruebas/documentación, actualizar dependencias en `.venv` y ejecutar validaciones; `git add`, `git commit`, `git push`, PR y merge no autorizados |

## 1. Objetivo y alcance

Implementar la base funcional de clientes con las decisiones aprobadas tras TASK018, sin inventar el catálogo de planes ni presentar el alta como terminada.

La tarea incluyó:

- Registrar D-01 y D-03 a D-14.
- Implementar dominio fiscal, entidad, puerto de repositorio, caso de uso, persistencia SQLAlchemy, configuración Alembic y esquemas HTTP.
- Mantener `POST /customers` sin registrar y sin devolver `201 Created`.
- No crear una migración de `customers` que omita `plan`.
- Añadir pruebas proporcionales y ejecutar las validaciones del repositorio.

D-02 (catálogo de planes) sigue pendiente y es la única decisión de negocio que bloquea el contrato definitivo del alta.

## 2. Estado Git inicial y final

### 2.1 Estado inicial

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/customer-registration` |
| HEAD | `be755a68a52392fd562eb3901e317bc85b1ed8e9` |
| `origin/main` tras `git fetch origin` | `be755a68a52392fd562eb3901e317bc85b1ed8e9` |
| Relación `HEAD...origin/main` | `0 0` |
| Archivos modificados de TASK018 | 4 |
| Archivos nuevos de TASK018 | 5 |
| Archivos preparados para commit | Ninguno |
| Cambios de TASK018 | Preservados |

### 2.2 Estado final

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/customer-registration` |
| HEAD | `be755a68a52392fd562eb3901e317bc85b1ed8e9` |
| Archivos preparados para commit | Ninguno |
| `LICENSE` | Sin cambios |
| `TASKS.zip`, `.venv`, cachés y bases SQLite | Excluidos y no versionados |
| `git diff --check` | Sin errores |

No se ejecutaron `git add`, `git commit`, `git push`, creación de PR, merge, escritura en `main` ni comandos destructivos.

## 3. Decisiones aplicadas

| ID | Decisión aplicada |
| --- | --- |
| D-01 | Códigos ISO 3166-1 alfa-2; solo `ES`; sin validadores fiscales internacionales. |
| D-02 | Catálogo de planes pendiente; sin catálogo provisional, sin plan por defecto y sin eliminar `plan` del contrato. |
| D-03 | DNI/NIF, NIE y CIF/NIF con formato y carácter de control. |
| D-04 | `email` obligatorio y validado con Pydantic `EmailStr`; `email-validator==2.4.0` autorizado e instalado. |
| D-05 | NIF normalizado único por país; restricción única `(country, tax_id)` y traducción de conflictos. |
| D-06 | Sin unicidad de razón social. |
| D-07 | Eliminación de espacios y guiones, mayúsculas, validación posterior y persistencia normalizada. |
| D-08 | Los cinco campos de FR-01 son obligatorios. |
| D-09 | `201 Created` con representación y sin `Location`; pendiente de endpoint. |
| D-10 | UUID generado por el servidor; la petición no incluye `id`. |
| D-11 | `application/problem+json` para validación, conflicto y error interno; esquema en OpenAPI. |
| D-12 | Ruta `POST /customers`; sin `/api/v1`. |
| D-13 | Una transacción por caso de uso; commit en infraestructura; dominio y aplicación sin SQLAlchemy. |
| D-14 | `created_at` en UTC; sin `updated_at`. |

## 4. Componentes implementados

### 4.1 Dominio

- `CountryCode` con `ES`.
- `TaxIdKind` con `DNI`, `NIE` y `CIF`.
- `SpanishTaxId` con normalización y validación de DNI/NIF, NIE y CIF/NIF.
- `Customer` con UUID, razón social, NIF normalizado, email, país, plan y `created_at`.
- `CustomerRepository` como puerto de persistencia.
- Errores `InvalidTaxId`, `InvalidCountry` y `DuplicateCustomerTaxId`.

`plan` se almacena como cadena opaca, sin valor por defecto y sin validación de catálogo.

### 4.2 Aplicación

- `CreateCustomerCommand` y `CustomerResult`.
- `CreateCustomer` con normalización fiscal, validación de país, comprobación previa de duplicados, generación de UUID, `created_at` UTC y persistencia.
- Errores `InvalidCustomerData` y `CustomerTaxIdAlreadyExists`.
- Traducción de duplicados detectados por persistencia.
- Caso de uso preparado, no inyectado en ningún endpoint.

### 4.3 Infraestructura

- `Base`, `create_sqlite_engine` y `create_session_factory`.
- `CustomerModel` con `plan` no nulo y restricción única `(country, tax_id)`.
- Mapeadores `to_domain` y `to_model`.
- `SqlAlchemyCustomerRepository` con comprobación de existencia, persistencia y traducción de conflictos.
- Configuración Alembic en `alembic.ini` y `migrations/`.
- `migrations/versions/README.md` documenta la ausencia deliberada de migración de `customers`.

### 4.4 Presentación

- `CustomerCreateRequest` con los cinco campos obligatorios, `EmailStr` y `country="ES"`.
- `CustomerResponse` con UUID, campos del cliente y `created_at`.
- `ProblemDetails` y `ProblemFieldError`.
- Manejadores `application/problem+json` para errores de esquema, validación de dominio, conflicto y 500.
- `ProblemDetails` publicado en componentes OpenAPI.
- Sin router ni endpoint `POST /customers`.

### 4.5 Composition root

- `build_customer_use_case(session)` en `bootstrap/customers.py`.
- No se invoca desde `bootstrap/main.py`.
- `/health` y `/openapi.json` siguen disponibles.

## 5. Componentes bloqueados por D-02

- Catálogo de planes.
- Validación de valores de `plan`.
- Representación definitiva de `plan`.
- Migración inicial de `customers`.
- Router y endpoint `POST /customers`.
- Respuesta `201 Created` en ejecución.
- Pruebas HTTP de alta completa.
- Documentación de la operación de alta en OpenAPI.

No se ha creado un flujo alternativo de alta incompleta ni se ha asignado un plan por defecto.

## 6. Archivos creados y modificados

### 6.1 Creados

- `backend/src/saas_o_matic/domain/customers/__init__.py`
- `backend/src/saas_o_matic/domain/customers/entities.py`
- `backend/src/saas_o_matic/domain/customers/errors.py`
- `backend/src/saas_o_matic/domain/customers/ports.py`
- `backend/src/saas_o_matic/domain/customers/value_objects.py`
- `backend/src/saas_o_matic/application/customers/__init__.py`
- `backend/src/saas_o_matic/application/customers/dto.py`
- `backend/src/saas_o_matic/application/customers/errors.py`
- `backend/src/saas_o_matic/application/customers/use_cases.py`
- `backend/src/saas_o_matic/infrastructure/database.py`
- `backend/src/saas_o_matic/infrastructure/customers/__init__.py`
- `backend/src/saas_o_matic/infrastructure/customers/mappers.py`
- `backend/src/saas_o_matic/infrastructure/customers/models.py`
- `backend/src/saas_o_matic/infrastructure/customers/repositories.py`
- `backend/src/saas_o_matic/presentation/customers/__init__.py`
- `backend/src/saas_o_matic/presentation/customers/schemas.py`
- `backend/src/saas_o_matic/presentation/problems.py`
- `backend/src/saas_o_matic/bootstrap/customers.py`
- `backend/alembic.ini`
- `backend/migrations/env.py`
- `backend/migrations/script.py.mako`
- `backend/migrations/versions/README.md`
- `backend/tests/test_customer_repository.py`
- `backend/tests/test_customer_schemas.py`
- `backend/tests/test_customer_use_case.py`
- `backend/tests/test_problems.py`
- `backend/tests/test_spanish_tax_id.py`
- `ai-workspace/01-tasks/TASK019-customer-implementation.md`

### 6.2 Modificados

- `backend/pyproject.toml`: `email-validator==2.4.0`.
- `backend/requirements.lock`: `dnspython==2.9.2` y `email-validator==2.4.0`.
- `backend/src/saas_o_matic/presentation/app.py`: manejadores de problema y esquema OpenAPI.
- `backend/tests/test_health.py`: ausencia de `/customers`, 404 del alta y `ProblemDetails` en OpenAPI.
- `backend/README.md`: estado, estructura, Alembic, dependencias y alcance.
- `README.md`: estado del proyecto y enlace a la especificación.
- `docs/specs/001-customer-registration/spec.md`: decisiones y estado.
- `docs/specs/001-customer-registration/plan.md`: componentes implementados, preparados y pendientes.
- `docs/specs/001-customer-registration/tasks.md`: tareas completadas y bloqueadas.
- `ai-workspace/README.md`: TASK019, índice y limitaciones.
- `ai-workspace/00-project-context/architectural-evolution.md`: fase 6, estado actual y P-07/P-09.

Se preservaron los cambios de TASK018. No se modificaron `LICENSE`, `TASKS.zip`, `.venv`, bases SQLite locales ni cachés.

## 7. Dependencias y entorno

| Comprobación | Resultado |
| --- | --- |
| Intérprete | Python 3.13.17 desde `backend/.venv/Scripts/python.exe` |
| Aislamiento | `sys.prefix != sys.base_prefix`; `ENABLE_USER_SITE=False` |
| `email-validator` | 2.4.0 |
| `dnspython` | 2.9.2 |
| `idna` | 3.20, ya instalada |
| `pip check` | Sin dependencias rotas |
| Lock frente a `pip freeze` | 35/35; 0 diferencias |

No se instalaron paquetes globalmente ni se incorporaron gestores de dependencias adicionales.

## 8. Validaciones ejecutadas

| Comprobación | Resultado |
| --- | --- |
| `python -m pytest` | 50 pruebas superadas |
| `python -m ruff check .` | Sin hallazgos |
| `python -m ruff format --check .` | 37 archivos ya formateados |
| `python -m mypy .` | Sin incidencias en 35 archivos fuente |
| `python -m pip check` | Sin dependencias rotas |
| `GET /health` | HTTP 200; `{"status":"ok"}` |
| `GET /openapi.json` | HTTP 200; OpenAPI 3.1.0; `/health` presente; `ProblemDetails` y `ProblemFieldError` presentes |
| `POST /customers` | HTTP 404; no registrado |
| `/customers` en OpenAPI | Ausente |
| `python -m alembic heads` | Sin revisiones |
| `python -m alembic upgrade head` con SQLite temporal | Exit 0; sin migraciones |
| `python -m alembic current` con SQLite temporal | Sin revisión aplicada |
| Revisión de `customers` | No creada; bloqueada por D-02 |
| Bases SQLite de desarrollo | No se creó ninguna |
| Archivos SQLite versionados | Ninguno |
| `TASKS.zip`, `.venv` y cachés | Excluidos y no versionados |
| `git diff --check` | Sin errores |

## 9. Limitaciones y riesgos

- D-02 sigue pendiente; el catálogo de planes y su validación no están definidos.
- `plan` es una cadena opaca de preparación, no un contrato definitivo.
- No existe migración de `customers`.
- No existe endpoint `POST /customers` ni respuesta `201 Created`.
- La operación de alta no está documentada en OpenAPI; solo se publica el esquema de problema.
- SQLite limita la concurrencia y no reproduce producción (P-05).
- La estructura global por capas puede no ser la frontera modular definitiva (P-06).
- El lock de dependencias no es estricto ni usa hashes.
- No hay CI configurada.
- No consta revisión independiente humana de esta implementación.

## 10. Autorizaciones Git

Se autorizaron la modificación de archivos, la creación de código, pruebas y documentación, la actualización de dependencias dentro de `backend/.venv` y la ejecución de validaciones.

No se autorizaron `git add`, `git commit`, `git push`, creación de PR ni merge. No se escribió en `main` ni se ejecutaron comandos destructivos.

## 11. Resultado y siguiente paso

- Resultado: base técnica de clientes implementada y probada; decisiones registradas; endpoint y migración documentados como pendientes.
- Estado: parcial; no se publican cambios.
- Siguiente paso: el propietario debe aprobar el catálogo de planes y su semántica de validación. Después se podrá definir la representación definitiva de `plan`, crear la migración de `customers`, registrar `POST /customers`, devolver `201 Created` y añadir las pruebas HTTP y de migración.

## 12. Referencias

- [SPEC-001](../../docs/specs/001-customer-registration/spec.md)
- [PLAN-001](../../docs/specs/001-customer-registration/plan.md)
- [TASKS-001](../../docs/specs/001-customer-registration/tasks.md)
- [TASK018 - Primera funcionalidad: alta de clientes](TASK018-customer-registration.md)
- [Requisitos funcionales](../../docs/requirements/functional-requirements.md)
- [ADR 0002 - Arquitectura](../../docs/adr/0002-architecture.md)
