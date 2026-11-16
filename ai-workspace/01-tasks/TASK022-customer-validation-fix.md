# TASK022 - Corrección de `legal_name` y pruebas de regresión

| Campo | Valor |
| --- | --- |
| ID | TASK022 |
| Título | Corrección del hallazgo M-01 de TASK021 y pruebas de regresión de `legal_name` |
| Estado | **Completada y validada localmente; cambios no publicados** |
| Fecha | 2026-11-16 |
| Rama | `feature/customer-registration` |
| Base | `be755a68a52392fd562eb3901e317bc85b1ed8e9` (`HEAD` y `origin/main`) |
| Participantes | Propietario (instrucción y regla funcional) / OpenCode + DeepSeek (implementación, pruebas y documentación) |
| Autorización Git | Modificar código, pruebas y documentación dentro del alcance; `git add`, commit, push, PR, merge, escritura en `main` y comandos destructivos no autorizados |

## 1. Objetivo y alcance

Corregir el hallazgo M-01 de TASK021 antes de publicar el alta de clientes, sin ampliar la funcionalidad ni refactorizar áreas ajenas.

La corrección se limita a:

- Validar y normalizar `legal_name` en dominio y aplicación.
- Alinear la validación de Pydantic y la documentación OpenAPI.
- Actualizar la especificación y la documentación afectada.
- Añadir pruebas de regresión para los casos indicados en TASK022.
- Registrar los hallazgos menores m-01 a m-05 de TASK021.

No se modifica la longitud `VARCHAR(255)` ni se crea una migración nueva. No se añaden dependencias.

## 2. Hallazgo original de TASK021

TASK021 fue una auditoría en sesión, sin archivo de informe en el repositorio. Su hallazgo M-01 quedó registrado así:

- `POST /customers` aceptaba `legal_name` vacío, compuesto solo por espacios o de longitud superior a 255 caracteres.
- SQLite almacenaba valores de longitud 0, 3 y 300 aunque `CustomerModel.legal_name` y la migración declaran `VARCHAR(255)`.
- La validación de Pydantic no imponía límites de contenido ni longitud y el dominio no protegía las llamadas internas.

Este registro no reescribe el informe histórico de TASK021; solo traza el hallazgo y su corrección.

## 3. Regla funcional aplicada

La instrucción TASK022 del propietario se tomó como autorización para aplicar la siguiente regla, registrada como D-15:

- `legal_name` es obligatorio.
- Se eliminan los espacios iniciales y finales mediante `strip()`.
- Se rechazan cadenas vacías o compuestas únicamente por espacios.
- Se aceptan longitudes de 1 a 255 caracteres después del recorte.
- Se conservan los espacios interiores.
- Se persiste y se devuelve la razón social normalizada.

## 4. Cambios realizados

### 4.1 Dominio

- `backend/src/saas_o_matic/domain/customers/errors.py`: nuevo error `InvalidLegalName`.
- `backend/src/saas_o_matic/domain/customers/value_objects.py`: constantes `LEGAL_NAME_MIN_LENGTH = 1` y `LEGAL_NAME_MAX_LENGTH = 255`, y función `normalize_legal_name()`.
- `backend/src/saas_o_matic/domain/customers/entities.py`: `Customer.__post_init__()` normaliza `legal_name` para proteger las llamadas internas.
- `backend/src/saas_o_matic/domain/customers/__init__.py`: exporta `InvalidLegalName`.

### 4.2 Aplicación

- `backend/src/saas_o_matic/application/customers/catalogs.py`: reexporta los límites compartidos para que presentación no importe directamente el dominio.
- `backend/src/saas_o_matic/application/customers/use_cases.py`: `CreateCustomer` normaliza `legal_name` y traduce `InvalidLegalName` a `InvalidCustomerData("legal_name", ...)`.

### 4.3 Presentación y OpenAPI

- `backend/src/saas_o_matic/presentation/customers/schemas.py`: `LegalNameStr` usa `StringConstraints(strip_whitespace=True, min_length=1, max_length=255)`.
- El mismo tipo se aplica a la petición y a la respuesta.
- OpenAPI documenta `minLength: 1` y `maxLength: 255` en ambos esquemas.

### 4.4 Documentación

- `docs/requirements/functional-requirements.md`: versión 0.7, nota de FR-01 y decisión D-15.
- `docs/specs/001-customer-registration/spec.md`: D-15, contrato de `legal_name`, error `422`, criterio de aceptación y evidencias.
- `docs/specs/001-customer-registration/plan.md`: estado, restricciones de `legal_name` y riesgo residual de mantener alineadas las capas.
- `docs/specs/001-customer-registration/tasks.md`: D-15 y tareas de TASK022.
- `backend/README.md`: regla de normalización y límites en la documentación de la API.
- `README.md`: estado de publicación de TASK022.
- `ai-workspace/README.md`: índice de TASK022 y actualización de limitaciones.

### 4.5 Persistencia y dependencias

- No se modifica `backend/src/saas_o_matic/infrastructure/customers/models.py`; `legal_name` sigue siendo `String(255)`.
- No se modifica `backend/migrations/versions/0001_create_customers.py`.
- No se modifican `backend/pyproject.toml` ni `backend/requirements.lock` por TASK022.

## 5. Pruebas nuevas

### 5.1 Esquemas Pydantic

- `backend/tests/test_customer_schemas.py`:
  - Razón social vacía, solo espacios y solo tabuladores/saltos de línea.
  - Longitud de 1 carácter.
  - Longitud de 255 caracteres después del recorte.
  - Longitud de 256 caracteres.
  - Recorte de espacios exteriores y conservación de espacios interiores.
  - Límites `minLength` y `maxLength` en el esquema JSON/OpenAPI.

