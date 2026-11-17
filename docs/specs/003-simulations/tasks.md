# Tareas 003 - Simulaciones de costes

| Campo | Valor |
| --- | --- |
| ID | TASKS-003 |
| Título | Desglose del primer incremento de simulaciones |
| Estado | **Implementación local completada en TASK032; 240 pruebas superadas; auditoría y publicación pendientes** |
| Fecha | 2026-11-17 |
| Especificación | [spec.md](spec.md) |
| Plan | [plan.md](plan.md) |
| Preparación | [TASK029](../../../ai-workspace/01-tasks/TASK029-simulations-preparation.md), [TASK030](../../../ai-workspace/01-tasks/TASK030-simulations-decisions-and-contract.md) y [TASK031](../../../ai-workspace/01-tasks/TASK031-simulations-final-decisions.md) |

## 1. Regla de alcance

TASK031 fue exclusivamente documental. TASK032 autorizó e implementó localmente el primer incremento: dominio, aplicación, persistencia, migración, endpoint y pruebas. No se modificó el motor de precios ni se publicaron cambios.

Las casillas `[x]` reflejan trabajo completado y verificado en TASK032. Las casillas `[ ]` restantes corresponden a auditoría, publicación y merge, que no fueron autorizados.

## 2. Decisiones aprobadas

Hay **ocho identificadores SIM-P únicos aprobados** y **nueve decisiones conceptuales aprobadas**, porque SIM-P09 cubre API y UI.

| Identificador | Decisión | Estado |
| --- | --- | --- |
| SIM-P01 | Persistencia. | Aprobada. |
| SIM-P02 | Cliente obligatorio. | Aprobada. |
| SIM-P08 / Q-08 | Cadena decimal exacta. | Aprobada. |
| SIM-P09 / Q-12 (API) | Rango 1..1.000.000. | Aprobada. |
| SIM-P09 / Q-12 (UI) | Slider 1..1.000; manual hasta 1.000.000. | Aprobada. |
| SIM-P12 | Cliente inexistente: `404`; UUID malformado: `422`. | Aprobada. |
| SIM-P13 | Texto decimal canónico en SQLite. | Aprobada. |
| SIM-P15 | `POST /simulations` sin prefijo. | Aprobada. |
| SIM-P17 | Solo coste de usuarios. | Aprobada. |

## 3. Decisiones diferidas

Hay **nueve decisiones diferidas**. No bloquean el primer incremento.

| ID | Pregunta | Tratamiento |
| --- | --- | --- |
| SIM-P03 | Plan como contexto. | Omitir mientras no afecte al cálculo. |
| SIM-P04 / Q-15 | Almacenamiento y API. | Diferir. |
| SIM-P05 / Q-16 | Importe base. | Mantener `user_subtotal_eur` separado. |
| SIM-P06 / Q-05 | Impuestos. | Diferir. |
| SIM-P07 / Q-06, Q-07, Q-17 | Divisas y tasas. | Diferir. |
| SIM-P10 / Q-09 | Inmutabilidad/edición. | No exponer edición. |
| SIM-P11 | Endpoints de lectura. | Diferir; no emitir `Location`. |
| SIM-P14 | Impuesto histórico. | Diferir. |
| SIM-P16 | Idempotencia. | Documentar riesgo de duplicados. |

## 4. Aceptación parcial

- [x] **AC-01:** confirmar que FR-04 solo cubre usuarios en el primer incremento.
- [x] **AC-02:** confirmar que FR-06 no se implementa.
- [x] **AC-03:** confirmar que FR-10 no se implementa.
- [x] **AC-04:** confirmar que FR-11 solo cubre el subtotal EUR.
- [x] **AC-05:** registrar que la aceptación no cancela requisitos ni declara el MVP completo.

## 5. Fase 1. Dominio y aplicación

