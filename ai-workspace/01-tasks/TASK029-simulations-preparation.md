# TASK029 — Análisis y especificación del módulo de simulaciones

| Campo | Valor |
| --- | --- |
| ID | TASK029 |
| Título | Análisis y especificación del módulo de simulaciones |
| Estado | **Completada (análisis y documentación); decisiones pendientes; sin implementación** |
| Fecha | 2026-11-16 |
| Participantes | Propietario (instrucción y decisiones) / OpenCode + DeepSeek (análisis, documentación y registro) |
| Autorización Git | **Ninguna publicación**: no `git add`, commit, push, PR ni merge. Solo se creó la rama local de trabajo. |

## 1. Estado Git inicial y final

### 1.1. Estado inicial

| Comprobación | Resultado |
| --- | --- |
| Rama activa | `feature/progressive-pricing` |
| `HEAD` | `3439d1abe49a18381a15e857a8cdcf57992178d6` |
| `git status --short` | Limpio; 0 entradas |
| Cambios staged | Ninguno |
| Rama local `feature/simulations` | No existía |
| Rama remota `feature/simulations` | No existía |
| `main` local | `8371f9f608ce6e06984cc501d8240e1b7edf34d5` |

No se descartó ni sobrescribió trabajo existente.

### 1.2. Preparación

Se ejecutó `git fetch origin`. El fetch actualizó `origin/main` de `88816201a01677760a68ded5b8be21565bf737fc` a `9cd553fff035de640e12a5eb5530f0791ed7b9e7`.

Se verificó el commit de merge del PR #4:

