# TASK032 - Implementación del primer incremento de simulaciones

| Campo | Valor |
| --- | --- |
| ID | TASK032 |
| Título | Implementación del primer incremento del módulo de simulaciones |
| Estado | Completada y validada localmente; cambios no publicados |
| Fecha | 2026-11-17 |
| Rama | `feature/simulations` |
| HEAD | `9cd553fff035de640e12a5eb5530f0791ed7b9e7` |
| Base | `origin/main` en `9cd553fff035de640e12a5eb5530f0791ed7b9e7` |
| Especificación | [SPEC-003](../../docs/specs/003-simulations/spec.md) |
| Plan | [PLAN-003](../../docs/specs/003-simulations/plan.md) |
| Tareas | [TASKS-003](../../docs/specs/003-simulations/tasks.md) |
| Autorización Git | Sin autorización de `git add`, commit, push, PR ni merge |

## 1. Estado Git inicial y final

### Inicial

- Rama: `feature/simulations`.
- HEAD: `9cd553fff035de640e12a5eb5530f0791ed7b9e7`.
- `origin/main`: `9cd553fff035de640e12a5eb5530f0791ed7b9e7`.
- `main` local: `8371f9f608ce6e06984cc501d8240e1b7edf34d5`.
- Sin archivos staged.
- Siete archivos locales pendientes de TASK029–TASK031, preservados sin cambios.
- Suite base: **167 pruebas superadas**.

### Final

- Rama: `feature/simulations`.
- HEAD: `9cd553fff035de640e12a5eb5530f0791ed7b9e7`.
- `origin/main`: `9cd553fff035de640e12a5eb5530f0791ed7b9e7`.
- `main` local: `8371f9f608ce6e06984cc501d8240e1b7edf34d5`.
- Sin archivos staged.
- Suite final: **240 pruebas superadas, 0 fallidas, 0 omitidas**.
- TASK029, TASK030 y TASK031 conservan sus hashes:
  - `9deb8ede918528df388a1910547d8b951145bd0f`
  - `a75a9e7a4ec5296aefd1b0cf6c87456bef9f67db`
  - `5e77d00aa9758fca9e07ff32d32a8fca5eb81491`

## 2. Confirmación de rama y HEAD

Se trabajó exclusivamente en `feature/simulations`. No se cambió de rama, no se modificó `main` local o remoto y no se reescribió el historial. HEAD y `origin/main` permanecen en el commit esperado.

## 3. Archivos creados

### Dominio

- `backend/src/saas_o_matic/domain/simulations/__init__.py`
- `backend/src/saas_o_matic/domain/simulations/entities.py`
- `backend/src/saas_o_matic/domain/simulations/ports.py`

### Aplicación

- `backend/src/saas_o_matic/application/simulations/__init__.py`
- `backend/src/saas_o_matic/application/simulations/dto.py`
- `backend/src/saas_o_matic/application/simulations/errors.py`
- `backend/src/saas_o_matic/application/simulations/use_cases.py`

### Infraestructura

- `backend/src/saas_o_matic/infrastructure/simulations/__init__.py`
- `backend/src/saas_o_matic/infrastructure/simulations/mappers.py`
- `backend/src/saas_o_matic/infrastructure/simulations/models.py`
- `backend/src/saas_o_matic/infrastructure/simulations/repositories.py`

### Presentación y composición

- `backend/src/saas_o_matic/presentation/simulations/__init__.py`
- `backend/src/saas_o_matic/presentation/simulations/dependencies.py`
- `backend/src/saas_o_matic/presentation/simulations/router.py`
- `backend/src/saas_o_matic/presentation/simulations/schemas.py`
- `backend/src/saas_o_matic/bootstrap/simulations.py`

### Migración y pruebas

- `backend/migrations/versions/0002_create_simulations.py`
- `backend/tests/test_simulation_use_case.py`
- `backend/tests/test_simulation_repository.py`
- `backend/tests/test_simulation_api.py`
- `backend/tests/test_simulation_schemas.py`

### Documentación

- `ai-workspace/01-tasks/TASK032-simulations-implementation.md`

## 4. Archivos modificados

