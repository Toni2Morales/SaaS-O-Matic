# Plan técnico 003 - Simulaciones de costes

| Campo | Valor |
| --- | --- |
| ID | PLAN-003 |
| Título | Plan técnico del primer incremento de simulaciones |
| Estado | **Implementación local completada en TASK032; 240 pruebas superadas; auditoría independiente y publicación pendientes** |
| Fecha | 2026-11-17 |
| Base arquitectónica | [ADR 0002](../../adr/0002-architecture.md) |
| Especificación | [spec.md](spec.md) |
| Tareas | [tasks.md](tasks.md) |
| Base Git | `origin/main` en `9cd553fff035de640e12a5eb5530f0791ed7b9e7` |

## 1. Principios

- No implementar hasta que el propietario autorice una tarea de implementación.
- Persistir cada simulación y exigir un cliente registrado.
- Calcular únicamente el subtotal de usuarios en EUR.
- Reutilizar `calculate_user_subtotal`; no duplicar tramos, precios ni validaciones.
- Representar los importes HTTP como cadenas decimales exactas.
- Almacenar los importes como texto decimal canónico.
- No usar `float`, números JSON para dinero ni redondeos comerciales nuevos.
- Mantener `presentation → application → domain` e `infrastructure → domain`.
- No introducir impuestos, divisas, almacenamiento, llamadas API, planes nuevos ni cargos sin decisión expresa.
- No crear abstracciones o campos sin un caso de uso real.

## 2. Decisiones aprobadas y diferidas

### 2.1. Aprobadas

Hay **ocho identificadores SIM-P únicos aprobados** y **nueve decisiones conceptuales aprobadas**, porque SIM-P09 cubre API y UI.

| Identificador | Decisión |
| --- | --- |
| SIM-P01 | Persistencia de simulaciones. |
| SIM-P02 | Cliente registrado obligatorio. |
| SIM-P08 / Q-08 | Importes HTTP como cadena decimal exacta. |
| SIM-P09 / Q-12 (API) | Rango 1..1.000.000, ambos inclusive. |
| SIM-P09 / Q-12 (UI) | Slider 1..1.000; entrada manual hasta 1.000.000. |
| SIM-P12 | Cliente válido inexistente: `404` problem+json; UUID malformado: `422`. |
| SIM-P13 | Importes en SQLite como texto decimal canónico. |
| SIM-P15 | `POST /simulations` sin prefijo `/api/v1`. |
| SIM-P17 | Solo coste progresivo de usuarios. |

### 2.2. Diferidas

Hay **nueve decisiones diferidas**: SIM-P03, SIM-P04/Q-15, SIM-P05/Q-16, SIM-P06/Q-05, SIM-P07/Q-06-Q-07-Q-17, SIM-P10/Q-09, SIM-P11, SIM-P14 y SIM-P16.

Ninguna bloquea el primer incremento. Se mantienen abiertas y no se implementan por inferencia.

## 3. Arquitectura objetivo

### 3.1. Módulos

```text
backend/src/saas_o_matic/
├── domain/
│   └── simulations/
│       ├── __init__.py
│       ├── entities.py
│       └── ports.py
├── application/
│   └── simulations/
│       ├── __init__.py
│       ├── dto.py
│       ├── errors.py
│       └── use_cases.py
├── infrastructure/
│   └── simulations/
│       ├── __init__.py
│       ├── mappers.py
│       ├── models.py
│       └── repositories.py
├── presentation/
│   └── simulations/
│       ├── __init__.py
│       ├── dependencies.py
│       ├── router.py
│       └── schemas.py
└── bootstrap/
    ├── main.py
    └── simulations.py
```

No se crean estos paquetes en TASK031.

### 3.2. Flujo

1. El router valida el cuerpo y crea `CreateSimulationCommand(customer_id, user_count)`.
2. La aplicación valida el rango 1..1.000.000.
3. El caso de uso llama a `calculate_user_subtotal(user_count)`.
4. Si el motor rechaza el número de usuarios, se devuelve `422`.
5. El caso de uso comprueba `customer_repository.exists_by_id(customer_id)`.
6. Si el cliente no existe, se devuelve `404`.
7. El caso de uso construye `Simulation` con `uuid4()` y `datetime.now(UTC)`.
8. El repositorio persiste y confirma la transacción.
9. El router serializa `user_subtotal_eur` como cadena decimal exacta.

### 3.3. Puertos y adaptadores

