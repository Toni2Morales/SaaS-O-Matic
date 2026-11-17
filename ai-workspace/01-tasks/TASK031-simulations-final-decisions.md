# TASK031 — Cierre definitivo de decisiones bloqueantes de simulaciones

| Campo | Valor |
| --- | --- |
| ID | TASK031 |
| Título | Cierre definitivo de decisiones bloqueantes de simulaciones |
| Estado | **Completada (documentación); decisiones bloqueantes cerradas; sin implementación** |
| Fecha | 2026-11-17 |
| Participantes | Propietario (decisiones) / OpenCode + DeepSeek (actualización documental y registro) |
| Autorización Git | **Ninguna publicación**: no `git add`, commit, push, PR, merge, rebase, reset ni `git clean`. |

## 1. Estado Git inicial y final

### 1.1. Estado inicial

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/simulations` |
| `HEAD` | `9cd553fff035de640e12a5eb5530f0791ed7b9e7` |
| `origin/main` | `9cd553fff035de640e12a5eb5530f0791ed7b9e7` |
| `main` local | `8371f9f608ce6e06984cc501d8240e1b7edf34d5` |
| Cambios locales | README modificado; TASK029, TASK030 y `docs/specs/003-simulations/` sin seguimiento |
| Archivos staged | Ninguno |
| Archivos locales | **6**, los esperados por TASK029/TASK030 |

Los seis archivos iniciales eran:

- `docs/specs/003-simulations/spec.md`
- `docs/specs/003-simulations/plan.md`
- `docs/specs/003-simulations/tasks.md`
- `ai-workspace/01-tasks/TASK029-simulations-preparation.md`
- `ai-workspace/01-tasks/TASK030-simulations-decisions-and-contract.md`
- `ai-workspace/README.md`

### 1.2. Estado final

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/simulations` |
| `HEAD` | Sin cambios |
| Archivos locales | **7** |
| Archivos staged | **Ninguno** |
| Commit / push / PR / merge | **No ejecutados** |
| `main` local | Sin cambios |
| TASK029 y TASK030 | Preservadas; hashes verificados |
| TASK032 | **No creado** |

## 2. Archivos creados y modificados

| Archivo | Acción |
| --- | --- |
| `docs/specs/003-simulations/spec.md` | Modificado: decisiones, contrato, modelo, validación, trazabilidad y aceptación parcial |
| `docs/specs/003-simulations/plan.md` | Modificado: arquitectura, secuencia, inventario y pruebas |
| `docs/specs/003-simulations/tasks.md` | Modificado: tareas futuras y criterios de verificación |
| `ai-workspace/README.md` | Modificado: índice y estado de TASK031 |
| `ai-workspace/01-tasks/TASK031-simulations-final-decisions.md` | Creado |

No se modificaron TASK029, TASK030, SPEC-001, SPEC-002, requisitos generales, código, pruebas, migraciones, dependencias ni configuración.

## 3. Decisiones aprobadas

Hay **ocho identificadores SIM-P únicos aprobados** y **nueve decisiones conceptuales aprobadas**, porque SIM-P09 cubre API y UI.

| Identificador | Decisión aprobada |
| --- | --- |
| SIM-P01 | Persistencia de simulaciones; historial futuro con importes originales. |
| SIM-P02 | Cliente registrado obligatorio. |
| SIM-P08 / Q-08 | Importes HTTP como cadenas decimales exactas; `Decimal` interno. |
| SIM-P09 / Q-12 (API) | Rango 1..1.000.000, ambos inclusive; sin coerciones. |
| SIM-P09 / Q-12 (UI) | Slider 1..1.000; entrada manual hasta 1.000.000. |
| SIM-P12 | Cliente válido inexistente: `404` problem+json; UUID malformado: `422`. |
| SIM-P13 | Importes en SQLite como texto decimal canónico. |
| SIM-P15 | `POST /simulations` sin prefijo `/api/v1`. |
| SIM-P17 | Solo coste progresivo de usuarios en EUR. |

## 4. Decisiones diferidas

