# Especificación 001 - Alta de clientes

| Campo | Valor |
| --- | --- |
| ID | SPEC-001 |
| Título | Alta de clientes mediante `POST /customers` |
| Estado | **Implementada; validación de `legal_name` corregida en TASK022. Cambios locales no publicados.** |
| Fecha | 2026-11-16 |
| Rama | `feature/customer-registration` |
| Base | `origin/main` en `be755a68a52392fd562eb3901e317bc85b1ed8e9` |
| Alcance | Creación de clientes; no incluye búsqueda, detalle, simulaciones, autenticación ni facturación |

## 1. Fuentes

- [Requisitos funcionales](../../requirements/functional-requirements.md)
- [ADR 0001 - Stack tecnológico](../../adr/0001-technology-stack.md)
- [ADR 0002 - Arquitectura](../../adr/0002-architecture.md)
- [Evaluación inicial del repositorio](../../assessment/001-repository-assessment.md)
- [README raíz](../../../README.md)
- [Contexto de evolución arquitectónica](../../../ai-workspace/00-project-context/architectural-evolution.md)
- [Herramientas y roles de IA](../../../ai-workspace/00-project-context/ai-tools-and-roles.md)
- [TASK020 - Cierre del alta de clientes](../../../ai-workspace/01-tasks/TASK020-customer-registration-completion.md)
- [TASK022 - Corrección de `legal_name` y pruebas de regresión](../../../ai-workspace/01-tasks/TASK022-customer-validation-fix.md)

## 2. Objetivo y límites

Definir el comportamiento de `POST /customers` para dar de alta un cliente de SaaS-O-Matic.

Quedan fuera de esta especificación:

- Búsqueda y listado de clientes (FR-07).
- Detalle de cliente e historial (FR-08).
- Simulaciones, precios, impuestos y divisas.
- Autenticación, autorización y multi-tenancy.
- Stripe, frontend, PDF, correo y aprovisionamiento.
- Cualquier funcionalidad no incluida en el alcance aprobado.

## 3. Requisitos confirmados

### 3.1 Requisitos funcionales

| ID | Requisito | Consecuencia para esta especificación |
| --- | --- | --- |
| FR-01 | Crear clientes con razón social, identificador fiscal, email, país y plan seleccionado. | El alta contempla esos cinco datos y los cinco son obligatorios (D-08). |
| FR-02 | Validar identificadores fiscales españoles (DNI/NIF/CIF) mediante sus algoritmos de comprobación. | Se validan DNI/NIF, NIE y CIF/NIF de entidad (D-03). |
| FR-07 | Ofrecer un panel de clientes con búsqueda por razón social o identificador fiscal. | Fuera del alcance de esta tarea; no se implementa aquí. |
| FR-08 | Mostrar el detalle del cliente con tarjetas resumen e historial de simulaciones. | Fuera del alcance de esta tarea. |

### 3.2 Restricciones y decisiones técnicas confirmadas

| Fuente | Decisión confirmada |
| --- | --- |
| CON-01 / ADR 0001 | Backend en Python 3.13 con FastAPI, Pydantic v2, SQLAlchemy 2, SQLite y Alembic. |
| CON-08 | La API se documenta con OpenAPI. |
| CON-09 | El backend se valida con Pytest, HTTPX, Ruff y mypy. |
| ADR 0002 | Monolito modular con dependencias dirigidas hacia el dominio. |
| ADR 0002 | `domain` no importa FastAPI, Pydantic ni SQLAlchemy. |
| ADR 0002 | `presentation` no importa `domain`; los errores se traducen en `application` y luego a HTTP. |
| ADR 0002 | Los modelos SQLAlchemy y los esquemas Pydantic son independientes y se mapean explícitamente. |
| ADR 0002 | Ninguna capa importa `infrastructure`; el composition root inyecta los adaptadores. |
| ADR 0002 | El composition root sigue siendo provisional en `backend/src/saas_o_matic/bootstrap/`. |
| TASK018 | El endpoint solicitado es `POST /customers`. |