- `SimulationRepository.add(simulation)` en dominio; implementación SQLAlchemy en infraestructura.
- `CustomerRepository.exists_by_id(customer_id)` como ampliación mínima del puerto de clientes.
- La aplicación no conoce SQLAlchemy ni FastAPI.
- La presentación no importa dominio; usa DTOs de aplicación.
- El composition root comparte una sesión por petición entre ambos repositorios.

### 3.4. Errores

- `InvalidUserCount` de dominio → `InvalidSimulationData` de aplicación → `422`.
- `CustomerNotFound` de aplicación → `404` problem+json.
- `ProblemDetails` existente para todos los errores.
- El título de `422` no debe ser «Datos de cliente no válidos» para simulaciones; se propone «Datos de simulación no válidos».
- El `404` requiere un manejador o una respuesta problem+json explícita.
- No se exponen detalles internos de infraestructura.

## 4. Validación por capas

| Capa | Regla |
| --- | --- |
| Dominio `pricing` | Mínimo 1; entero positivo estricto; rechazo de `bool`, no enteros y negativos; sin máximo comercial. No se modifica. |
| Aplicación | Rango defensivo 1..1.000.000; cliente existente; cálculo; persistencia; sin efectos ante error. |
| Presentación | UUID válido; entero estricto; rango 1..1.000.000; `422`; `application/problem+json`. |
| Persistencia | `CHECK` de `user_count` entre 1 y 1.000.000; FK; transacción. |
| UI futura | Slider 1..1.000; entrada manual hasta 1.000.000. No se implementa. |

El máximo de API no se introduce en `pricing`. El dominio sigue sin máximo comercial.

## 5. Secuencia de implementación

### Fase 0. Confirmación de arranque

- Confirmar que las decisiones bloqueantes están cerradas.
- Confirmar la aceptación parcial de FR-04/06/10/11.
- Confirmar que no se implementan las decisiones diferidas.

No hay bloqueantes funcionales conocidos para el primer incremento.

### Fase 1. Dominio y aplicación

1. Crear entidad `Simulation` con `id`, `customer_id`, `user_count`, `user_subtotal_eur` y `created_at`.
2. Crear el puerto `SimulationRepository`.
3. Crear DTOs y errores de aplicación.
4. Implementar `CreateSimulation` con dependencias explícitas a pricing y al puerto de clientes.
5. Traducir `InvalidUserCount` y `CustomerNotFound`.
6. Probar los siete ejemplos y las entradas inválidas sin base de datos.

### Fase 2. Clientes

1. Añadir `exists_by_id(customer_id: UUID) -> bool` al puerto `CustomerRepository`.
2. Implementarlo en `SqlAlchemyCustomerRepository`.
3. Probar cliente existente, inexistente y UUID mal formado.
4. No cargar la entidad completa si no se necesita.

### Fase 3. Persistencia

1. Crear `SimulationModel`.
2. Crear mapeadores entidad/modelo.
3. Crear `SqlAlchemySimulationRepository` con commit y rollback.
4. Crear migración Alembic con `upgrade` y `downgrade`.
5. Declarar la clave foránea y activar `PRAGMA foreign_keys=ON`.
6. Probar la ida y vuelta exacta de `user_subtotal_eur`.
7. Probar `created_at` UTC, el máximo 1.000.000 y la ausencia de registros parciales.

### Fase 4. Presentación y bootstrap

1. Crear esquemas Pydantic v2 de entrada y salida.
2. Crear router `POST /simulations`.
3. Serializar `user_subtotal_eur` como cadena exacta.
4. Añadir manejadores de error de simulación.
5. Crear `bootstrap/simulations.py`.
6. Registrar el router y la dependencia en `app.py` y `main.py`.
7. No emitir `Location` hasta que exista un endpoint de lectura aprobado.

### Fase 5. Pruebas y calidad

1. Ejecutar pruebas unitarias, de integración, HTTP y arquitectura.
2. Ejecutar la suite completa de regresión.
3. Ejecutar Pytest, Ruff, mypy y `pip check` si el entorno lo permite.
4. Ejecutar `git diff --check` y verificar ausencia de artefactos.
5. Registrar resultados reales en el informe de tarea.

### Fase 6. Auditoría y publicación

1. Auditoría independiente de los cambios.
2. Correcciones limitadas si procede.
3. Publicación mediante una tarea específica autorizada.
4. El merge lo ejecuta el propietario.