Hay **nueve decisiones diferidas**, no canceladas:

| Identificador | Decisión diferida |
| --- | --- |
| SIM-P03 | Plan como contexto de simulación. |
| SIM-P04 / Q-15 | Almacenamiento y llamadas API. |
| SIM-P05 / Q-16 | Semántica del importe base. |
| SIM-P06 / Q-05 | Impuestos. |
| SIM-P07 / Q-06, Q-07, Q-17 | Divisas y tipos de cambio. |
| SIM-P10 / Q-09 | Inmutabilidad y edición. |
| SIM-P11 | Endpoints de lectura. |
| SIM-P14 | Impuesto histórico. |
| SIM-P16 | Idempotencia. |

Ninguna bloquea el primer incremento. No se introducen edición, borrado, lectura, dashboard, autenticación, autorización, multitenancy ni idempotencia inventada.

## 5. Contrato HTTP definitivo del incremento

### 5.1. Endpoint y petición

```text
POST /simulations
```

```json
{
  "customer_id": "00000000-0000-0000-0000-000000000000",
  "user_count": 100
}
```

| Campo | Tipo | Restricción |
| --- | --- | --- |
| `customer_id` | UUID | Obligatorio; cliente existente |
| `user_count` | Entero estricto | Obligatorio; entre 1 y 1.000.000 |

No se incluyen `plan`, `storage`, `api_calls`, `display_currency`, impuestos, descuentos ni otros campos comerciales no aprobados.

### 5.2. Respuesta correcta

HTTP `201 Created`:

```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "customer_id": "00000000-0000-0000-0000-000000000000",
  "user_count": 100,
  "user_subtotal_eur": "670.00",
  "created_at": "2026-11-16T16:00:00Z"
}
```

| Campo | Tipo |
| --- | --- |
| `id` | UUID de la simulación |
| `customer_id` | UUID del cliente |
| `user_count` | Entero |
| `user_subtotal_eur` | Cadena decimal exacta |
| `created_at` | Fecha y hora ISO 8601 en UTC |

No se incluye `base_amount_eur`. No se emite `Location` mientras no exista un endpoint de lectura aprobado.

### 5.3. Errores

| Situación | Código |
| --- | ---: |
| Entrada inválida | `422` |
| Cliente inexistente | `404` |
| Error interno inesperado | `500` |

Todos los errores usan `application/problem+json` y no exponen detalles internos de infraestructura. Un UUID malformado es `422`; un UUID válido no registrado es `404`.

## 6. Modelo de persistencia

Tabla `simulations`:

| Columna | Tipo | Restricción |
| --- | --- | --- |
| `id` | UUID | Clave primaria |
| `customer_id` | UUID | No nulo; FK a `customers.id` |
| `user_count` | Entero | No nulo; `CHECK` entre 1 y 1.000.000 |
| `user_subtotal_eur` | Texto decimal | No nulo; representación exacta |
| `created_at` | Fecha/hora UTC | No nulo |

Se documentan:

- Integridad referencial y activación de `PRAGMA foreign_keys=ON`.
- Transacción con commit y rollback; sin registros parciales.
- Conservación del subtotal histórico calculado.
- Migración con `upgrade` y `downgrade`.
- Pruebas de persistencia exacta.
- No se definen cascadas, edición ni versionado de tarifas.

## 7. Reglas de validación

| Capa | Regla |
| --- | --- |
| Dominio `pricing` | Mínimo 1; entero positivo estricto; rechazo de `bool`, no enteros y negativos; sin máximo comercial. No se modifica. |
| Aplicación | Rango defensivo 1..1.000.000; cliente existente; cálculo; persistencia; sin efectos ante error. |
| Presentación | UUID válido; entero estricto; rango 1..1.000.000; `422`; `application/problem+json`. |
| Persistencia | `CHECK` de `user_count` entre 1 y 1.000.000; FK; transacción. |
| UI futura | Slider 1..1.000; entrada manual hasta 1.000.000. No se implementa. |

El máximo de API no se introduce en `pricing`. El dominio sigue sin máximo comercial.

