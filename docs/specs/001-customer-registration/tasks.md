# Tareas 001 - Alta de clientes

| Campo | Valor |
| --- | --- |
| ID | TASKS-001 |
| Título | Desglose de implementación de `POST /customers` |
| Estado | **Implementado; validación de `legal_name` corregida en TASK022. Cambios locales no publicados** |
| Fecha | 2026-11-16 |

## 1. Regla de alcance

Las decisiones D-01 a D-15 están aprobadas. D-02 se aprobó en TASK020 con un catálogo MVP de un único plan, `standard`; D-15 se aprobó en TASK022 para la normalización y validación de `legal_name`.

No se crea un catálogo provisional, no se asigna un plan por defecto, no se añaden precios o prestaciones al plan y no se introducen otros planes sin una decisión posterior.

## 2. Tareas completadas en TASK018

- [x] Comprobar el estado de Git y confirmar el punto de partida.
- [x] Verificar que el PR #2 está fusionado.
- [x] Confirmar el commit de merge `be755a68a52392fd562eb3901e317bc85b1ed8e9`.
- [x] Ejecutar `git fetch origin` y confirmar `origin/main`.
- [x] Crear `feature/customer-registration` desde `origin/main`.
- [x] Registrar TASK017 y actualizar el índice de tareas.
- [x] Revisar requisitos, ADRs, assessment, README y contexto de `ai-workspace/`.
- [x] Crear `spec.md`, `plan.md` y `tasks.md`.
- [x] Documentar la propuesta inicial de contrato y sus alternativas.
- [x] Ejecutar las validaciones de referencia del scaffold.
- [x] Crear el registro TASK018.

## 3. Decisiones

- [x] D-01: países ISO 3166-1 alfa-2; solo `ES`; sin validadores internacionales.
- [x] D-02: catálogo MVP con un único plan, `standard`; obligatorio, sin valor por defecto y sin otros valores.
- [x] D-03: DNI/NIF, NIE y CIF/NIF con formato y control.
- [x] D-04: email obligatorio con `EmailStr` y `email-validator`.
- [x] D-05: unicidad fiscal normalizada por país y restricción de base de datos.
- [x] D-06: sin unicidad de razón social.
- [x] D-07: normalización de espacios, guiones y mayúsculas antes de validar.
- [x] D-08: los cinco campos de FR-01 son obligatorios.
- [x] D-09: `201 Created` con representación y sin `Location`.
- [x] D-10: UUID generado por el servidor.
- [x] D-11: `application/problem+json`, validación, conflicto y error interno.
- [x] D-12: ruta `POST /customers`, sin `/api/v1`.
- [x] D-13: una transacción por caso de uso y commit en infraestructura.
- [x] D-14: `created_at` en UTC, sin `updated_at`.
- [x] D-15: `legal_name` obligatorio, recortado, entre 1 y 255 caracteres tras el recorte, con espacios interiores conservados y valor normalizado persistido y devuelto.

## 4. Tareas completadas en TASK019

### 4.1 Dominio

- [x] Crear `Customer` con UUID, razón social, NIF normalizado, email, país, plan y `created_at`.
- [x] Crear `CountryCode` con `ES`.
- [x] Implementar normalización de identificadores fiscales.
- [x] Implementar DNI/NIF, NIE y CIF/NIF con carácter de control.
- [x] Definir `InvalidTaxId`, `InvalidCountry` y `DuplicateCustomerTaxId`.
- [x] Definir el puerto `CustomerRepository`.
- [x] Añadir pruebas de los tres tipos de identificador, normalización, entradas vacías y controles incorrectos.

### 4.2 Aplicación

- [x] Crear `CreateCustomerCommand` y `CustomerResult`.
- [x] Implementar `CreateCustomer`.
- [x] Comprobar duplicados antes de persistir.
- [x] Traducir duplicados de persistencia a `CustomerTaxIdAlreadyExists`.
- [x] Definir `InvalidCustomerData` y `CustomerTaxIdAlreadyExists`.
- [x] Añadir pruebas con repositorio falso.

