# TASK030 — Cierre de decisiones y contrato del primer incremento de simulaciones

| Campo | Valor |
| --- | --- |
| ID | TASK030 |
| Título | Cierre de decisiones y contrato del primer incremento de simulaciones |
| Estado | **Completada (documentación); cuatro decisiones aprobadas; sin implementación** |
| Fecha | 2026-11-16 |
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
| Cambios locales | `ai-workspace/README.md` modificado; `TASK029` y `docs/specs/003-simulations/` sin seguimiento |
| Archivos staged | Ninguno |
| TASK029 | Presente y sin modificar |

Los cinco archivos locales de TASK029 eran:

- `docs/specs/003-simulations/spec.md`
- `docs/specs/003-simulations/plan.md`
- `docs/specs/003-simulations/tasks.md`
- `ai-workspace/01-tasks/TASK029-simulations-preparation.md`
- `ai-workspace/README.md`

### 1.2. Estado final

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/simulations` |
| `HEAD` | `9cd553fff035de640e12a5eb5530f0791ed7b9e7` |
| Cambios | Cuatro archivos documentales modificados y un registro nuevo |
| Archivos staged | Ninguno |
| Commit, push, PR, merge | No ejecutados |
| `main` local | Sin cambios |
| TASK029 | Preservado; hash verificado |
| TASK031 | No creado |

El estado local contiene los cinco archivos de TASK029 más el nuevo registro TASK030: seis archivos en total.

## 2. Archivos creados y modificados

| Archivo | Acción |
| --- | --- |
| `docs/specs/003-simulations/spec.md` | Modificado: decisiones aprobadas, contrato, modelo, trazabilidad y pendientes. |
| `docs/specs/003-simulations/plan.md` | Modificado: arquitectura, secuencia incremental y puertas de decisión. |
| `docs/specs/003-simulations/tasks.md` | Modificado: tareas futuras y decisiones bloqueantes. |
| `ai-workspace/README.md` | Modificado: índice y estado de TASK030. |
| `ai-workspace/01-tasks/TASK030-simulations-decisions-and-contract.md` | Creado: este informe. |

No se modificaron `TASK029`, SPEC-001, SPEC-002, requisitos generales, código, pruebas, migraciones, dependencias ni configuración.

## 3. Decisiones aprobadas y correspondencia

| Decisión TASK030 | Identificador conservado | Reflejo documental |
| --- | --- | --- |
| SIM-P01: persistencia | SIM-P01 | Se persiste `id`, `customer_id`, `user_count`, `user_subtotal_eur` y `created_at`; se prevén repositorio y migración. |
| SIM-P02: cliente obligatorio | SIM-P02 | `customer_id` obligatorio, comprobación de existencia y clave foránea. |
| SIM-P03: cadena decimal exacta | SIM-P08 / Q-08 | `user_subtotal_eur` se serializa como cadena decimal; no se usa `float` ni número JSON. |
| SIM-P04: solo coste de usuarios | SIM-P17 | Se excluyen almacenamiento, API, impuestos, divisas, descuentos, periodicidad y planes nuevos. |

La instrucción TASK030 usa `SIM-P03` y `SIM-P04` con significados distintos de los que ya tenían en SPEC-003. Para no renumerar silenciosamente:

- `SIM-P03` sigue siendo la decisión pendiente sobre el plan.
- `SIM-P04` sigue siendo la decisión pendiente sobre Q-15.
- La representación monetaria se identifica como `SIM-P08 / Q-08`.
- El alcance inicial se registra como `SIM-P17`, etiqueta nueva.

Esta correspondencia queda documentada en SPEC-003, sección 1.

## 4. Contrato HTTP propuesto

### 4.1. Entrada

```json
{
  "customer_id": "00000000-0000-0000-0000-000000000000",
  "user_count": 100
}
```

- `customer_id` es UUID, no entero: es el tipo real de `customers.id` y de `CustomerResponse`.
- `user_count` es entero estricto, mínimo 1, sin coerciones.
- No se aceptan `plan`, `storage`, `api_calls`, `display_currency` ni `persist` en el primer incremento.

### 4.2. Salida

```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "customer_id": "00000000-0000-0000-0000-000000000000",
  "user_count": 100,
  "user_subtotal_eur": "670.00",
  "created_at": "2026-11-16T16:00:00Z"
}
```

- `id` y `customer_id` son UUID.
- `created_at` es ISO 8601 UTC. Pydantic v2 serializa un `datetime` UTC con sufijo `Z`, coherente con la API actual.
- `user_subtotal_eur` es cadena decimal exacta.
- No se incluye `base_amount_eur`, porque Q-16 no ha definido una magnitud distinta y el primer incremento solo calcula el subtotal de usuarios.
- No se incluye `plan` ni campos de almacenamiento, API, impuestos o divisas.

### 4.3. Estados y errores

| Situación | Propuesta |
| --- | --- |
| Creación persistida | `201 Created`. |
| Cuerpo o `user_count` inválido | `422` con `application/problem+json`. |
| Cliente inexistente | `404` con `application/problem+json`; propuesto, pendiente de aprobación. |
| Cliente mal formado | `422`. |
| Error interno | `500` con `application/problem+json`. |

No se emite `Location` mientras no exista un endpoint de lectura aprobado. La API de clientes tampoco emite `Location`. El `404` requiere un manejador de aplicación o una respuesta problem+json explícita; el manejador actual no lo cubre y el título genérico de `422` está redactado para clientes.

## 5. Modelo de datos conceptual

Tabla `simulations`:

| Columna | Tipo propuesto | Restricción |
| --- | --- | --- |
| `id` | UUID | Clave primaria, no nula. |
| `customer_id` | UUID | No nulo; clave foránea a `customers.id`. |
| `user_count` | Entero | No nulo; `>= 1`. |
| `user_subtotal_eur` | Texto decimal | No nulo; cadena canónica exacta. |
| `created_at` | Fecha/hora UTC | No nulo. |

No se añaden `plan`, `storage`, `api_calls`, impuestos, divisa, tasa, `base_amount_eur`, versión de tarifa ni campos de edición. No se define recálculo histórico: el importe persistido es el valor calculado en la creación.

SQLite no aplica claves foráneas por defecto. La implementación futura deberá declarar la FK, activar `PRAGMA foreign_keys=ON` o garantizar integridad equivalente, y probar que no se crean simulaciones huérfanas.

## 6. Almacenamiento exacto de importes

| Alternativa | Valoración |
| --- | --- |
| Texto decimal canónico | **Recomendado.** Exacto, independiente de SQLite, coincide con la representación HTTP y no requiere aritmética SQL. |
| Entero de unidades menores | Exacto, pero presupone escala 2 y una conversión; menos flexible para precisión futura. |
| `Numeric` | Semántico, pero SQLite no tiene decimal nativo; exige probar el viaje de ida y vuelta y el driver. |
| `float` | Prohibido. |

La propuesta es `TEXT`/`Text` con cadena canónica, mapeada a `Decimal` al leer. La decisión definitiva queda pendiente de confirmación técnica (SIM-P13), pero no se acepta `float`.

La normalización textual propuesta usa punto decimal, sin separador de miles, sin exponente y con dos decimales para los valores actuales (`10.00`, `100.00`, `108.00`, `420.00`, `425.00`, `670.00`). Es representación, no redondeo comercial. Si una fase futura produce más de dos decimales, no se redondeará silenciosamente; se conservará la precisión o se pedirá una decisión adicional.

## 7. Cambio mínimo en `CustomerRepository`

Se recomienda añadir:

```python
def exists_by_id(self, customer_id: UUID) -> bool:
    """Comprueba si existe un cliente por su identificador."""