TASK032 completó localmente las fases 1–5. La fase 6 no se inició: no hubo auditoría independiente, publicación ni merge.

## 6. Inventario propuesto para TASK032

### 6.1. Archivos nuevos

| Archivo | Responsabilidad |
| --- | --- |
| `backend/src/saas_o_matic/domain/simulations/__init__.py` | Paquete de dominio. |
| `backend/src/saas_o_matic/domain/simulations/entities.py` | Entidad `Simulation`. |
| `backend/src/saas_o_matic/domain/simulations/ports.py` | Puerto `SimulationRepository`. |
| `backend/src/saas_o_matic/application/simulations/__init__.py` | Paquete de aplicación. |
| `backend/src/saas_o_matic/application/simulations/dto.py` | Comando y resultado. |
| `backend/src/saas_o_matic/application/simulations/errors.py` | Errores de simulación. |
| `backend/src/saas_o_matic/application/simulations/use_cases.py` | Caso de uso `CreateSimulation`. |
| `backend/src/saas_o_matic/infrastructure/simulations/__init__.py` | Paquete de infraestructura. |
| `backend/src/saas_o_matic/infrastructure/simulations/models.py` | Modelo SQLAlchemy. |
| `backend/src/saas_o_matic/infrastructure/simulations/mappers.py` | Conversión entidad/modelo. |
| `backend/src/saas_o_matic/infrastructure/simulations/repositories.py` | Repositorio SQLAlchemy. |
| `backend/src/saas_o_matic/presentation/simulations/__init__.py` | Paquete de presentación. |
| `backend/src/saas_o_matic/presentation/simulations/schemas.py` | Esquemas Pydantic. |
| `backend/src/saas_o_matic/presentation/simulations/router.py` | Router HTTP. |
| `backend/src/saas_o_matic/presentation/simulations/dependencies.py` | Dependencias HTTP. |
| `backend/src/saas_o_matic/bootstrap/simulations.py` | Composición de dependencias. |
| `backend/migrations/versions/0002_create_simulations.py` | Migración; número indicativo. |
| `backend/tests/test_simulation_use_case.py` | Pruebas de aplicación. |
| `backend/tests/test_simulation_repository.py` | Pruebas de persistencia. |
| `backend/tests/test_simulation_api.py` | Pruebas HTTP. |
| `backend/tests/test_simulation_schemas.py` | Pruebas de esquemas y serialización. |

### 6.2. Archivos existentes que podrían modificarse

| Archivo | Cambio |
| --- | --- |
| `backend/src/saas_o_matic/domain/customers/ports.py` | Añadir `exists_by_id`. |
| `backend/src/saas_o_matic/infrastructure/customers/repositories.py` | Implementar `exists_by_id`. |
| `backend/src/saas_o_matic/presentation/problems.py` | Añadir errores de simulación y revisar el título de `422`. |
| `backend/src/saas_o_matic/presentation/app.py` | Registrar el router de simulaciones. |
| `backend/src/saas_o_matic/bootstrap/main.py` | Registrar la dependencia de simulación. |
| `backend/tests/test_migrations.py` | Probar la nueva migración y la reversión. |
| `backend/tests/test_architecture.py` | Ampliar si es necesario; no se prevé cambio funcional. |

TASK032 creó todos los archivos nuevos previstos. No fue necesario crear un archivo de errores de dominio separado: `Simulation`, sus invariantes y `format_eur_amount` residen en `domain/simulations/entities.py`. Además de los archivos existentes previstos, se adaptaron `migrations/env.py` para registrar el modelo, `tests/test_health.py` para comprobar el nuevo wiring y `tests/test_customer_use_case.py` para que su doble cumpla el puerto ampliado. No se modificó el dominio `pricing`.

## 7. Estrategia de pruebas

| Nivel | Pruebas |
| --- | --- |
| Dominio `pricing` | Ya cubierto; no se duplica. |
| Aplicación | Siete ejemplos, reutilización del motor, límites, entradas inválidas, cliente inexistente. |
| Persistencia | Migración y reversión, repositorio, FK, `Decimal` exacto, `created_at` UTC, máximo técnico. |
| HTTP | `201`, `422`, `404`, `problem+json`, cadena monetaria, UUID y fecha. |
| Arquitectura | Dependencias entre capas y ausencia de imports prohibidos. |
| Regresión | Clientes, precios, problemas, salud y migraciones. |

Los siete subtotales de aceptación son `10.00`, `100.00`, `108.00`, `420.00`, `425.00`, `670.00` y `5000170.00` EUR. Las pruebas comparan la cadena exacta, no un `float`.