## 8. Trazabilidad y aceptación parcial

La matriz completa está en `spec.md`, secciones 12 y 13. Resumen:

| Requisito | Aceptación del primer incremento |
| --- | --- |
| FR-04 | Solo número de usuarios; almacenamiento y llamadas API pendientes. |
| FR-06 | Sin cálculo de impuestos. |
| FR-10 | Sin conversión de divisas. |
| FR-11 | Persistencia del subtotal EUR; otros importes y metadatos pendientes. |

Esta aceptación no cancela requisitos, no modifica sus objetivos finales, no declara completado todo el MVP y no autoriza a inventar datos o importes cero.

Q-08 y Q-12 quedan resueltas para este incremento. Q-15, Q-16 y Q-17 siguen abiertas. Las actualizaciones globales pendientes se registran en `spec.md`, sección 14, sin modificar los requisitos generales.

## 9. Plan de pruebas

| Usuarios | Subtotal EUR |
| ---: | ---: |
| 1 | `10.00` |
| 10 | `100.00` |
| 11 | `108.00` |
| 50 | `420.00` |
| 51 | `425.00` |
| 100 | `670.00` |
| 1000000 | `5000170.00` |

Verificación independiente de 1.000.000:

- 1–10: `100,00`.
- 11–50: `320,00`.
- 51–1.000.000: `999.950 × 5,00 = 4.999.750,00`.
- Total: `5.000.170,00`.

Se prevén pruebas de 0, negativos, 1.000.001, cantidades enormes, decimales como `10.0`, cadenas, booleanos, nulos, campos ausentes, UUID malformado y UUID válido inexistente. También se prevén pruebas HTTP, persistencia, migración/reversión, exactitud monetaria, regresión y arquitectura.

No se implementan ni ejecutan pruebas en TASK031.

## 10. Plan de implementación

1. Dominio, puertos y estructuras de aplicación.
2. Ampliación mínima de `CustomerRepository`.
3. Caso de uso de creación de simulaciones.
4. Persistencia y migración.
5. Contrato HTTP y bootstrap.
6. Pruebas y validaciones.
7. Auditoría independiente.
8. Publicación controlada mediante autorización específica.

No se inicia ninguna fase. No se crea TASK032.

## 11. Inventario propuesto para TASK032

### 11.1. Archivos nuevos

- `backend/src/saas_o_matic/domain/simulations/{__init__,entities,ports}.py`
- `backend/src/saas_o_matic/application/simulations/{__init__,dto,errors,use_cases}.py`
- `backend/src/saas_o_matic/infrastructure/simulations/{__init__,models,mappers,repositories}.py`
- `backend/src/saas_o_matic/presentation/simulations/{__init__,schemas,router,dependencies}.py`
- `backend/src/saas_o_matic/bootstrap/simulations.py`
- `backend/migrations/versions/0002_create_simulations.py`
- `backend/tests/test_simulation_use_case.py`
- `backend/tests/test_simulation_repository.py`
- `backend/tests/test_simulation_api.py`
- `backend/tests/test_simulation_schemas.py`

### 11.2. Archivos existentes que podrían modificarse

| Archivo | Cambio |
| --- | --- |
| `backend/src/saas_o_matic/domain/customers/ports.py` | Añadir `exists_by_id`. |
| `backend/src/saas_o_matic/infrastructure/customers/repositories.py` | Implementar `exists_by_id`. |
| `backend/src/saas_o_matic/presentation/problems.py` | Añadir errores de simulación y revisar el título de `422`. |
| `backend/src/saas_o_matic/presentation/app.py` | Registrar el router. |
| `backend/src/saas_o_matic/bootstrap/main.py` | Registrar la dependencia. |
| `backend/tests/test_migrations.py` | Probar migración y reversión. |
| `backend/tests/test_architecture.py` | Ampliar si es necesario. |

El inventario es una propuesta y puede ajustarse a la arquitectura real.

## 12. Validaciones documentales ejecutadas

