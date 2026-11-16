# Plan técnico 001 - Alta de clientes

| Campo | Valor |
| --- | --- |
| ID | PLAN-001 |
| Título | Plan técnico para `POST /customers` |
| Estado | **Implementado; validación de `legal_name` corregida en TASK022. Cambios locales no publicados.** |
| Fecha | 2026-11-16 |
| Base arquitectónica | [ADR 0002](../../adr/0002-architecture.md) |
| Especificación | [spec.md](spec.md) |

## 1. Principios

- Respetar las dependencias `presentation → application → domain` e `infrastructure → domain`.
- Mantener `domain` en Python puro, sin FastAPI, Pydantic ni SQLAlchemy.
- No importar `infrastructure` desde ninguna capa; inyectarla desde `bootstrap/`.
- No reutilizar modelos SQLAlchemy como esquemas HTTP.
- No usar `create_all()` como sustituto de Alembic.
- No introducir dependencias nuevas sin autorización expresa.
- No fijar reglas de negocio que sigan pendientes.
- Mantener una única fuente de verdad para el catálogo de planes.

## 2. Estructura implementada

La estructura actual mantiene capas globales, no módulos por funcionalidad. La frontera modular definitiva sigue pendiente (P-06), pero los componentes de clientes se agrupan por subpaquete dentro de cada capa.

```text
backend/src/saas_o_matic/
├── domain/
│   └── customers/
│       ├── entities.py
│       ├── errors.py
│       ├── ports.py
│       └── value_objects.py
├── application/
│   └── customers/
│       ├── catalogs.py
│       ├── dto.py
│       ├── errors.py
│       └── use_cases.py
├── infrastructure/
│   ├── database.py
│   └── customers/
│       ├── mappers.py
│       ├── models.py
│       └── repositories.py
├── presentation/
│   ├── app.py
│   ├── problems.py
│   └── customers/
│       ├── dependencies.py
│       ├── router.py
│       └── schemas.py
└── bootstrap/
    ├── main.py
    └── customers.py
```

La migración inicial vive en `backend/migrations/versions/0001_create_customers.py`.

## 3. Dominio implementado

### 3.1 Entidad

`Customer` contiene:

| Atributo | Tipo | Estado |
| --- | --- | --- |
| `id` | `UUID` | Generado por el servidor (D-10). |
| `legal_name` | `str` | Obligatorio; recortado; 1–255 caracteres tras el recorte; sin unicidad (D-06, D-08, D-15). |
| `tax_id` | `SpanishTaxId` | Normalizado y validado (D-03, D-07). |
| `email` | `str` | Obligatorio; validación sintáctica en presentación (D-04, D-08). |
| `country` | `CountryCode` | Solo `ES` (D-01, D-08). |
| `plan` | `PlanCode` | Obligatorio; solo `standard` (D-02, D-08). |
| `created_at` | `datetime` | UTC; sin `updated_at` (D-14). |

### 3.2 Objetos de valor

- `CountryCode`: enumeración ISO 3166-1 alfa-2 con `ES` y `CountryCode.parse()`.
- `PlanCode`: enumeración del catálogo MVP con `STANDARD = "standard"` y `PlanCode.parse()`.
- `SpanishTaxId`: normaliza espacios y guiones, convierte a mayúsculas y valida DNI/NIF, NIE y CIF/NIF.
- `TaxIdKind`: clasifica el identificador como `DNI`, `NIE` o `CIF`.

`PlanCode.parse()` y `CountryCode.parse()` son la validación centralizada del catálogo. No existe un plan por defecto.

### 3.3 Errores de dominio

| Error | Uso |
| --- | --- |
| `InvalidTaxId` | Formato, longitud o carácter de control incorrectos. |
| `InvalidCountry` | País no soportado. |
| `InvalidPlan` | Plan fuera del catálogo aprobado. |
| `DuplicateCustomerTaxId` | Conflicto de unicidad detectado por persistencia. |

Los errores de dominio no se convierten directamente en HTTP. `application` los traduce y `presentation` los mapea.

### 3.4 Puerto de repositorio

```python
class CustomerRepository(Protocol):
    def exists_by_tax_id(self, tax_id: SpanishTaxId, country: CountryCode) -> bool: ...
    def add(self, customer: Customer) -> None: ...
```