## 4. Decisiones aprobadas por el propietario

Las decisiones D-01 a D-15 quedan aprobadas. D-02 se aprobó expresamente en TASK020 y D-15 en TASK022.

| ID | Decisión aprobada |
| --- | --- |
| D-01 | Usar códigos ISO 3166-1 alfa-2. Admitir únicamente `ES` en esta primera versión. No implementar validadores fiscales internacionales. |
| D-02 | El catálogo de planes del MVP contiene únicamente `standard`. `plan` es obligatorio, no tiene valor por defecto, acepta exactamente `standard` y rechaza cualquier otro valor. No existen precios ni prestaciones adicionales asociados al plan. El plan no modifica los tramos progresivos de precio por número de usuarios. No se introducirán otros planes sin una decisión posterior. |
| D-03 | Admitir DNI/NIF, NIE y CIF/NIF de entidad españoles. Validar formato y carácter de control con sus algoritmos. Rechazar identificadores inválidos. |
| D-04 | `email` es obligatorio y se valida sintácticamente con Pydantic `EmailStr`. Se autoriza `email-validator` como dependencia explícita, manteniendo la estrategia de versiones existente. |
| D-05 | El identificador fiscal normalizado es único dentro de cada país. Aplicar una restricción de unicidad en la base de datos y traducir los conflictos sin exponer excepciones SQLAlchemy al cliente HTTP. |
| D-06 | La razón social no tiene unicidad. Se admiten clientes distintos con la misma razón social si sus identificadores fiscales difieren. |
| D-07 | Eliminar espacios y guiones del identificador fiscal, convertir a mayúsculas, validar después de normalizar y persistir el valor normalizado. |
| D-08 | Los cinco campos de FR-01 son obligatorios en el contrato definitivo: `legal_name`, `tax_id`, `email`, `country` y `plan`. No se crea silenciosamente un contrato de cuatro campos. |
| D-09 | El alta responde `201 Created` y devuelve la representación del cliente creado. No se incluye cabecera `Location` mientras no exista un endpoint de detalle aprobado. |
| D-10 | El identificador interno es un UUID generado por el servidor. El cliente HTTP no puede suministrarlo. |
| D-11 | Usar `application/problem+json` para errores controlados, distinguir validación, conflicto y error interno, no filtrar detalles de SQLAlchemy ni trazas y documentar el esquema en OpenAPI. |
| D-12 | La ruta es `POST /customers`. No se introduce `/api/v1` sin una decisión posterior. |
| D-13 | Una transacción por ejecución del caso de uso. Las operaciones de persistencia y el commit quedan en la frontera de infraestructura. Dominio y aplicación no importan SQLAlchemy. |
| D-14 | Incorporar `created_at` en UTC. No añadir `updated_at` sin necesidad funcional. |
| D-15 | `legal_name` es obligatorio. Eliminar espacios iniciales y finales con `strip()`; rechazar cadenas vacías o compuestas únicamente por espacios; aceptar entre 1 y 255 caracteres después del recorte; conservar los espacios interiores; persistir y devolver el valor normalizado. |

### 4.1 Representación del catálogo de planes

- `PlanCode` es un `StrEnum` de dominio con el único valor `STANDARD = "standard"`.
- `PlanCode.parse()` rechaza valores ausentes, vacíos o desconocidos y no aplica valores por defecto.
- La aplicación reexporta `CountryCode` y `PlanCode` mediante `application/customers/catalogs.py` para que presentación use la misma fuente de verdad sin importar `domain`.
- La persistencia guarda el valor `standard` como cadena y no crea una tabla de planes para un catálogo fijo de un único valor.
- El plan no altera los tramos progresivos de usuarios ni introduce precios o prestaciones.

## 5. Contrato HTTP definitivo

### 5.1 Ruta

```text
POST /customers
Content-Type: application/json
```

No se antepone `/api/v1` (D-12).

### 5.2 Petición