- `ai-workspace/README.md`: índice, narrativa y limitaciones de TASK032.
- `docs/specs/003-simulations/spec.md`: estado de implementación, contrato, persistencia, pruebas y riesgos.
- `docs/specs/003-simulations/plan.md`: estado, inventario real y resultado de implementación.
- `docs/specs/003-simulations/tasks.md`: checklist completado salvo auditoría, publicación y merge.
- `backend/migrations/env.py`: registro del modelo de simulaciones en los metadatos de Alembic.
- `backend/src/saas_o_matic/bootstrap/main.py`: composición y dependency override de simulaciones.
- `backend/src/saas_o_matic/domain/customers/ports.py`: `exists_by_id`.
- `backend/src/saas_o_matic/infrastructure/customers/repositories.py`: implementación de `exists_by_id`.
- `backend/src/saas_o_matic/infrastructure/database.py`: `PRAGMA foreign_keys=ON` en cada conexión SQLite.
- `backend/src/saas_o_matic/presentation/app.py`: registro del router de simulaciones.
- `backend/src/saas_o_matic/presentation/problems.py`: errores `422` y `404` de simulación y título específico.
- `backend/tests/test_customer_repository.py`: prueba de `exists_by_id`.
- `backend/tests/test_customer_use_case.py`: doble adaptado al puerto ampliado.
- `backend/tests/test_health.py`: comprobación del nuevo wiring y de la ruta OpenAPI.
- `backend/tests/test_migrations.py`: revisión `0002`, tabla, FK, CHECK, downgrade y conservación de clientes.

No se modificaron TASK029, TASK030, TASK031, SPEC-001, SPEC-002, requisitos generales, `pyproject.toml`, `requirements.lock` ni el dominio `pricing`.

## 5. Diferencias justificadas respecto al inventario previsto

- Se crearon todos los archivos nuevos previstos.
- No se creó un archivo de errores de dominio separado: `Simulation`, sus invariantes y `format_eur_amount` residen en `domain/simulations/entities.py`.
- Se modificó `backend/migrations/env.py`, autorizado por la necesidad de registrar el modelo en los metadatos de Alembic.
- Se modificaron `tests/test_health.py` y `tests/test_customer_use_case.py`, no listados inicialmente, para cubrir el nuevo wiring y mantener el doble de clientes conforme al puerto ampliado.
- No se crearon abstracciones, servicios, campos comerciales ni repositorios de lectura pública adicionales.

## 6. Arquitectura implementada

Se mantiene el monolito modular y la dirección de dependencias de ADR 0002:

- `domain/simulations` no importa FastAPI, Pydantic, SQLAlchemy ni capas externas.
- `application/simulations` depende del dominio, incluido `calculate_user_subtotal`.
- `infrastructure/simulations` depende del dominio y de la base SQLAlchemy.
- `presentation/simulations` depende de aplicación; no importa dominio.
- `bootstrap` compone los adaptadores y comparte una sesión por petición entre los repositorios de clientes y simulaciones.

## 7. Entidad y puertos

`Simulation` es una entidad inmutable con `id`, `customer_id`, `user_count`, `user_subtotal_eur` y `created_at`. Protege las invariantes básicas: usuarios enteros positivos, sin booleanos, y subtotal `Decimal` finito y no negativo.

`SimulationRepository` define únicamente `add(simulation)`. La implementación SQLAlchemy añade `get_by_id` como recuperación interna para pruebas de ida y vuelta, sin exponer un endpoint de lectura.

`format_eur_amount` produce texto decimal canónico con dos decimales. No redondea: rechaza importes con más precisión de la representable.

## 8. Caso de uso

`CreateSimulation`:

1. Valida defensivamente que `user_count` sea un entero estricto entre 1 y 1.000.000.
2. Invoca `calculate_user_subtotal`.
3. Comprueba `CustomerRepository.exists_by_id`.
4. Construye la simulación con `uuid4()` y `datetime.now(UTC)`.
5. Persiste mediante `SimulationRepository.add`.
6. Devuelve un `SimulationResult` con el subtotal como cadena exacta.

Los errores de validación se traducen a `InvalidSimulationData`; la ausencia de cliente a `SimulationCustomerNotFound`. No se persiste nada antes de completar las validaciones y la comprobación de cliente.

## 9. Ampliación de CustomerRepository

Se añadió `exists_by_id(customer_id: UUID) -> bool` al puerto y una consulta que selecciona solo el identificador en `SqlAlchemyCustomerRepository`. No se modificaron registro, validación fiscal, normalización, unicidad ni el contrato de `POST /customers`. Se añadió una prueba para cliente existente e inexistente.

## 10. Reutilización del motor pricing

El caso de uso importa y llama directamente a `calculate_user_subtotal`. No se copiaron tramos, precios ni lógica de cálculo. No se modificó el dominio `pricing` y no se introdujo el máximo técnico de la API en el motor.

## 11. Modelo de persistencia

`SimulationModel` representa la tabla `simulations`:

| Columna | Tipo | Restricción |
| --- | --- | --- |
| `id` | UUID | Clave primaria |
| `customer_id` | UUID | No nulo; FK `fk_simulations_customer_id` a `customers.id` |
| `user_count` | Integer | No nulo; CHECK `ck_simulations_user_count_range` entre 1 y 1.000.000 |
| `user_subtotal_eur` | Text | No nulo; texto decimal canónico |
| `created_at` | DateTime con zona | No nulo |