| Comprobación | Resultado |
| --- | --- |
| `git status --short` | **7 archivos locales:** README modificado; TASK029, TASK030, TASK031 y los tres documentos de SPEC-003 sin seguimiento. |
| `git diff --check` | **OK; sin errores en archivos rastreados.** |
| Espacios y tabulaciones finales | **0 problemas en los siete archivos.** |
| Enlaces relativos | **154 enlaces comprobados; 0 rotos.** |
| Referencias a requisitos | **0 identificadores FR/CON/ASM/Q ausentes** en los cinco documentos de análisis. |
| SIM-P01 a SIM-P17 | **17 etiquetas presentes; 0 ausentes y 0 adicionales.** |
| Ocho aprobadas / nueve conceptuales / nueve diferidas | **8 identificadores únicos aprobados; 9 decisiones conceptuales (SIM-P09 API+UI); 9 diferidas; unión completa de 17.** |
| TASK029 y TASK030 intactas | **Sí:** hashes `9deb8ede918528df388a1910547d8b951145bd0f` y `a75a9e7a4ec5296aefd1b0cf6c87456bef9f67db`, idénticos al inicial. |
| Siete archivos locales | **Sí.** |
| Cero staged | **Sí.** |
| Sin cambios de código/configuración | **Sí:** sin cambios en `backend/src`, `backend/tests`, `backend/migrations`, `backend/pyproject.toml` o `backend/requirements.lock`. |
| Pytest, Ruff, mypy | **No ejecutados:** TASK031 no modifica código. |

## 13. Riesgos pendientes

- FR-04, FR-06, FR-10 y FR-11 no se satisfacen completos; la entrega es parcial y aceptada.
- Ordenar importes almacenados como texto no equivale a ordenar por valor numérico.
- SQLite no aplica claves foráneas por defecto.
- Los manejadores de error están acoplados a clientes.
- No hay idempotencia; los reintentos pueden duplicar simulaciones.
- No hay endpoint de lectura; lo persistido no se puede consultar todavía por API.
- El máximo técnico de 1.000.000 puede consumir recursos si no se valida antes de calcular.
- Los requisitos generales no se actualizan en TASK031; la divergencia queda registrada.
- No hay CI; las comprobaciones son locales.

## 14. Bloqueantes reales para implementar

**No hay bloqueantes funcionales conocidos para el primer incremento.** Las decisiones necesarias para el contrato, el modelo, la validación, el cliente inexistente, el almacenamiento monetario y la ruta están cerradas. Las decisiones diferidas no afectan al alcance del primer incremento.

Quedan riesgos de implementación, pero no decisiones imprescindibles sin resolver para TASK032.

## 15. Recomendación para TASK032

Recomiendo autorizar TASK032 como tarea de implementación del primer incremento, con el alcance exacto de SPEC-003: `POST /simulations`, persistencia, cliente obligatorio, rango 1..1.000.000, subtotal de usuarios, texto decimal canónico, `404`/`422`/`500` problem+json y pruebas completas. No debe incluir impuestos, divisas, almacenamiento, API, lectura, edición, idempotencia ni dashboard.

No se ha creado TASK032, no se ha implementado código y no se ha publicado ningún cambio.

## 16. Referencias

- [Especificación 003](../../docs/specs/003-simulations/spec.md)
- [Plan técnico 003](../../docs/specs/003-simulations/plan.md)
- [Tareas 003](../../docs/specs/003-simulations/tasks.md)
- [Requisitos funcionales](../../docs/requirements/functional-requirements.md)
- [ADR 0001 - Stack tecnológico](../../docs/adr/0001-technology-stack.md)
- [ADR 0002 - Arquitectura](../../docs/adr/0002-architecture.md)
- [Especificación 001 - Alta de clientes](../../docs/specs/001-customer-registration/spec.md)
- [Especificación 002 - Precios progresivos](../../docs/specs/002-progressive-pricing/spec.md)
- [TASK029 - Preparación de simulaciones](TASK029-simulations-preparation.md)
- [TASK030 - Cierre de decisiones y contrato](TASK030-simulations-decisions-and-contract.md)
- [Índice de trazabilidad](../README.md)