- [x] **A-01:** crear `domain/simulations/entities.py` con `Simulation`.
- [x] **A-02:** crear `domain/simulations/ports.py` con `SimulationRepository`.
- [x] **A-03:** crear `application/simulations/dto.py` con comando y resultado.
- [x] **A-04:** crear `application/simulations/errors.py`.
- [x] **A-05:** implementar `CreateSimulation` con `calculate_user_subtotal`.
- [x] **A-06:** validar defensivamente el rango 1..1.000.000 en aplicación.
- [x] **A-07:** traducir `InvalidUserCount` a error de aplicación.
- [x] **A-08:** traducir cliente inexistente a error de aplicación.
- [x] **A-09:** comprobar que no se duplican tramos, precios ni validaciones.
- [x] **A-10:** comprobar que el dominio pricing no se modifica.

**Criterio de verificación:** los siete ejemplos se calculan llamando al motor; 0, negativos, decimales, cadenas, booleanos, nulos y 1.000.001 se rechazan.

## 6. Fase 2. Clientes

- [x] **L-01:** añadir `exists_by_id(customer_id: UUID) -> bool` al puerto.
- [x] **L-02:** implementarlo en `SqlAlchemyCustomerRepository`.
- [x] **L-03:** probar cliente existente, inexistente y UUID mal formado.
- [x] **L-04:** comprobar compatibilidad con dobles de prueba.

**Criterio de verificación:** el caso de uso distingue cliente existente e inexistente sin acoplarse a SQLAlchemy.

## 7. Fase 3. Persistencia

- [x] **P-01:** crear `SimulationModel` con `id`, `customer_id`, `user_count`, `user_subtotal_eur` y `created_at`.
- [x] **P-02:** crear mapeadores entidad/modelo y restaurar UTC al leer.
- [x] **P-03:** crear `SqlAlchemySimulationRepository` con commit y rollback.
- [x] **P-04:** crear la migración Alembic con `upgrade` y `downgrade`.
- [x] **P-05:** declarar la clave foránea a `customers.id`.
- [x] **P-06:** activar y probar `PRAGMA foreign_keys=ON`.
- [x] **P-07:** añadir `CHECK` de `user_count` entre 1 y 1.000.000.
- [x] **P-08:** probar la ida y vuelta exacta de `user_subtotal_eur`.
- [x] **P-09:** probar `created_at`, `id`, máximo 1.000.000 y ausencia de registros parciales.
- [x] **P-10:** probar migración y reversión.

**Criterio de verificación:** una simulación persistida se recupera con el mismo importe exacto y no se crea con un cliente inexistente.

## 8. Fase 4. Presentación y bootstrap

- [x] **H-01:** crear esquemas Pydantic v2 de entrada y salida.
- [x] **H-02:** validar `customer_id` como UUID y `user_count` como entero estricto 1..1.000.000.
- [x] **H-03:** crear router `POST /simulations`.
- [x] **H-04:** serializar `user_subtotal_eur` como cadena decimal exacta.
- [x] **H-05:** añadir manejadores de error de simulación.
- [x] **H-06:** revisar el título genérico de `422`.
- [x] **H-07:** crear `bootstrap/simulations.py`.
- [x] **H-08:** registrar router y dependencia en `app.py` y `main.py`.
- [x] **H-09:** no emitir `Location` hasta que exista lectura aprobada.

**Criterio de verificación:** el endpoint responde `201`, los errores usan `problem+json` y la respuesta contiene UUID, entero, cadena decimal y fecha UTC.

## 9. Fase 5. Pruebas

### 9.1. Precios obligatorios

- [x] **T-01:** probar 1 usuario → `10.00`.
- [x] **T-02:** probar 10 usuarios → `100.00`.
- [x] **T-03:** probar 11 usuarios → `108.00`.
- [x] **T-04:** probar 50 usuarios → `420.00`.
- [x] **T-05:** probar 51 usuarios → `425.00`.
- [x] **T-06:** probar 100 usuarios → `670.00`.
- [x] **T-07:** probar 1.000.000 usuarios → `5000170.00`.

### 9.2. Límites y entradas inválidas

- [x] **T-08:** probar 0, negativos, 1.000.001 y cantidades enormes.
- [x] **T-09:** probar decimales, `10.0`, cadenas, booleanos y nulos.
- [x] **T-10:** probar campos ausentes y UUID malformado.
- [x] **T-11:** probar UUID válido de cliente inexistente.