La comprobación previa no sustituye a la restricción única de base de datos.

## 4. Aplicación implementada

### 4.1 Caso de uso

`CreateCustomer` recibe `CreateCustomerCommand` y devuelve `CustomerResult`.

Responsabilidades implementadas:

1. Normalizar y validar el identificador fiscal mediante el dominio.
2. Validar que el país sea `ES` mediante `CountryCode.parse()`.
3. Validar que el plan sea `standard` mediante `PlanCode.parse()`.
4. Comprobar duplicados mediante el puerto.
5. Generar UUID y `created_at` en UTC.
6. Persistir mediante el puerto.
7. Traducir errores de dominio a errores de aplicación.

La persistencia y el commit quedan en la frontera de infraestructura. El caso de uso no importa SQLAlchemy.

### 4.2 Errores de aplicación

| Error | Uso |
| --- | --- |
| `InvalidCustomerData` | Identificador fiscal, país o plan inválidos. |
| `CustomerTaxIdAlreadyExists` | Duplicado detectado antes o durante la persistencia. |

### 4.3 DTOs y catálogos compartidos

- `CreateCustomerCommand`: datos de entrada de aplicación.
- `CustomerResult`: datos de salida de aplicación con `CountryCode` y `PlanCode`.
- `application/customers/catalogs.py` reexporta `CountryCode` y `PlanCode` para presentación.
- No se reutilizan DTOs como esquemas Pydantic ni como modelos SQLAlchemy.

## 5. Infraestructura implementada

### 5.1 SQLAlchemy 2

`CustomerModel` es independiente del dominio. La tabla `customers` contiene:

- `id` como UUID y clave primaria.
- `legal_name`, `tax_id`, `email`, `country`, `plan` y `created_at`.
- Todos los campos funcionales no nulos.
- `plan` almacenado como cadena, sin valor por defecto.
- Restricción única `(country, tax_id)`.
- Sin restricción de unicidad sobre `legal_name`.

`to_domain` y `to_model` realizan el mapeo explícito. `created_at` se interpreta como UTC si SQLite lo devuelve sin zona horaria. `plan` se convierte con `PlanCode.parse()` al leer y se persiste con `plan.value` al escribir.

### 5.2 SQLite de desarrollo

`create_sqlite_engine` crea un motor para una ruta concreta y asegura el directorio padre. La configuración de Alembic usa por defecto `sqlite:///./var/saas_o_matic.sqlite3`, sustituible mediante `DATABASE_URL`.

Las pruebas usan una base SQLite temporal y aislada creada mediante Alembic. No se usa la base de desarrollo ni `create_all()` como sustituto de la migración.

### 5.3 Repositorio

`SqlAlchemyCustomerRepository` implementa el puerto:

- Comprueba la existencia por `(tax_id, country)`.
- Persiste y confirma la transacción en la frontera de infraestructura.
- Traduce conflictos de unicidad de SQLite/SQLAlchemy a `DuplicateCustomerTaxId`.
- No expone excepciones SQLAlchemy a capas superiores.

### 5.4 Alembic

Se ha añadido:

```text
backend/
├── alembic.ini
└── migrations/
    ├── env.py
    ├── script.py.mako
    └── versions/
        ├── 0001_create_customers.py
        └── README.md
```

La revisión `0001_create_customers`:

- Crea la tabla `customers` desde una base vacía.
- Declara UUID compatible con SQLite, `created_at` con zona horaria y los cinco campos funcionales no nulos.
- Declara la restricción única `uq_customers_country_tax_id` sobre `(country, tax_id)`.
- Permite `downgrade base` y una nueva `upgrade head`.

No se crea una tabla de planes porque el catálogo fijo de un único valor no necesita datos adicionales.

## 6. Presentación implementada

### 6.1 Esquemas Pydantic

- `CustomerCreateRequest`: exige `legal_name`, `tax_id`, `email`, `country` y `plan`.
- `legal_name` se recorta y se limita a 1–255 caracteres después del recorte; los límites se documentan en OpenAPI.
- `email` usa `EmailStr`.
- `country` usa `CountryCode`; `plan` usa `PlanCode`, reexportados desde aplicación.
- No incluye `id` en la petición.
- `CustomerResponse`: incluye UUID, campos del cliente y `created_at`.
- La respuesta se construye con `model_validate(result, from_attributes=True)`.