No se añadieron campos comerciales, borrado en cascada, edición ni versionado de tarifas.

## 12. Estrategia de almacenamiento monetario

- Cálculo interno con `Decimal`.
- Columna SQLAlchemy `Text` y almacenamiento SQLite de tipo texto.
- Punto decimal, dos decimales exactos, sin separadores de miles ni notación científica.
- Reconstrucción con `Decimal` al leer.
- Sin `float` y sin redondeo comercial.
- Prueba directa del texto almacenado y del valor recuperado para `670.00` y `5000170.00`.

## 13. Activación y verificación de claves foráneas

`create_sqlite_engine` registra un listener `connect` que ejecuta `PRAGMA foreign_keys=ON` en cada conexión. Se comprobó que la conexión devuelve `1` para el PRAGMA y que insertar una simulación con un `customer_id` inexistente produce `IntegrityError`, sin dejar registros.

## 14. Gestión transaccional

El repositorio controla la transacción: añade el modelo y hace `commit`. Ante cualquier error durante el alta o la confirmación, hace `rollback` y propaga la excepción. El caso de uso no hace commits duplicados. La respuesta `201` solo se genera después de que `add` haya confirmado. La sesión se crea por petición en el composition root y se libera al terminar.

## 15. Migración y reversión

`0002_create_simulations` depende de `0001_create_customers` y crea la tabla, la clave primaria, la FK, los `NOT NULL` y el CHECK. El downgrade elimina la tabla. Las pruebas verifican:

1. Upgrade desde la revisión anterior.
2. Creación correcta de la tabla y sus restricciones.
3. Conservación de clientes existentes.
4. Integridad referencial.
5. Downgrade a `0001_create_customers`.
6. Downgrade a `base` y nuevo upgrade a `head`.

No se modificó retroactivamente la migración de clientes ni se eliminaron bases de datos existentes.

## 16. Contrato HTTP implementado

`POST /simulations`, sin prefijo `/api/v1`.

Petición:

```json
{
  "customer_id": "00000000-0000-0000-0000-000000000000",
  "user_count": 100
}
```

Respuesta `201 Created`:

```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "customer_id": "00000000-0000-0000-0000-000000000000",
  "user_count": 100,
  "user_subtotal_eur": "670.00",
  "created_at": "2026-11-16T16:00:00Z"
}
```

No se devuelve `Location`. Los campos adicionales se ignoran conforme a la política existente de los esquemas HTTP; se documentó esa decisión. `user_count` usa validación estricta y no acepta `10.0`, cadenas, booleanos ni nulos.

## 17. Ejemplo real de petición y respuesta

Ejemplo obtenido durante la validación local con una base SQLite temporal migrada. Los UUID y la fecha son los generados en esa ejecución y no corresponden a datos persistidos en el repositorio.

Petición:

```http
POST /simulations
Content-Type: application/json

{
  "customer_id": "c58669e3-4bcb-49ca-b2c3-7f6eb17cb506",
  "user_count": 100
}
```

Respuesta:

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: (ausente)