### 9.3. HTTP

- [x] **T-12:** probar `201` y el contrato de respuesta.
- [x] **T-13:** probar cadenas monetarias y timestamp UTC.
- [x] **T-14:** probar `422`, `404` y `application/problem+json`.

### 9.4. Persistencia y arquitectura

- [x] **T-15:** probar almacenamiento, identificador único y relación con cliente.
- [x] **T-16:** probar FK, exactitud monetaria, máximo técnico y ausencia de parciales.
- [x] **T-17:** probar migración y reversión.
- [x] **T-18:** probar clientes, pricing, capas y regresión completa.
- [x] **T-19:** comprobar que pricing no tiene máximo comercial.

**Criterio de verificación:** todas las pruebas obligatorias pasan y las futuras se ejecutan solo después de su decisión.

## 10. Fase 6. Calidad, auditoría y publicación

- [x] **C-01:** ejecutar Pytest y registrar el resultado real.
- [x] **C-02:** ejecutar Ruff check y Ruff format --check.
- [x] **C-03:** ejecutar mypy.
- [x] **C-04:** ejecutar `pip check` si el entorno lo permite.
- [x] **C-05:** ejecutar `git diff --check`.
- [x] **C-06:** verificar que no se incluyen secretos, bases SQLite, `.venv` ni artefactos.
- [x] **C-07:** actualizar la especificación, el plan y las tareas con las decisiones aprobadas.
- [ ] **C-08:** auditoría independiente.
- [ ] **C-09:** publicación mediante una tarea específica autorizada.
- [ ] **C-10:** merge ejecutado por el propietario.

**Criterio de verificación:** el informe final contiene resultados reales, archivos afectados, decisiones y riesgos.

## 11. Criterio de finalización

El primer incremento se considerará terminado cuando:

1. La aceptación parcial esté registrada.
2. El caso de uso reutilice el motor y no duplique precios.
3. La simulación se persista con cliente, usuarios, subtotal exacto y fecha UTC.
4. El contrato HTTP y los errores estén probados.
5. La arquitectura y la suite de regresión pasen.
6. La documentación y el informe de tarea estén actualizados.
7. La publicación y el merge hayan sido autorizados.

TASK032 cumple localmente los criterios 1–6. El criterio 7 sigue pendiente porque no se autorizaron publicación ni merge.

## 12. Resultado real TASK032

- Suite completa: **240 pruebas superadas, 0 fallidas, 0 omitidas**.
- Pruebas nuevas de simulación: **72**; se añadió una prueba de `exists_by_id` en clientes.
- Caso de uso: 21 superadas; repositorio: 5; API: 24; esquemas: 22.
- Migraciones: 1 superada; arquitectura: 7; pricing: 67.
- Ruff check, Ruff format --check, mypy y `pip check`: sin errores.
- Los siete subtotales aprobados y los códigos `201`, `404`, `422` y `500` quedaron cubiertos.
- Sin cambios en `pricing`, sin archivos staged, sin commit, push, PR ni merge.

## 13. Referencias

- [Especificación 003](spec.md)
- [Plan técnico 003](plan.md)
- [Requisitos funcionales](../../requirements/functional-requirements.md)
- [ADR 0002 - Arquitectura](../../adr/0002-architecture.md)
- [Especificación 001 - Alta de clientes](../001-customer-registration/spec.md)
- [Especificación 002 - Precios progresivos](../002-progressive-pricing/spec.md)
- [TASK029 - Preparación de simulaciones](../../../ai-workspace/01-tasks/TASK029-simulations-preparation.md)
- [TASK030 - Cierre de decisiones y contrato](../../../ai-workspace/01-tasks/TASK030-simulations-decisions-and-contract.md)
- [TASK031 - Cierre definitivo de decisiones bloqueantes](../../../ai-workspace/01-tasks/TASK031-simulations-final-decisions.md)
- [TASK032 - Implementación del primer incremento](../../../ai-workspace/01-tasks/TASK032-simulations-implementation.md)
- [Índice de trazabilidad](../../../ai-workspace/README.md)