### 6.2 Errores `application/problem+json`

`ProblemDetails` y `ProblemFieldError` están implementados. Los manejadores traducen:

| Error | HTTP |
| --- | --- |
| `RequestValidationError` de FastAPI/Pydantic | `422 Unprocessable Content` |
| `InvalidCustomerData` | `422 Unprocessable Content` |
| `CustomerTaxIdAlreadyExists` | `409 Conflict` |
| Excepción no controlada | `500 Internal Server Error` sin detalles internos |

OpenAPI documenta `ProblemDetails` y las respuestas `409`, `422` y `500` con `application/problem+json`.

### 6.3 Endpoint

`POST /customers` está registrado en `presentation/customers/router.py`:

- Recibe `CustomerCreateRequest`.
- Ejecuta `CreateCustomer`.
- Devuelve `201 Created` con `CustomerResponse`.
- No añade cabecera `Location`.
- No expone endpoints de listado, edición o eliminación.

## 7. Composition root

`bootstrap/main.py` es el composition root provisional:

- Crea la fábrica de sesiones SQLite de forma perezosa, de modo que importar la aplicación no crea el directorio ni el fichero de base de datos.
- Sustituye la dependencia `get_create_customer_use_case` por una que abre una sesión por petición y construye `CreateCustomer` con `build_customer_use_case(session)`.
- Registra la aplicación con `/health` y `/customers`.

`bootstrap/customers.py` construye el caso de uso con el repositorio SQLAlchemy.

## 8. Estrategia de pruebas

| Nivel | Qué se prueba | Estado |
| --- | --- | --- |
| Dominio | DNI/NIF, NIE, CIF/NIF, normalización, país y plan `standard`/desconocido. | Implementado |
| Esquemas | Obligatoriedad de los cinco campos, `EmailStr`, país `ES`, plan `standard` y rechazo de otros valores. | Implementado |
| Aplicación | Normalización, errores de validación, plan inválido, duplicado previo y duplicado de persistencia. | Implementado |
| Infraestructura | Persistencia SQLite, lectura, `created_at` UTC, unicidad y traducción de conflictos. | Implementado |
| Migraciones | `upgrade head`, esquema, persistencia, duplicados, `current`, `downgrade base` y nueva `upgrade head`. | Implementado |
| API | `201`, persistencia, campos, `409`, `422`, JSON malformado, `500`, ausencia de `Location` y OpenAPI. | Implementado |
| Arquitectura | Reglas de dependencia del ADR 0002. | Implementado |

Las pruebas de persistencia y API usan SQLite temporal creado con Alembic. Las pruebas de dominio y aplicación no usan base de datos.

## 9. Dependencias

Dependencias ya disponibles y declaradas:

- FastAPI, Pydantic, SQLAlchemy, Alembic, Uvicorn.
- Pytest, HTTPX, Ruff, mypy.

Dependencia añadida y autorizada en TASK019:

- `email-validator==2.4.0`, necesaria para `EmailStr`.
- `dnspython==2.9.2`, dependencia transitiva fijada en `requirements.lock`.
- `idna==3.20` ya estaba instalada y se mantiene.

TASK020 no añade dependencias ni modifica `pyproject.toml` ni `requirements.lock`.

## 10. Orden de implementación completado

1. Aprobar D-02 y el catálogo de planes.
2. Sustituir la cadena opaca de `plan` por `PlanCode`.
3. Crear la migración inicial de `customers` con `plan` obligatorio.
4. Implementar el router `POST /customers` y conectarlo al caso de uso.
5. Añadir pruebas HTTP de integración y de migración.
6. Documentar la operación y sus respuestas en OpenAPI.
7. Ejecutar Pytest, Ruff, mypy, `pip check`, comprobaciones HTTP, Alembic y Git.

## 11. Riesgos técnicos

- SQLite limita la concurrencia y no reproduce producción (P-05).
- La estructura global de capas puede no ser la frontera modular definitiva (P-06).
- El catálogo de planes es fijo y cualquier plan futuro requerirá una decisión y una migración.
- La validación de `legal_name` se expresa en dominio y en el esquema Pydantic; los límites compartidos deben mantenerse alineados.
- El lock de dependencias no es estricto ni usa hashes.
- No hay CI configurada.
- No consta una revisión independiente humana de TASK020.