```

Ventajas:

- Evita cargar la entidad completa.
- Es suficiente porque el plan no se usa en el cálculo.
- Mantiene la dependencia de la aplicación hacia un puerto de dominio.

`get_by_id` solo sería necesario si una fase futura requiere el plan u otros datos del cliente. No se modifica ninguna interfaz en TASK030.

## 8. Matriz de conflictos y trazabilidad

La matriz completa está en [SPEC-003, sección 11](../../docs/specs/003-simulations/spec.md#11-matriz-de-trazabilidad). Resumen:

| Referencia | Estado | Conflicto o brecha |
| --- | --- | --- |
| FR-03 | Alineado con SIM-P01/SIM-P02. | Ninguno. |
| FR-04 | Parcial: solo usuarios. | No se registran almacenamiento ni llamadas; Q-15 pendiente. |
| FR-06 | Diferido. | No se calculan impuestos; Q-05/Q-16 pendientes. |
| FR-08 | Diferido. | La persistencia habilita historial, pero no hay endpoint de lectura. |
| FR-10 | Diferido. | No se implementan divisas; Q-06/Q-07 pendientes. |
| FR-11 | Parcial. | Se guarda el subtotal, no el importe base ni divisa/tasa; Q-16/Q-17 pendientes. |
| Q-08 | Formato HTTP aprobado. | Normalización a dos decimales es propuesta, no redondeo. |
| Q-09 | Pendiente. | No se implementa edición. |
| Q-12 | Dominio sin máximo; API/UI pendientes. | Riesgo de entradas enormes. |
| Q-15 | Pendiente. | Bloquea FR-04 completo. |
| Q-16 | Pendiente. | No se usa `base_amount_eur`. |
| Q-17 | Pendiente. | No aplica sin divisas. |

No se modifican los requisitos generales para ocultar estas brechas. El primer incremento es una entrega parcial documentada.

## 9. Decisiones restantes

### 9.1. Bloqueantes para cerrar el primer incremento

| ID | Pregunta | Recomendación |
| --- | --- | --- |
| SIM-P09 / Q-12 | Máximo de API/UI. | Aprobar un límite de API y un rango de UI; no cambiar el dominio. |
| SIM-P12 | Cliente inexistente. | `404` con `problem+json`. |
| SIM-P13 | Almacenamiento exacto de `Decimal`. | Texto decimal canónico con prueba de ida y vuelta. |
| SIM-P15 | Prefijo de versión. | Mantener `/simulations` hasta una decisión global. |

### 9.2. Diferibles

| ID | Pregunta | Tratamiento |
| --- | --- | --- |
| SIM-P03 | Plan como contexto. | Se omite; revisar si se necesita en el futuro. |
| SIM-P04 / Q-15 | Almacenamiento y API. | Diferir; no inventar unidades ni cargos. |
| SIM-P05 / Q-16 | Importe base. | Mantener `user_subtotal_eur` separado. |
| SIM-P06 / Q-05 | Impuestos. | Diferir. |
| SIM-P07 / Q-06, Q-07, Q-17 | Divisas y tasas. | Diferir. |
| SIM-P10 / Q-09 | Inmutabilidad/edición. | No exponer edición; decidir antes del historial. |
| SIM-P11 | Endpoints de lectura. | Diferir; no emitir `Location`. |
| SIM-P14 | Impuesto histórico. | Diferir. |
| SIM-P16 | Idempotencia. | Decidir si los reintentos deben deduplicar. |

No se aprueba ninguna de estas decisiones por inferencia.

## 10. Plan de implementación incremental

1. **Fase 0:** cerrar SIM-P09, SIM-P12, SIM-P13 y SIM-P15; confirmar la aceptación de la brecha FR-04/06/10/11.
2. **Fase 1:** dominio y aplicación; entidad, puerto, DTOs, errores y caso de uso con pricing.
3. **Fase 2:** persistencia; modelo, mapeadores, repositorio, migración, FK y pruebas exactas.
4. **Fase 3:** clientes; `exists_by_id` y pruebas.
5. **Fase 4:** presentación y bootstrap; esquemas, router, serialización, errores y composición.
6. **Fase 5:** pruebas y calidad; Pytest, Ruff, mypy, regresión y arquitectura.
7. **Fase 6:** auditoría independiente y publicación mediante tarea específica autorizada.

No se inicia ninguna fase en TASK030. No se crea TASK031.

## 11. Validaciones ejecutadas

| Comprobación | Resultado |
| --- | --- |
| `git status --short` | **6 archivos locales:** `ai-workspace/README.md` modificado; TASK029, TASK030 y los tres documentos de SPEC-003 sin seguimiento. |
| `git diff --check` | **OK; sin errores en archivos rastreados.** |
| Espacios y tabulaciones finales | **0 problemas en los seis archivos.** |
| Enlaces relativos | **138 enlaces comprobados; 0 rotos.** |
| Referencias FR, Q y SIM-P | **0 identificadores FR/CON/ASM/Q ausentes** en los cuatro documentos de análisis. **17 etiquetas `SIM-P01` a `SIM-P17` presentes**, sin etiquetas adicionales; la correspondencia con TASK030 está documentada. |
| Solo archivos autorizados | **Sí:** SPEC-003, plan, tareas, README y TASK030; TASK029 preservado. |
| Archivos staged | **Ninguno.** |
| Cambios en código/configuración | **Ninguno** en `backend/src`, `backend/tests`, `backend/migrations`, `backend/pyproject.toml` o `backend/requirements.lock`. |
| TASK029 sin modificar | **Sí:** hash `9deb8ede918528df388a1910547d8b951145bd0f`, idéntico al inicial. |
| Pytest, Ruff, mypy | **No ejecutados:** TASK030 no modifica código. |

## 12. Riesgos pendientes

- El primer incremento no satisface FR-04, FR-06, FR-10 ni FR-11 completos.
- No hay máximo de API aprobado; una entrada enorme puede consumir CPU o memoria.
- SQLite puede perder exactitud si se usa `Numeric` o `float`; se recomienda texto decimal.
- SQLite no aplica claves foráneas por defecto.
- Los manejadores de error están acoplados a clientes.
- No hay idempotencia; los reintentos pueden duplicar simulaciones.
- No hay endpoint de lectura; lo persistido no se puede consultar todavía por API.
- SPEC-001 y SPEC-002 siguen conteniendo afirmaciones históricas de «cambios locales no publicados»; no se modifican sin autorización.
- No hay CI; las comprobaciones son locales.

## 13. Recomendación para TASK031

TASK031 debería ser una **tarea breve de cierre de las decisiones bloqueantes** (SIM-P09, SIM-P12, SIM-P13 y SIM-P15) y de aceptación explícita de la entrega parcial de FR-04/06/10/11. Solo después debería autorizarse una tarea de implementación separada, con alcance y archivos concretos.

No se ha creado TASK031, no se ha iniciado la implementación y no se ha publicado ningún cambio.

## 14. Referencias

- [Especificación 003](../../docs/specs/003-simulations/spec.md)
- [Plan técnico 003](../../docs/specs/003-simulations/plan.md)
- [Tareas 003](../../docs/specs/003-simulations/tasks.md)
- [Requisitos funcionales](../../docs/requirements/functional-requirements.md)
- [ADR 0001 - Stack tecnológico](../../docs/adr/0001-technology-stack.md)
- [ADR 0002 - Arquitectura](../../docs/adr/0002-architecture.md)
- [Especificación 001 - Alta de clientes](../../docs/specs/001-customer-registration/spec.md)
- [Especificación 002 - Precios progresivos](../../docs/specs/002-progressive-pricing/spec.md)
- [TASK029 - Preparación de simulaciones](TASK029-simulations-preparation.md)
- [Índice de trazabilidad](../README.md)