### 4.3 Infraestructura

- [x] Configurar SQLAlchemy 2 y SQLite.
- [x] Crear `CustomerModel` con los campos aprobados.
- [x] Marcar `plan` como no nulo y sin valor por defecto.
- [x] Crear la restricción única `(country, tax_id)`.
- [x] Crear el mapeador entre entidad y modelo.
- [x] Implementar `SqlAlchemyCustomerRepository`.
- [x] Traducir conflictos de unicidad sin exponer SQLAlchemy.
- [x] Configurar la fábrica de sesiones.
- [x] Crear la configuración inicial de Alembic.
- [x] Probar el repositorio contra SQLite temporal.

### 4.4 Presentación

- [x] Crear `CustomerCreateRequest` con los cinco campos obligatorios.
- [x] Validar email con `EmailStr`.
- [x] Restringir `country` a `ES`.
- [x] Crear `CustomerResponse` con UUID y `created_at`.
- [x] Implementar `ProblemDetails` y `ProblemFieldError`.
- [x] Implementar manejadores `application/problem+json` para 422, 409 y 500.
- [x] Publicar `ProblemDetails` en los componentes OpenAPI.
- [x] Verificar que `presentation` no importa `domain` ni `infrastructure`.

### 4.5 Composition root

- [x] Preparar `build_customer_use_case(session)` en `bootstrap/customers.py`.
- [x] Mantener `GET /health` y `/openapi.json`.
- [x] Confirmar que ninguna capa importa `bootstrap`.

### 4.6 Documentación y dependencias

- [x] Registrar las decisiones aprobadas en `spec.md`, `plan.md` y `tasks.md`.
- [x] Añadir `email-validator==2.4.0` a `pyproject.toml`.
- [x] Actualizar `requirements.lock` con `email-validator==2.4.0` y `dnspython==2.9.2`.
- [x] Instalar la dependencia exclusivamente en `backend/.venv`.
- [x] Crear el registro TASK019 y actualizar el índice de `ai-workspace/`.

## 5. Tareas completadas en TASK020

### 5.1 Decisión y catálogo

- [x] Registrar D-02 en requisitos, especificación, plan y decisiones.
- [x] Añadir `PlanCode.STANDARD` como único valor del catálogo.
- [x] Centralizar la validación en `PlanCode.parse()` y `CountryCode.parse()`.
- [x] Reexportar los catálogos desde aplicación para presentación.
- [x] Eliminar la cadena opaca de `plan` en dominio, aplicación, persistencia y presentación.
- [x] Rechazar planes ausentes, vacíos o distintos de `standard` sin valor por defecto.
- [x] No crear una tabla de planes para un catálogo fijo de un único valor.

### 5.2 Migración y persistencia

- [x] Crear la revisión `0001_create_customers`.
- [x] Incluir UUID compatible con SQLite, campos funcionales no nulos, `created_at` UTC y restricción única `(country, tax_id)`.
- [x] Alinear el modelo SQLAlchemy y la migración.
- [x] Probar `upgrade head` desde una base vacía.
- [x] Verificar tabla, columnas, nulabilidad y restricción única.
- [x] Persistir un cliente y rechazar un duplicado.
- [x] Verificar la revisión actual.
- [x] Ejecutar `downgrade base` y una nueva `upgrade head`.
- [x] Sustituir `create_all()` por Alembic en las pruebas de persistencia.

### 5.3 API y composition root

- [x] Crear `presentation/customers/router.py`.
- [x] Registrar `POST /customers` mediante `create_app()` y el composition root.
- [x] Inyectar una sesión SQLAlchemy por petición.
- [x] Devolver `201 Created` con la representación persistida.
- [x] Generar UUID en el servidor, normalizar el identificador fiscal y devolver `created_at` UTC.
- [x] No añadir cabecera `Location`.
- [x] Documentar `201`, `409`, `422` y `500` en OpenAPI con `application/problem+json`.
- [x] Mantener `/health` y `/openapi.json`.