| Comprobación | Resultado |
| --- | --- |
| Commit | `9cd553fff035de640e12a5eb5530f0791ed7b9e7` |
| Tipo de objeto | `commit` |
| Padres | `88816201a01677760a68ded5b8be21565bf737fc` y `3439d1abe49a18381a15e857a8cdcf57992178d6` |
| Mensaje | `Merge pull request #4 from Toni2Morales/feature/progressive-pricing` |
| Autor | `Antonio Morales <107318721+Toni2Morales@users.noreply.github.com>` |
| Fecha | `2026-11-16 17:15:26 +0100` |
| Ancestro de `origin/main` | Sí; `origin/main` apunta exactamente a ese commit |
| PR | [#4](https://github.com/Toni2Morales/SaaS-O-Matic/pull/4) |
| Merge ejecutado por el agente | No; lo ejecutó el propietario |

Se creó la rama de trabajo desde `origin/main`:

```text
git switch -c feature/simulations origin/main
```

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/simulations` |
| `HEAD` | `9cd553fff035de640e12a5eb5530f0791ed7b9e7` |
| `origin/main` | `9cd553fff035de640e12a5eb5530f0791ed7b9e7` |
| `main` local | Sin modificar; `8371f9f608ce6e06984cc501d8240e1b7edf34d5` |
| Operaciones de publicación | Ninguna |

### 1.3. Estado final

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/simulations` |
| `HEAD` | `9cd553fff035de640e12a5eb5530f0791ed7b9e7` |
| Cambios | Tres documentos nuevos, este informe y `ai-workspace/README.md` modificado |
| Cambios staged | Ninguno |
| `git add` / commit / push / PR / merge | No ejecutados |
| `main` local | Sin cambios |
| TASK030 | No creado |

## 2. Confirmación del merge del PR #4

El PR #4 fue fusionado por el propietario. El commit de merge verificado es `9cd553fff035de640e12a5eb5530f0791ed7b9e7`, cuyos padres son el `main` anterior (`8881620`) y la rama `feature/progressive-pricing` (`3439d1a`). El commit es ancestro de `origin/main` y `origin/main` apunta exactamente a él.

TASK028 no generó un archivo de registro en el repositorio. La evidencia de la publicación es el PR #4 y el commit de merge. El agente no ejecutó el merge.

## 3. Documentos y código consultados

### 3.1. Documentación

- [`AGENTS.md`](../../AGENTS.md).
- [`docs/requirements/functional-requirements.md`](../../docs/requirements/functional-requirements.md): FR-03, FR-04, FR-05, FR-06, FR-08, FR-09, FR-10, FR-11, CON-03, CON-04, CON-06, ASM-01 a ASM-07, Q-05, Q-06, Q-07, Q-09, Q-12, Q-15, Q-16 y Q-17.
- [`docs/adr/0001-technology-stack.md`](../../docs/adr/0001-technology-stack.md).
- [`docs/adr/0002-architecture.md`](../../docs/adr/0002-architecture.md).
- [`docs/specs/001-customer-registration/spec.md`](../../docs/specs/001-customer-registration/spec.md), [`plan.md`](../../docs/specs/001-customer-registration/plan.md) y [`tasks.md`](../../docs/specs/001-customer-registration/tasks.md).
- [`docs/specs/002-progressive-pricing/spec.md`](../../docs/specs/002-progressive-pricing/spec.md), [`plan.md`](../../docs/specs/002-progressive-pricing/plan.md) y [`tasks.md`](../../docs/specs/002-progressive-pricing/tasks.md).
- [`docs/process/ai-assisted-development.md`](../../docs/process/ai-assisted-development.md).
- [`ai-workspace/README.md`](../README.md).
- [`TASK024`](TASK024-progressive-pricing-preparation.md), [`TASK025`](TASK025-progressive-pricing-implementation.md) y [`TASK027`](TASK027-progressive-pricing-audit-fixes.md).
- [`TASK023`](TASK023-customer-publication.md) como antecedente de publicación y trazabilidad.

### 3.2. Código y pruebas

- `backend/src/saas_o_matic/domain/pricing/`: `services.py`, `schedule.py`, `value_objects.py` y `errors.py`.
- `backend/src/saas_o_matic/domain/customers/`: `entities.py`, `value_objects.py`, `ports.py` y `errors.py`.
- `backend/src/saas_o_matic/application/customers/`: `use_cases.py`, `dto.py`, `errors.py` y `catalogs.py`.
- `backend/src/saas_o_matic/infrastructure/customers/`: `models.py`, `mappers.py` y `repositories.py`.
- `backend/src/saas_o_matic/infrastructure/database.py`.
- `backend/src/saas_o_matic/presentation/`: `app.py`, `problems.py`, `customers/router.py`, `customers/schemas.py` y `customers/dependencies.py`.
- `backend/src/saas_o_matic/bootstrap/`: `main.py` y `customers.py`.
- `backend/migrations/versions/0001_create_customers.py`.
- `backend/tests/test_architecture.py`, `test_customer_api.py`, `test_customer_use_case.py`, `test_customer_schemas.py`, `test_customer_repository.py`, `test_problems.py`, `test_pricing.py`, `test_migrations.py` y `conftest.py`.
- `backend/pyproject.toml` y `backend/requirements.lock` como contexto de stack; no se modificaron.

## 4. Requisitos confirmados

### 4.1. Reglas y decisiones aprobadas

- Q-02: mínimo 1 usuario; cero se rechaza.
- PP-Q-01: solo enteros positivos estrictos; se rechazan cero, negativos, no enteros y `bool`, sin coerciones.
- Q-08: cálculo exacto con `Decimal` en EUR, sin `float` ni redondeo de negocio. El formato de salida sigue pendiente.
- Q-12: sin máximo comercial de usuarios en el dominio; el límite de UI/API se decide por separado.
- D-02: el catálogo MVP contiene únicamente `standard`; el plan es obligatorio en el cliente, no modifica los tramos y no añade precios o prestaciones.
- CON-03: EUR es la divisa base.
- CON-04: almacenamiento y llamadas a la API se registran y muestran, pero no generan cargos.
- CON-06: la aplicación estima costes; no es un sistema de cobro.

### 4.2. Requisitos fuente que no equivalen a diseño aprobado

FR-03 exige crear y persistir simulaciones asociadas a un cliente. FR-04 exige registrar usuarios, almacenamiento y llamadas estimadas. FR-06 exige incluir el impuesto aplicable. FR-08 exige historial en el detalle del cliente. FR-10 y FR-11 exigen conversiones de divisa y persistencia de sus metadatos. Estos requisitos están documentados, pero la validación global de los requisitos sigue pendiente y no se ha aprobado un modelo concreto de simulación.

## 5. Ambigüedades y contradicciones detectadas

| Referencia | Ambigüedad o contradicción | Tratamiento |
| --- | --- | --- |
| FR-03 frente a la alternativa efímera | FR-03 exige persistir; una simulación efímera contradice el texto. | Se documentan ambas; A solo sería viable si el propietario cambia FR-03. No se elige. |
| Q-16 | La pregunta global pide la magnitud del importe base, no decide por sí sola si hay persistencia. | Se separa la decisión de persistencia (SIM-P01) de la magnitud (SIM-P05/Q-16). |
| FR-04 / Q-15 | Se exige registrar almacenamiento y llamadas, pero no hay unidades ni periodo. | El contrato de FR-04 queda bloqueado; no se inventan unidades. |
| FR-06 / Q-05 | Se exige impuesto por país, pero no hay tabla, fuente ni vigencia. | No se implementa impuesto; se registra como decisión pendiente. |
| FR-10 / FR-11 / Q-06, Q-07, Q-17 | Se exigen divisas y metadatos de tasa, pero faltan proveedor, lista y obligatoriedad. | No se implementa conversión; se proponen campos condicionados. |
| FR-11 y reproducibilidad del impuesto | FR-11 permite reconstruir la conversión, pero no garantiza reconstruir un impuesto si cambian las reglas. | Se registra como riesgo SIM-P14; no se añade un campo no requerido. |
| Q-09 | No se decide si el historial es inmutable o editable. | No se diseñan `PATCH`, `PUT` ni `DELETE`; se recomienda inmutabilidad, sin aprobarla. |
| Q-12 | El dominio no tiene máximo, pero API y UI lo necesitan. | Se separan dominio, API y UI; no se fija un valor. |
| Q-08 | El cálculo es exacto, pero el formato de serialización no está decidido. | Se comparan cadena decimal, entero de céntimos y número JSON; no se aprueba ninguno. |
| Plan `standard` | El cliente ya tiene plan, pero el motor no lo usa. | Se plantean tres alternativas; se recomienda omitirlo del cálculo, sin aprobarlo. |
| FR-08 / endpoints de lectura | El historial exige lectura, pero no hay endpoints aprobados. | Se condicionan a persistencia y a SIM-P11. |
| Sin autenticación | La asociación con un cliente no demuestra propiedad ni autorización. | Se documenta que la relación sería solo referencial; no se inventa multi-tenancy. |
| `presentation/problems.py` | Los manejadores están acoplados a errores de clientes y el `422` dice «Datos de cliente no válidos». | Se requiere extensión futura; no se modifica ahora. |
| `CustomerRepository` | No existe lectura por identificador. | Se propone `exists_by_id` o `get_by_id` como cambio futuro, condicionado. |
| NFR-02 | Propone `/api/v1`, pero las rutas actuales no lo usan. | No se introduce prefijo sin decisión global. |
| SPEC-001 y SPEC-002 | Afirman que los cambios locales no están publicados, aunque el PR #3 y el PR #4 ya se fusionaron. | Se registra la desactualización; no se modifican esas especificaciones sin autorización. |
| Idempotencia | No hay requisito; un reintento de `POST` podría duplicar simulaciones persistidas. | Se registra SIM-P16; no se inventa una clave de idempotencia. |

## 6. Alternativas de persistencia

| Alternativa | Ventajas | Coste | API | Modelo de datos | Consulta posterior |
| --- | --- | --- | --- | --- | --- |
| A. Efímera | Baja complejidad; sin migración ni repositorio; útil para vista previa. | Bajo. | `200`; sin `id` ni `created_at`. | Sin tabla de simulación. | No permite historial. |
| B. Persistida | Alinea con FR-03, FR-08 y FR-11; permite historial y reconstrucción. | Medio. | `201` con `Location`; `id` y `created_at`. | Tabla, clave foránea, repositorio y migración. | Sí, con endpoints de lectura aprobados. |
| C. Híbrida | Combina cálculo rápido y guardado opcional. | Medio-alto. | Debe definirse `200`/`201` o dos operaciones. | Modelo condicionado a guardar. | Solo para registros guardados. |

No se elige ninguna. La recomendación técnica es B si FR-03 se mantiene; A o C exigirían una decisión funcional explícita.

## 7. Alternativas de relación con clientes

| Alternativa | Efecto | Ventajas | Inconvenientes |
| --- | --- | --- | --- |
| A. Obligatorio | `customer_id` requerido; cliente inexistente produce error. | Alinea con FR-03 y FR-08; integridad clara. | Requiere consulta de cliente y decidir `404`/`422`. |
| B. Sin cliente | No hay `customer_id`. | Contrato mínimo; calculadora rápida. | Contradice FR-03; no hay historial por cliente. |
| C. Opcional | `customer_id` puede faltar. | Cubre ambos usos. | Ambigüedad de historial y clave foránea opcional. |

No se elige ninguna. A es la recomendación si FR-03 se mantiene. No se definen propiedad, autenticación ni multitenancy.

## 8. Propuesta de contrato HTTP

### 8.1. Endpoint

```text
POST /simulations
```

Sin prefijo de versión. No se asume `201` si no se decide persistencia. La tabla completa de campos y estados está en [SPEC-003](../../docs/specs/003-simulations/spec.md), secciones 7.2 a 7.5.

### 8.2. Entrada candidata

| Campo | Tipo | Estado |
| --- | --- | --- |
| `customer_id` | UUID | Obligatorio, opcional o ausente según SIM-P02. |
| `user_count` | Entero estricto | Necesario para el motor; `>= 1`; sin coerciones; máximo pendiente. |
| `storage` | Objeto o número | Pendiente de Q-15. |
| `api_calls` | Objeto o número | Pendiente de Q-15. |
| `plan` | `standard` | Pendiente de SIM-P03; no se propone por defecto. |
| `display_currency` | Código ISO | Pendiente de Q-07; fuera de la primera entrega propuesta. |
| `persist` | Booleano | Solo para el modo híbrido; pendiente. |

### 8.3. Salida candidata

| Campo | Estado |
| --- | --- |
| `id` | Solo si hay persistencia. |
| `customer_id` | Si hay asociación. |
| `user_count` | Propuesto. |
| `user_subtotal_eur` | Cálculo aprobado; serialización pendiente. |
| `base_amount_eur` | Pendiente de Q-16. |
| `created_at` | Solo si hay persistencia. |
| `storage` / `api_calls` | Pendiente de Q-15. |
| `plan` | Pendiente de SIM-P03. |
| Campos de divisa y tasa | Pendientes de FR-10/FR-11 y Q-06/Q-07/Q-17. |

### 8.4. Estados y errores

| Situación | Propuesta |
| --- | --- |
| Persistida | `201 Created` con `Location`. |
| Efímera | `200 OK`. |
| Híbrida | `200` o `201`, pendiente de semántica. |
| Entrada inválida | `422` con `application/problem+json`. |
| Cliente inexistente | `404` recomendado; pendiente SIM-P12. |
| Cliente mal formado | `422`. |
| Error interno | `500` con `application/problem+json`. |

No se inventa un `409`. El esquema `ProblemDetails` existente se reutiliza, pero los manejadores de simulación necesitarán mensajes propios.

## 9. Alternativas de representación monetaria

| Alternativa | Ventajas | Inconvenientes | Compatibilidad con Angular |
| --- | --- | --- | --- |
| Cadena decimal exacta, por ejemplo `"108.00"` | No pierde precisión; el contrato es explícito; fácil de comparar en pruebas. | Angular debe formatear y no debe convertirlo a `number` sin control. | Alta si se usa un tipo string o una librería decimal. |
| Entero de céntimos, por ejemplo `10800` | Exacto y compacto; evita decimales en JSON. | Presupone escala 2 y un redondeo no aprobado; futuras tasas o impuestos pueden necesitar más precisión. | Alta, pero requiere conversión y formato en el cliente. |
| Número JSON, por ejemplo `108.00` | Lectura directa. | JavaScript lo interpreta como `number` binario; riesgo de precisión; no es adecuado para dinero. | Riesgo alto. |

No se aprueba ninguno. La recomendación técnica es la cadena decimal exacta, pendiente de Q-08/SIM-P08 y de una prueba con Angular. No se introduce conversión de divisas ni redondeo nuevo.

## 10. Propuesta arquitectónica

| Capa | Propuesta | Condición |
| --- | --- | --- |
| `domain/simulations` | Entidad, invariantes y puerto de repositorio. | Solo si la persistencia o las invariantes lo justifican. |
| `application/simulations` | `CreateSimulation`, DTOs, errores y orquestación. | Siempre que haya caso de uso. |
| `infrastructure/simulations` | Modelo SQLAlchemy, mapeador y repositorio. | Solo si hay persistencia. |
| `presentation/simulations` | Esquemas, router y dependencias HTTP. | Siempre que haya endpoint. |
| `bootstrap` | Composición del caso de uso y de la sesión. | Siempre que haya endpoint. |

El caso de uso importará `calculate_user_subtotal` desde `saas_o_matic.domain.pricing.services` y no duplicará la tabla de tramos. No se pasa el plan al motor. La presentación no importa dominio. La consulta de cliente, si se aprueba, requiere ampliar `CustomerRepository` con `exists_by_id` o `get_by_id`. El composition root compartirá la sesión por petición.

## 11. Modelo de datos condicionado

| Campo | Tipo candidato | Condición |
| --- | --- | --- |
| `id` | UUID | Persistencia. |
| `customer_id` | UUID con clave foránea | Relación A o C. |
| `user_count` | Entero | Siempre; `>= 1`. |
| `user_subtotal_eur` | `Decimal` | Resultado del motor. |
| `base_amount_eur` | `Decimal` | Q-16. |
| `plan` | `standard` | Pendiente SIM-P03. |
| `storage_quantity` / `storage_unit` | Pendientes | Q-15. |
| `api_calls_quantity` / `api_calls_unit` | Pendientes | Q-15. |
| `created_at` | Fecha/hora UTC | Persistencia. |
| `display_currency`, `exchange_rate`, `rate_date`, `rate_source` | Pendientes | FR-10/FR-11, Q-06/Q-07/Q-17. |

No se elige un tipo de columna definitivo. Para SQLite se comparan cadena decimal canónica, entero de unidades menores y `Numeric`; se exige una prueba de ida y vuelta exacta. No se usa `float`. No se crean tablas ni migraciones en TASK029.

## 12. Plan de pruebas

### 12.1. Obligatorias

- Seis ejemplos de precios a través del caso de uso: 1, 10, 11, 50, 51 y 100 usuarios.
- Entradas inválidas: 0, negativos, decimales, cadenas y `bool`, sin coerciones.
- Contrato HTTP válido y estado acordado.
- Errores `422` y `application/problem+json`.
- Exactitud y serialización monetaria aprobada.
- Arquitectura: `presentation` no importa `domain`; no se modifica el motor.
- Regresión de clientes, precios, problemas, salud y migraciones.

### 12.2. Condicionadas

- Cliente existente, inexistente y ausente.
- Migración, repositorio y recuperación.
- Almacenamiento y llamadas.
- Impuesto y magnitud base.
- Divisa, tasa, fecha y fuente.
- Máximo de API/UI.
- Historial y edición.
- Endpoints de lectura.

No se ejecutaron pruebas en TASK029 porque no se modificó código.

## 13. Decisiones pendientes

| ID | Pregunta | Recomendación técnica | Estado |
| --- | --- | --- | --- |
| SIM-P01 | ¿Persistencia efímera, persistida o híbrida? | B si FR-03 se mantiene. | Pendiente. |
| SIM-P02 | ¿Cliente obligatorio, sin cliente u opcional? | A si FR-03 se mantiene. | Pendiente. |
| SIM-P03 | ¿Plan obligatorio, deducido u omitido? | Omitido para el MVP actual. | Pendiente. |
| SIM-P04 / Q-15 | Unidades y periodo de almacenamiento y API. | Decidir antes del contrato; no inventar cargos. | Pendiente. |
| SIM-P05 / Q-16 | Magnitud del importe base. | Decidir antes del modelo. | Pendiente. |
| SIM-P06 / Q-05 | Fuente y vigencia del impuesto. | No implementar sin fuente autoritativa. | Pendiente. |
| SIM-P07 / Q-06, Q-07, Q-17 | Proveedor, divisas y metadatos de tasa. | Aplazar conversión o decidir todo el paquete. | Pendiente. |
| SIM-P08 / Q-08 | Formato monetario. | Cadena decimal exacta como candidata. | Pendiente. |
| SIM-P09 / Q-12 | Máximo de API y rango de UI. | Guard de API y rango de UI; sin máximo de dominio. | Pendiente. |
| SIM-P10 / Q-09 | Historial inmutable o editable. | Inmutable para trazabilidad. | Pendiente. |
| SIM-P11 | Endpoints de lectura. | Detalle e historial solo si hay persistencia. | Pendiente. |
| SIM-P12 | Cliente inexistente. | `404` con `problem+json`. | Pendiente. |
| SIM-P13 | `Decimal` en SQLite. | Probar exactitud antes de elegir. | Pendiente. |
| SIM-P14 | Impuesto histórico. | Decidir si el historial debe ser auditable. | Pendiente. |
| SIM-P15 | Prefijo `/api/v1`. | Mantener `/simulations` hasta decisión global. | Pendiente. |
| SIM-P16 | Idempotencia. | Decidir si los reintentos pueden duplicar. | Pendiente. |

Los identificadores `SIM-Pxx` son etiquetas de revisión de TASK029, no decisiones aprobadas ni renumeración de Q-01 a Q-17.

## 14. Archivos creados y modificados

| Archivo | Acción | Contenido |
| --- | --- | --- |
| `docs/specs/003-simulations/spec.md` | Creado | Contexto, requisitos, alternativas, contrato, arquitectura, modelo condicionado, validaciones, pruebas, riesgos y decisiones. |
| `docs/specs/003-simulations/plan.md` | Creado | Secuencia, dependencias, módulos afectados, pruebas, riesgos y puntos de control. |
| `docs/specs/003-simulations/tasks.md` | Creado | Desglose de tareas futuras y puertas de decisión. |
| `ai-workspace/01-tasks/TASK029-simulations-preparation.md` | Creado | Este informe. |
| `ai-workspace/README.md` | Modificado | Índice de TASK029, publicación del PR #4 y estado actualizado. |

No se modificaron archivos de código, pruebas, dependencias, migraciones, configuración, modelos de clientes, routers, esquemas Pydantic ni bootstrap.

## 15. Validaciones ejecutadas

| Comprobación | Resultado real |
| --- | --- |
| `git diff --check` | **OK; sin errores en archivos rastreados.** |
| Espacios o tabulaciones finales en los cinco archivos | **0 problemas.** |
| Enlaces relativos de los cinco archivos | **127 enlaces comprobados; 0 enlaces rotos.** |
| Coherencia de referencias FR, CON, ASM y Q | **0 identificadores ausentes** en los cuatro documentos de análisis; las referencias existen en los requisitos o son etiquetas locales `SIM-Pxx` identificadas como tales. |
| Solo los cinco archivos autorizados | **Sí:** `docs/specs/003-simulations/spec.md`, `plan.md`, `tasks.md`, `ai-workspace/01-tasks/TASK029-simulations-preparation.md` y `ai-workspace/README.md`. |
| Archivos staged | **Ninguno.** |
| Cambios en `backend/src`, `backend/tests`, `backend/migrations`, `backend/pyproject.toml` o `backend/requirements.lock` | **Ninguno.** |
| Pytest, Ruff, mypy | **No ejecutados:** TASK029 no modifica código. |

## 16. Recomendación para TASK030

TASK030 debería ser una **tarea de cierre de decisiones y aprobación de SPEC-003**, no una implementación directa. Debería:

1. Resolver SIM-P01 a SIM-P16, empezando por persistencia, relación con cliente, consumo, importe base, formato monetario y máximo.
2. Confirmar si se mantiene FR-03 y si se acepta una entrega parcial sin impuestos o divisas.
3. Aprobar o corregir el contrato HTTP y el modelo condicionado.
4. Autorizar después una tarea de implementación separada, con alcance y archivos concretos.

No se ha creado TASK030, no se ha iniciado la implementación y no se ha publicado ningún cambio.

## 17. Referencias

- [Especificación 003](../../docs/specs/003-simulations/spec.md)
- [Plan técnico 003](../../docs/specs/003-simulations/plan.md)
- [Tareas 003](../../docs/specs/003-simulations/tasks.md)
- [Requisitos funcionales](../../docs/requirements/functional-requirements.md)
- [ADR 0001 - Stack tecnológico](../../docs/adr/0001-technology-stack.md)
- [ADR 0002 - Arquitectura](../../docs/adr/0002-architecture.md)
- [Especificación 001 - Alta de clientes](../../docs/specs/001-customer-registration/spec.md)
- [Especificación 002 - Precios progresivos](../../docs/specs/002-progressive-pricing/spec.md)
- [TASK024 - Preparación del motor de precios](TASK024-progressive-pricing-preparation.md)
- [TASK025 - Implementación del motor de precios](TASK025-progressive-pricing-implementation.md)
- [TASK027 - Correcciones del motor de precios](TASK027-progressive-pricing-audit-fixes.md)
- [Índice de trazabilidad](../README.md)