{
  "id": "660c66d3-cd19-4192-8946-b60a0cdf98d4",
  "customer_id": "c58669e3-4bcb-49ca-b2c3-7f6eb17cb506",
  "user_count": 100,
  "user_subtotal_eur": "670.00",
  "created_at": "2026-11-17T14:54:58.935304Z"
}
```

## 18. Manejo de errores

- `422`: errores de esquema, UUID malformado y validación defensiva de aplicación. Título `Datos de simulación no válidos`.
- `404`: UUID válido de cliente inexistente. Título `Cliente no encontrado`.
- `500`: error interno inesperado, sin trazas, SQL, credenciales ni detalles internos.
- Todos usan `application/problem+json` y el esquema `ProblemDetails`.
- El título de validación de clientes se mantiene mediante selección por ruta; no se degradó el comportamiento público existente.

## 19. Resultados de los siete ejemplos comerciales

| Usuarios | Subtotal EUR |
| ---: | ---: |
| 1 | `10.00` |
| 10 | `100.00` |
| 11 | `108.00` |
| 50 | `420.00` |
| 51 | `425.00` |
| 100 | `670.00` |
| 1000000 | `5000170.00` |

Los siete valores se comprobaron en caso de uso, repositorio y API, comparando la cadena exacta.

## 20. Pruebas nuevas y totales

- Suite base: 167 superadas.
- Suite final: **240 superadas, 0 fallidas, 0 omitidas**.
- Nuevas pruebas de simulación: **72**.
  - `test_simulation_use_case.py`: 21.
  - `test_simulation_repository.py`: 5.
  - `test_simulation_api.py`: 24.
  - `test_simulation_schemas.py`: 22.
- Prueba adicional de `exists_by_id`: 1.
- `test_migrations.py`: 1 superada; `test_architecture.py`: 7; `test_pricing.py`: 67.
- No se eliminaron, desactivaron ni omitieron pruebas para ocultar fallos.

## 21. Validaciones reales ejecutadas

Desde `backend/` con `backend/.venv/Scripts/python.exe`:

```text
python -m pytest                                     240 passed
python -m pytest tests/test_simulation_use_case.py   21 passed
python -m pytest tests/test_simulation_repository.py  5 passed
python -m pytest tests/test_simulation_api.py        24 passed
python -m pytest tests/test_simulation_schemas.py    22 passed
python -m pytest tests/test_migrations.py             1 passed
python -m pytest tests/test_architecture.py           7 passed
python -m pytest tests/test_pricing.py               67 passed
python -m ruff check .                               All checks passed
python -m ruff format --check .                      71 files already formatted
python -m mypy .                                     Success: 69 source files
python -m pip check                                  No broken requirements found
```

También se ejecutaron `git diff --check` sin errores, comprobación de hashes de TASK029–TASK031, ausencia de cambios en `pricing`, ausencia de cambios en dependencias y ausencia de archivos staged. Se verificaron los 35 pines de `requirements.lock` contra las versiones instaladas: 0 ausentes y 0 discrepancias. Los enlaces relativos de la documentación modificada resolvieron correctamente y no se detectaron espacios ni tabulaciones finales en los archivos nuevos o modificados. La búsqueda de patrones de secretos solo encontró la mención documental de la propia checklist.

## 22. Dependencias

No se añadieron dependencias ni se modificaron `backend/pyproject.toml` o `backend/requirements.lock`. `pip check` no encontró requisitos rotos. Se utilizó exclusivamente el entorno virtual del proyecto.

## 23. Limitaciones y riesgos

- FR-04, FR-06, FR-10 y FR-11 siguen parcialmente satisfechos.
- No hay endpoint de lectura ni historial accesible por API.
- No hay idempotencia; los reintentos pueden duplicar simulaciones.
- No hay edición, borrado ni política de inmutabilidad decidida.
- La ordenación numérica de importes no equivale a ordenación textual; no se implementó ordenación monetaria.
- No hay CI, autenticación, autorización ni multitenancy.
- H-03 del motor de precios, relativo al contexto Decimal heredado, sigue pendiente.
- Las nueve decisiones diferidas de SPEC-003 siguen abiertas.
- La documentación global de requisitos y las preguntas Q-08/Q-12/FR-04/06/10/11 siguen pendientes de actualización.
- El ejemplo real usa una base temporal; no se versionó ninguna base SQLite.

## 24. Criterios de aceptación cumplidos

Se consideran cumplidos los 20 criterios de TASK032 en el alcance local:

1. Existe `POST /simulations`.
2. Requiere un cliente registrado.
3. Rechaza entradas inválidas.
4. Respeta el máximo técnico de 1.000.000.
5. Reutiliza el motor pricing.
6. Devuelve los siete subtotales exactos.
7. Persiste correctamente las simulaciones.
8. Usa texto decimal canónico.
9. Aplica integridad referencial real.
10. Garantiza transacciones correctas.
11. Devuelve `201`, `404`, `422` y `500` según corresponda.
12. Mantiene `application/problem+json`.
13. Dispone de migración y reversión verificadas.
14. Supera las pruebas nuevas y anteriores.
15. Supera Ruff, mypy y `pip check`.
16. Respeta la arquitectura.
17. No introduce funcionalidades excluidas.
18. Mantiene intacto el dominio pricing.
19. Documenta las limitaciones.
20. No publica cambios.

La auditoría independiente y la publicación no forman parte de TASK032 y siguen pendientes.

## 25. Incidencias pendientes

No quedan fallos funcionales conocidos en el alcance local. No se ejecutó auditoría independiente, no se publicó la rama y no se creó TASK033. La actualización de requisitos generales y la revisión de H-03 quedan fuera del alcance.

## 26. Recomendación para TASK033

Realizar una auditoría independiente de la implementación local antes de cualquier publicación. La auditoría debería revisar el contrato HTTP, la exactitud monetaria, la FK y las transacciones, la migración, la separación de capas, las pruebas y la documentación. Si la auditoría es favorable, una tarea posterior autorizada podría preparar el commit, el push y el PR; el merge seguiría reservado al propietario. No se recomienda iniciar una nueva funcionalidad antes de cerrar esa revisión.

## Confirmaciones expresas

- Sin cambios en `backend/src/saas_o_matic/domain/pricing`.
- Sin modificaciones en `main` local o remoto.
- Sin archivos staged.
- Sin commit.
- Sin push.
- Sin PR.
- Sin merge.
- Sin operaciones destructivas.
- Sin creación de TASK033.