### 5.4 Pruebas

- [x] Cubrir plan `standard`, plan desconocido y plan ausente.
- [x] Cubrir creación, UUID, unicidad fiscal y errores de aplicación.
- [x] Cubrir persistencia real con SQLite temporal y restricción única.
- [x] Cubrir migración, esquema y downgrade/upgrade.
- [x] Cubrir `POST /customers` con `201`, persistencia, campos y ausencia de `Location`.
- [x] Cubrir errores `422` por cada campo ausente.
- [x] Cubrir email inválido, DNI/NIF inválido, NIE inválido y CIF/NIF inválido.
- [x] Cubrir país distinto de `ES`, plan distinto de `standard`, duplicado y JSON malformado.
- [x] Cubrir `application/problem+json` y `500` sin detalles internos.
- [x] Cubrir OpenAPI y `/health`.

### 5.5 Documentación

- [x] Actualizar `README.md`, `backend/README.md` y el índice de `ai-workspace/`.
- [x] Actualizar el contexto de evolución arquitectónica y herramientas de IA.
- [x] Crear `ai-workspace/01-tasks/TASK020-customer-registration-completion.md`.
- [x] No reescribir los registros históricos de TASK018 y TASK019.

### 5.6 Corrección y regresión de TASK022

- [x] Aplicar D-15 en dominio, aplicación y esquema Pydantic.
- [x] Centralizar los límites y la normalización de `legal_name` en el dominio.
- [x] Documentar los límites 1–255 en OpenAPI.
- [x] Añadir pruebas de vacío, solo espacios, 1, 255 y 256 caracteres, recorte, persistencia normalizada, duplicado fiscal normalizado, misma razón social con distinto identificador, NIE con Y/Z y CIF con K.
- [x] Verificar que los valores inválidos devuelven errores controlados y no se persisten.
- [x] Crear `ai-workspace/01-tasks/TASK022-customer-validation-fix.md`.
- [x] Mantener m-01 a m-04 de TASK021 como observaciones pendientes.

## 6. Validaciones

- [x] `python -m pytest`.
- [x] `python -m ruff check .`.
- [x] `python -m ruff format --check .`.
- [x] `python -m mypy .`.
- [x] `python -m pip check`.
- [x] Verificar `/health` y `/openapi.json`.
- [x] Verificar `POST /customers` con `201`, `409` y `422`.
- [x] Verificar migración Alembic desde base vacía, `current`, `downgrade base` y nueva `upgrade head`.
- [x] Verificar que no se han creado bases SQLite versionables.
- [x] Verificar que `.venv`, cachés y `TASKS.zip` permanecen excluidos.
- [x] Ejecutar `git diff --check`.

Los resultados reales se registran en [TASK020](../../../ai-workspace/01-tasks/TASK020-customer-registration-completion.md) y en [TASK022](../../../ai-workspace/01-tasks/TASK022-customer-validation-fix.md).

## 7. Criterio de finalización

La funcionalidad se considera terminada cuando:

1. D-02 está aprobada por el propietario. **Cumplido.**
2. El plan tiene una representación y validación definitivas. **Cumplido.**
3. La migración inicial de `customers` se ejecuta correctamente. **Cumplido.**
4. `POST /customers` está registrado y devuelve `201 Created`. **Cumplido.**
5. Las pruebas HTTP y de migración pasan con resultados reales. **Cumplido.**
6. Las validaciones de calidad y arquitectura pasan. **Cumplido.**
7. El propietario revisa el resultado y autoriza las operaciones Git que procedan. **Pendiente de revisión.**

## 8. Estado actual

El alta de clientes está implementada y validada localmente. Los cambios de TASK020 y la corrección de TASK022 permanecen sin `git add`, sin commit, sin push y sin PR. El siguiente paso es la revisión del propietario y la eventual preparación del PR #3. El merge corresponde exclusivamente al propietario.