```json
{
  "legal_name": "Empresa Ejemplo S.L.",
  "tax_id": "B12345674",
  "email": "contacto@ejemplo.es",
  "country": "ES",
  "plan": "standard"
}
```

`B12345674` es un identificador ficticio de prueba, sintáctica y algorítmicamente válido. No identifica a una empresa real.

| Campo | Tipo | Obligatorio | Observación |
| --- | --- | --- | --- |
| `legal_name` | `string` | Sí | Se recorta; entre 1 y 255 caracteres tras el recorte; no puede quedar vacío; sin restricción de unicidad (D-06, D-15). |
| `tax_id` | `string` | Sí | Se normaliza y se valida como DNI/NIF, NIE o CIF/NIF (D-03, D-07). |
| `email` | `string` | Sí | Validación sintáctica con `EmailStr` (D-04). |
| `country` | `string` | Sí | Únicamente `ES` (D-01). |
| `plan` | `string` | Sí | Únicamente `standard` (D-02). |

La petición no incluye `id`: el servidor genera un UUID (D-10).

### 5.3 Respuesta de éxito

```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "legal_name": "Empresa Ejemplo S.L.",
  "tax_id": "B12345674",
  "email": "contacto@ejemplo.es",
  "country": "ES",
  "plan": "standard",
  "created_at": "2026-11-15T12:00:00Z"
}
```

| Aspecto | Decisión |
| --- | --- |
| Código de éxito | `201 Created` (D-09) |
| `Content-Type` | `application/json` |
| Cuerpo | Representación del cliente persistido (D-09) |
| Identificador | UUID generado por el servidor (D-10) |
| Identificador fiscal | Valor normalizado (D-07) |
| `created_at` | Fecha y hora en UTC (D-14) |
| `Location` | No se incluye (D-09) |

### 5.4 Errores

Los errores controlados usan `application/problem+json` (D-11).

| Caso | Código | Tratamiento |
| --- | --- | --- |
| JSON malformado, campos ausentes o tipos incorrectos | `422` | `ProblemDetails` con los errores de esquema de FastAPI/Pydantic. |
| Identificador fiscal inválido (DNI/NIF, NIE o CIF/NIF) | `422` | `ProblemDetails` con el campo afectado. |
| Email inválido | `422` | `ProblemDetails` con el error de validación de Pydantic. |
| Razón social vacía, solo con espacios o de más de 255 caracteres | `422` | `ProblemDetails` con el campo afectado. |
| País no soportado | `422` | `ProblemDetails` con el campo afectado. |
| Plan distinto de `standard` | `422` | `ProblemDetails` con el campo afectado. |
| Identificador fiscal duplicado en el mismo país | `409` | `ProblemDetails` de conflicto. |
| Error interno no controlado | `500` | `ProblemDetails` sin detalles internos ni trazas. |

El esquema `ProblemDetails` y las respuestas `201`, `409`, `422` y `500` se documentan en OpenAPI. La operación no añade endpoints de listado, edición o eliminación.

## 6. Estado de implementación

| Componente | Estado | Evidencia |
| --- | --- | --- |
| Validación fiscal española | Implementada | `SpanishTaxId`, `TaxIdKind` y pruebas de DNI, NIE y CIF. |
| Normalización fiscal | Implementada | Se eliminan espacios y guiones, se aplica mayúsculas y se valida después. |
| País | Implementado | `CountryCode` admite únicamente `ES`. |
| Catálogo de planes | Implementado | `PlanCode.STANDARD`; `PlanCode.parse()` rechaza valores desconocidos. |
| Entidad de cliente | Implementada | UUID, razón social normalizada, NIF normalizado, email, país, `PlanCode` y `created_at`. |
| Puerto de repositorio | Implementado | Comprobación de unicidad y persistencia. |
| Caso de uso de alta | Implementado | `CreateCustomer` valida razón social, país y plan, genera UUID y `created_at`, y persiste. |
| Modelo SQLAlchemy | Implementado | `CustomerModel` con `plan` obligatorio y restricción única `(country, tax_id)`. |
| Repositorio SQLAlchemy | Implementado | Traduce conflictos de unicidad a errores de dominio. |
| Migración Alembic | Implementada | Revisión `0001_create_customers`. |
| Esquemas Pydantic | Implementados | Entrada con los cinco campos, `legal_name` con límites 1–255, `EmailStr`, `CountryCode` y `PlanCode`; respuesta con `created_at`. |
| Errores HTTP | Implementados | `application/problem+json` y esquemas en OpenAPI. |
| `POST /customers` | Implementado | Registrado por el composition root; devuelve `201 Created`. |
| Composition root | Implementado | Sesión SQLAlchemy por petición y dependencia del caso de uso sustituida en `bootstrap/main.py`. |