Resultado real de TASK032: **240 pruebas superadas, 0 fallidas, 0 omitidas**. Las 72 pruebas nuevas de simulación se distribuyen en 21 de caso de uso, 5 de repositorio, 24 de API y 22 de esquemas; se añadió una prueba de `exists_by_id` en clientes. Ruff, formato, mypy y `pip check` pasaron.

Verificación independiente para 1.000.000:

- 1–10: `100,00`.
- 11–50: `320,00`.
- 51–1.000.000: `999.950 × 5,00 = 4.999.750,00`.
- Total: `5.000.170,00`.

## 8. Riesgos

| Riesgo | Mitigación |
| --- | --- |
| Implementar antes de confirmar la aceptación parcial. | Fase 0. |
| Duplicar el cálculo de precios. | Importar y probar `calculate_user_subtotal`; revisar que no haya tramos en simulaciones. |
| Pérdida de exactitud en SQLite. | Texto decimal canónico y prueba de ida y vuelta; nunca `float`. |
| Ordenar texto monetario como número. | No implementar ordenación/agregación; documentar la advertencia. |
| Simulaciones huérfanas. | Clave foránea y `PRAGMA foreign_keys=ON`; prueba de integridad. |
| Error `422` con título de cliente. | Mensajes de simulación y pruebas de regresión. |
| `404` no problem+json. | Añadir manejador o respuesta explícita; probar. |
| Entradas grandes. | Validar 1.000.000 y rechazar 1.000.001 antes de calcular. |
| Duplicados por reintentos. | Documentar SIM-P16; no inventar idempotencia. |
| FR-04/06/10/11 parciales. | Mantener la matriz de trazabilidad y planificar fases futuras. |

## 9. Puntos de control

1. **Control 0:** aceptación parcial y alcance confirmados.
2. **Control 1:** contrato y formato monetario aprobados.
3. **Control 2:** modelo y migración aprobados.
4. **Control 3:** caso de uso reutiliza pricing y pasa los siete ejemplos.
5. **Control 4:** persistencia exacta, FK y reversión probadas.
6. **Control 5:** endpoint, errores y OpenAPI probados.
7. **Control 6:** arquitectura y regresión sin fallos.
8. **Control 7:** auditoría independiente.
9. **Control 8:** publicación autorizada y merge del propietario.

## 10. Resultado de implementación TASK032

| Control | Resultado |
| --- | --- |
| Dominio y aplicación | `Simulation`, puerto, DTOs, errores y `CreateSimulation` implementados. |
| Clientes | `exists_by_id` añadido al puerto, al repositorio SQLAlchemy y a los dobles afectados. |
| Persistencia | Modelo, mapeadores, repositorio, FK, CHECK y texto decimal canónico implementados. |
| Migración | `0002_create_simulations` probada con upgrade, downgrade y nuevo upgrade. |
| HTTP | `POST /simulations` con `201`, `404`, `422`, `500` y `application/problem+json`. |
| Pruebas | 240 superadas; 72 nuevas de simulación y una de `exists_by_id`. |
| Calidad | Ruff check, Ruff format --check, mypy y `pip check` sin errores. |
| Publicación | No realizada: sin commit, push, PR ni merge. |

## 11. Referencias

- [Especificación 003](spec.md)
- [Tareas 003](tasks.md)
- [Requisitos funcionales](../../requirements/functional-requirements.md)
- [ADR 0001 - Stack tecnológico](../../adr/0001-technology-stack.md)
- [ADR 0002 - Arquitectura](../../adr/0002-architecture.md)
- [Especificación 001 - Alta de clientes](../001-customer-registration/spec.md)
- [Especificación 002 - Precios progresivos](../002-progressive-pricing/spec.md)
- [TASK029 - Preparación de simulaciones](../../../ai-workspace/01-tasks/TASK029-simulations-preparation.md)
- [TASK030 - Cierre de decisiones y contrato](../../../ai-workspace/01-tasks/TASK030-simulations-decisions-and-contract.md)
- [TASK031 - Cierre definitivo de decisiones bloqueantes](../../../ai-workspace/01-tasks/TASK031-simulations-final-decisions.md)
- [TASK032 - Implementación del primer incremento](../../../ai-workspace/01-tasks/TASK032-simulations-implementation.md)
- [Índice de trazabilidad](../../../ai-workspace/README.md)