### 5.2 Dominio y aplicación

- `backend/tests/test_customer_use_case.py`:
  - Normalización en el caso de uso y persistencia normalizada en el repositorio en memoria.
  - Rechazo de vacío, solo espacios y 256 caracteres sin llegar al repositorio.
  - Aceptación de 255 caracteres.
  - Normalización directa en la entidad `Customer`.
  - Rechazo directo en la entidad de valores inválidos.

### 5.3 API HTTP

- `backend/tests/test_customer_api.py`:
  - `legal_name` con espacios exteriores se recorta, se devuelve normalizado y se persiste normalizado.
  - Vacío, solo espacios y tabuladores/saltos de línea devuelven `422` y no persisten.
  - 1 carácter devuelve `201`.
  - 255 caracteres devuelve `201` y se persiste completo.
  - 256 caracteres devuelve `422` y no persiste.
  - Duplicado fiscal con variantes normalizadas devuelve `409`.
  - Misma razón social con identificadores fiscales distintos se acepta.
  - OpenAPI documenta los límites 1–255 en petición y respuesta.

### 5.4 Identificadores fiscales

- `backend/tests/test_spanish_tax_id.py`: se añaden NIE válidos con prefijos `Y` y `Z`, y CIF válido con prefijo `K`, conforme al algoritmo implementado.

## 6. Validaciones ejecutadas

Todas las comprobaciones se ejecutaron desde `backend/.venv` y sin usar bases de datos existentes.

| Comprobación | Resultado real |
| --- | --- |
| `python -m pytest -q` | **100 passed in 2.92s** |
| `python -m ruff check .` | **All checks passed!** |
| `python -m ruff format --check .` | **44 files already formatted** |
| `python -m mypy .` | **Success: no issues found in 42 source files** |
| `python -m pip check` | **No broken requirements found.** |
| Lock frente a `pip freeze` | **35/35 coinciden; 0 diferencias** |
| `git diff --check` | Sin errores |
| `pytest tests/test_migrations.py -q` | **1 passed in 0.31s** |
| Migración `0001_create_customers` | Sin cambios; `legal_name` sigue siendo `VARCHAR(255)` |

### 6.1 Comprobaciones HTTP

Se usó una base SQLite temporal migrada con Alembic y eliminada al terminar la comprobación:

| Comprobación | Resultado real |
| --- | --- |
| `GET /health` | `200` con `{"status":"ok"}` |
| `GET /openapi.json` | `200`; `legal_name` con `minLength: 1` y `maxLength: 255` en petición y respuesta |
| `POST /customers` con `"  Empresa  Ejemplo S.L.  "` | `201`; respuesta y SQLite con `"Empresa  Ejemplo S.L."` |
| `POST /customers` con `""`, `"   "` y 256 caracteres | `422` en los tres casos; sin nuevas filas persistidas |

La comprobación con `TestClient` emitió un aviso de deprecación de Starlette sobre `httpx`; no afectó al resultado. Las pruebas del repositorio usan `AsyncClient`.

## 7. Hallazgos menores de TASK021

| ID | Estado | Descripción |
| --- | --- | --- |
| m-01 | Pendiente | La entidad de dominio no valida en tiempo de ejecución los tipos de `plan` y `country`; `Customer(plan="premium")` puede construirse y `to_model` falla después con `AttributeError`. |
| m-02 | Pendiente | No existen restricciones `CHECK` de base de datos para `country='ES'` o `plan='standard'`; una inserción directa de `plan='premium'` puede almacenarse y fallar al reconstruir el dominio. |
| m-03 | Pendiente | Los nombres de campo de los errores `422` son inconsistentes: Pydantic usa `body.plan`/`body.country` y la aplicación usa `tax_id`/`plan`. |
| m-04 | Pendiente | El manejador genérico de `500` no registra la excepción original en el servidor, aunque la respuesta al cliente está saneada. |
| m-05 | **Cubierto por TASK022** | Faltaban pruebas de `legal_name` vacío/sobredimensionado, duplicado fiscal normalizado, misma razón social con distinto identificador, NIE con `Y`/`Z` y CIF con `K`. |

m-01 a m-04 permanecen como observaciones trazadas para una decisión posterior. No se corrigieron automáticamente porque no eran necesarios para completar la corrección principal.

## 8. Estado de Git

- Rama: `feature/customer-registration`.
- `HEAD` y `origin/main`: `be755a68a52392fd562eb3901e317bc85b1ed8e9`.
- Cambios staged: **ninguno**.
- Estado final tras crear este informe: **11 archivos modificados, 42 no rastreados, 0 staged**.
- Los cambios de TASK018–TASK020 y TASK022 permanecen locales y sin publicar.
- `LICENSE` no se ha modificado.
- No se han versionado `backend/.venv`, `TASKS.zip`, bases SQLite ni cachés.
- `backend/var` está vacío; no se ha creado una base de desarrollo.
- No se ejecutaron `git add`, commit, push, creación de PR, merge, escritura en `main` ni comandos destructivos.

## 9. Recomendación sobre el PR #3

La corrección está validada localmente y no requiere cambios de migración ni dependencias. Se recomienda que el propietario revise el diff completo y, si lo aprueba, autorice expresamente la preparación del PR #3 con los cambios de TASK018–TASK020 y TASK022.

m-01 a m-04 no bloquean la corrección principal, pero deben permanecer trazados para una tarea posterior. No se ha creado ni publicado el PR #3.