## 7. Criterios de aceptación

1. Un DNI/NIF, NIE o CIF/NIF válido se normaliza y se clasifica correctamente.
2. Un identificador con formato o control incorrecto se rechaza.
3. `country` solo admite `ES` en los esquemas y en el dominio.
4. `email` es obligatorio y se valida con `EmailStr`.
5. Los cinco campos de FR-01 son obligatorios en el esquema y en la API.
6. `plan` solo admite `standard`; no existe valor por defecto.
7. La unicidad fiscal se garantiza con una restricción `(country, tax_id)` en la base de datos.
8. La razón social no tiene restricción de unicidad.
9. El repositorio persiste el NIF normalizado y `created_at` en UTC.
10. Los conflictos de unicidad no exponen excepciones SQLAlchemy.
11. `POST /customers` devuelve `201 Created` con el cliente persistido y sin `Location`.
12. Los errores controlados usan `application/problem+json` con códigos `422`, `409` y `500`.
13. OpenAPI documenta la ruta, los esquemas y las respuestas.
14. La migración se ejecuta desde una base vacía, se puede revertir a `base` y se puede volver a aplicar.
15. `domain` no importa FastAPI, Pydantic ni SQLAlchemy.
16. `presentation` no importa `domain` ni `infrastructure`.
17. `/health` y `/openapi.json` siguen funcionando.
18. `legal_name` se recorta, no puede quedar vacío y tiene entre 1 y 255 caracteres después del recorte; se persiste y se devuelve normalizado.

## 8. Validación y evidencias

La validación completa se registra en [TASK020](../../../ai-workspace/01-tasks/TASK020-customer-registration-completion.md) y en [TASK022](../../../ai-workspace/01-tasks/TASK022-customer-validation-fix.md). Incluye:

- Pytest con pruebas de dominio, aplicación, infraestructura, migración y API.
- Ruff check, Ruff format check, mypy y `pip check`.
- Comprobaciones HTTP de `/health`, `/openapi.json` y `POST /customers` con respuestas `201`, `409` y `422`.
- Pruebas de normalización y límites de `legal_name`, incluidos vacío, solo espacios, 1, 255 y 256 caracteres.
- Ciclo Alembic `upgrade head`, `current`, `downgrade base` y nueva `upgrade head` sobre SQLite temporal.
- Comprobación de aislamiento de `backend/.venv`.
- Comparación entre `requirements.lock` y el entorno instalado.
- Comprobación de reglas de arquitectura, `git diff --check` y exclusiones de Git.

## 9. Limitaciones y siguiente paso

- SQLite limita la concurrencia y no reproduce producción (P-05).
- La estructura global por capas puede no ser la frontera modular definitiva (P-06).
- No hay endpoint de detalle, por lo que no se publica `Location`.
- No se han introducido planes adicionales, precios de planes ni prestaciones asociadas.
- El lock de dependencias no es estricto ni usa hashes.
- No hay CI configurada.
- Los cambios de TASK020 y la corrección de TASK022 permanecen locales y sin publicar.

El siguiente paso es la revisión del propietario y, si la autoriza, la preparación del PR #3. El merge corresponde exclusivamente al propietario.
