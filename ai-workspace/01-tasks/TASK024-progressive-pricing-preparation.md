# TASK024 — Preparación del motor de precios progresivos

| Campo | Valor |
| --- | --- |
| ID | TASK024 |
| Título | Especificación y planificación del motor de precios progresivos |
| Estado | **Completada (análisis y documentación); pendiente de aprobación del propietario; sin implementación** |
| Fecha | 2026-11-16 |
| Participantes | Propietario (instrucción y decisiones) / OpenCode + DeepSeek (análisis, documentación y registro) |
| Autorización Git | **Ninguna**: no `git add`, commit, push, PR ni merge. Solo se creó la rama local de trabajo. |

## 1. Objetivo y alcance

Preparar la especificación técnica, el plan y las tareas del motor de cálculo de precios progresivos por número de usuarios.

Esta tarea es exclusivamente de análisis, documentación y planificación. No se implementa código funcional, no se crean endpoints, no se modifica el catálogo `standard`, no se tocan migraciones ni modelos de clientes y no se introducen reglas comerciales nuevas.

## 2. Fuentes consultadas

| Tipo | Referencia | Uso |
| --- | --- | --- |
| Requisitos | [functional-requirements.md](../../docs/requirements/functional-requirements.md) | FR-05, sección 2, CON-03, ASM-02, ASM-03, Q-02, Q-08, Q-12 y D-02. |
| ADR | [0001-technology-stack.md](../../docs/adr/0001-technology-stack.md) | Python 3.13, calidad y divisa base EUR. |
| ADR | [0002-architecture.md](../../docs/adr/0002-architecture.md) | Monolito modular, dominio puro, módulo `pricing` y dependencias. |
| Especificación | [001-customer-registration/spec.md](../../docs/specs/001-customer-registration/spec.md) | D-02 y separación entre plan y precios. |
| Plan y tareas 001 | [plan.md](../../docs/specs/001-customer-registration/plan.md), [tasks.md](../../docs/specs/001-customer-registration/tasks.md) | Convenciones y antecedentes de implementación. |
| Evaluación | [001-repository-assessment.md](../../docs/assessment/001-repository-assessment.md) | Contexto de precisión decimal, redondeo y riesgos. |
| Proceso | [ai-assisted-development.md](../../docs/process/ai-assisted-development.md) | Flujo de especificación, plan, tareas y autorización. |
| Instrucciones | [AGENTS.md](../../AGENTS.md) | Alcance, arquitectura, Git y reglas de parada. |
| Trazabilidad | [ai-workspace/README.md](../README.md) | Índice de tareas, publicaciones y limitaciones. |
| Contexto | [architectural-evolution.md](../00-project-context/architectural-evolution.md) | Evolución y estado arquitectónico. |
| Tareas previas | [TASK020](TASK020-customer-registration-completion.md), [TASK022](TASK022-customer-validation-fix.md), [TASK023](TASK023-customer-publication.md) | Alta de clientes, corrección de `legal_name` y publicación del PR #3. |
| Código | `backend/src/saas_o_matic/`, `backend/tests/test_architecture.py`, `backend/pyproject.toml` | Estado real del backend y reglas de dependencia. |

## 3. Estado Git

### 3.1 Estado inicial

| Comprobación | Resultado |
| --- | --- |
| Rama activa | `feature/customer-registration` |
| `HEAD` | `b11a5dcdc4c04dcf46d35db122ab03f15b1b34da` |
| Árbol de trabajo | Limpio; 0 entradas |
| `git fetch origin` | Ejecutado |
| `origin/main` antes del fetch | `be755a68a52392fd562eb3901e317bc85b1ed8e9` |
| `origin/main` después del fetch | `88816201a01677760a68ded5b8be21565bf737fc` |

### 3.2 Verificación del merge del PR #3

| Comprobación | Resultado |
| --- | --- |
| Commit de merge | `88816201a01677760a68ded5b8be21565bf737fc` |
| Tipo de objeto | `commit` |
| Padres | `be755a68a52392fd562eb3901e317bc85b1ed8e9` y `b11a5dcdc4c04dcf46d35db122ab03f15b1b34da` |
| Autor | `Antonio Morales <107318721+Toni2Morales@users.noreply.github.com>` |
| Fecha | `2026-11-16T15:48:44+01:00` |
| Mensaje | `Merge pull request #3 from Toni2Morales/feature/customer-registration` |
| Ancestro de `origin/main` | Sí; `origin/main` apunta exactamente a ese commit |
| Merge ejecutado por el agente | No; lo ejecutó el propietario |

### 3.3 Rama de trabajo

Se creó `feature/progressive-pricing` desde `origin/main`:

```text
git switch -c feature/progressive-pricing origin/main
```

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/progressive-pricing` |
| `HEAD` | `88816201a01677760a68ded5b8be21565bf737fc` |
| `main` local | No modificada |
| Operaciones Git de publicación | Ninguna |

### 3.4 Estado final

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/progressive-pricing` |
| `HEAD` | `88816201a01677760a68ded5b8be21565bf737fc` |
| Cambios | Solo documentación y trazabilidad; pendiente de revisión |
| `git add` / commit / push / PR / merge | No ejecutados |
| `main` local | Sin cambios |

El estado detallado de archivos y validaciones se registra en las secciones 7 y 8.

## 4. Cierre documental del PR #3

- El PR #3 fue fusionado por el propietario.
- El commit de merge verificado es `88816201a01677760a68ded5b8be21565bf737fc`.
- La funcionalidad de alta de clientes está integrada en `main`.
- El PR #3 publicó 54 archivos y su registro de publicación es [TASK023](TASK023-customer-publication.md).
- El agente no ejecutó el merge.
- Los hallazgos menores m-01 a m-04 de TASK021 siguen pendientes y quedan fuera del alcance de TASK024:

| ID | Estado | Descripción |
| --- | --- | --- |
| m-01 | Pendiente | Validación de tipos de `plan` y `country` en la entidad de dominio. |
| m-02 | Pendiente | Restricciones `CHECK` de país y plan en base de datos. |
| m-03 | Pendiente | Formato de nombres de campo en errores `422`. |
| m-04 | Pendiente | Logging de excepciones `500` en servidor. |

## 5. Análisis de requisitos

### 5.1 Decisiones y requisitos aprobados

| Referencia | Contenido confirmado |
| --- | --- |
| FR-05 | El coste de usuarios se calcula mediante tramos progresivos acumulativos. |
| Requisitos, sección 2 | Tramos: 1–10 a 10,00 EUR/usuario; 11–50 a 8,00 EUR/usuario; más de 50 a 5,00 EUR/usuario. Cada tramo se aplica solo a sus unidades. |
| Requisitos, sección 2 | Ejemplos obligatorios: 1 → 10,00; 10 → 100,00; 11 → 108,00; 50 → 420,00; 51 → 425,00; 100 → 670,00 EUR. |
| CON-03 / ADR 0001 | La divisa base es EUR. |
| ASM-03 / D-02 | Los tramos están en EUR y no dependen del plan contratado. |
| D-02 | El catálogo del MVP contiene únicamente `standard`; el plan no modifica los tramos ni añade precios o prestaciones. |
| CON-04 | No se inventan cargos de almacenamiento ni de API. |
| CON-06 | La aplicación estima costes; no es un sistema de cobro. |
| ADR 0002 | El cálculo de precios pertenece a `domain` y debe poder probarse sin base de datos ni servidor. |

Los seis ejemplos se consideran criterios de aceptación obligatorios para el futuro motor, conforme a la instrucción de TASK024. No se modifican importes ni se introducen descuentos, impuestos, periodicidades, divisas adicionales o prestaciones de planes.

### 5.2 Requisitos documentados pero ambiguos

| Referencia | Contenido | Ambigüedad |
| --- | --- | --- |
| ASM-02 / Q-02 | El número de usuarios es un entero no negativo; el mínimo puede ser 0 o 1. | No está decidido si 0 usuarios es válido. |
| Requisitos, sección 2 | Las entradas negativas o no enteras «deben rechazarse en la validación». | Está bajo casos límite previstos, no bajo criterios cerrados; falta fijar el error y el tratamiento exacto. |
| Q-08 | Debe definirse precisión decimal, ámbito y modo de redondeo. | No hay precisión, modo ni formato de salida aprobados. Los dos decimales son un supuesto provisional. |
| Q-12 | Debe definirse si existe un máximo de usuarios y el rango y paso del control deslizante. | No hay máximo ni rango aprobado. |
| FR-09 | El simulador incluye un control deslizante. | El rango y el paso dependen de Q-12 y no pertenecen al motor puro. |
| Q-16 | Debe decidirse qué magnitud se persiste como importe base. | Fuera del alcance del cálculo puro. |

### 5.3 Decisiones pendientes

| ID | Pregunta | Opciones | Consecuencias | Recomendación técnica |
| --- | --- | --- | --- | --- |
| Q-02 | ¿Se permite 0 usuarios? | A) Rechazar y exigir mínimo 1. B) Permitir y devolver 0,00 EUR. | A evita simulaciones vacías; B obliga a definir si 0 es un resultado válido. | A para el motor, salvo necesidad explícita de escenarios vacíos. No aprobada. |
| PP-Q-01 | ¿Cómo se rechazan negativos y no enteros? | A) Error de validación en dominio. B) Solo tipo estático. C) Truncar o ajustar. | A evita resultados silenciosos; B no protege llamadas dinámicas; C oculta datos inválidos. | A: rechazo explícito, sin coerción. No aprobada. |
| Q-08 | ¿Precisión, redondeo y formato? | A) `Decimal` exacto y formato en la frontera. B) Dos decimales con modo explícito. C) Entero de euros o céntimos. | A conserva exactitud; B fija una regla; C simplifica el contrato. | A para el motor puro; el formato se decide antes de endpoint o persistencia. No aprobada. |
| Q-12 | ¿Existe un máximo de usuarios? | A) Sin máximo en dominio. B) Máximo fijo pendiente de valor. | A evita inventar un límite; B acota la interfaz y las pruebas. | A para el cálculo puro; el límite de UI/API se decide aparte. No aprobada. |

Las recomendaciones no son decisiones aprobadas. `PP-Q-01` es un identificador local de TASK024 y de SPEC-002; no sustituye ni renumera las preguntas globales Q-01 a Q-17.

### 5.4 Estado del código existente

- No existe un paquete `pricing` ni una implementación de precios progresivos en `backend/src`.
- No se encontraron usos de `Decimal`, `precio`, `price`, `tramo`, `round`, `money`, `EUR` ni `simulation` en `backend/src`.
- El backend actual contiene el alta de clientes, el catálogo `standard` y la infraestructura SQLite; no contiene cálculo de precios.
- La prueba `backend/tests/test_architecture.py` ya comprueba que el dominio no importa frameworks ni capas exteriores.

## 6. Diseño técnico propuesto

### 6.1 Enfoque

Implementar el cálculo como dominio puro en `backend/src/saas_o_matic/domain/pricing/`:

- `PricingBand`: límite inferior, límite superior opcional y precio por usuario en EUR.
- `PricingSchedule`: tupla inmutable de tramos con invariantes de continuidad y último tramo abierto.
- `APPROVED_USER_PRICING_SCHEDULE`: única fuente de verdad con los tres tramos aprobados.
- `calculate_user_subtotal(user_count: int) -> Decimal`: función pura que devuelve el subtotal exacto.
- `InvalidUserCount` e `InvalidPricingSchedule`: errores de dominio, el primero pendiente de Q-02/PP-Q-01.

No se proponen capas de aplicación, infraestructura, presentación ni bootstrap para TASK025. No hay persistencia ni endpoint.

### 6.2 Separación de responsabilidades

| Capa | TASK025 |
| --- | --- |
| `domain` | Reglas, tramos, cálculo exacto y errores. |
| `application` | Sin cambios; no hay caso de uso aprobado. |
| `infrastructure` | Sin cambios; no hay persistencia. |
| `presentation` | Sin cambios; no hay endpoint. |
| `bootstrap` | Sin cambios; no hay nueva dependencia que inyectar. |

### 6.3 Representación monetaria

- `Decimal` construido desde cadenas, nunca `float`.
- Sin `quantize()` ni modo de redondeo antes de Q-08.
- Los subtotales aprobados son enteros de euro, por lo que no requieren redondeo.
- Las pruebas comparan valores decimales, no cadenas formateadas.
- La precisión de `Decimal` para cantidades muy grandes queda pendiente de Q-12/Q-08.

### 6.4 Alternativas

| Alternativa | Valoración | Motivo |
| --- | --- | --- |
| Tabla de tramos + iteración genérica | Recomendada | Límites y precios explícitos; invariantes y pruebas más claras. |
| Fórmula directa con constantes | Sencilla | Menos código, pero mezcla límites y cálculo y dificulta cambios futuros. |
| Caso de uso de aplicación ahora | No recomendada | No hay endpoint ni simulación aprobada. |
| Persistencia o configuración de precios | No autorizada | No hay requisito y permitiría cambiar reglas comerciales sin decisión. |

## 7. Archivos creados o modificados

| Archivo | Acción | Contenido |
| --- | --- | --- |
| `docs/specs/002-progressive-pricing/spec.md` | Creado | Especificación, reglas, ejemplos, entradas/salidas, validaciones y pendientes. |
| `docs/specs/002-progressive-pricing/plan.md` | Creado | Componentes, responsabilidades, alternativas, pruebas, orden y riesgos. |
| `docs/specs/002-progressive-pricing/tasks.md` | Creado | Tareas pequeñas, verificables y trazables. |
| `ai-workspace/01-tasks/TASK024-progressive-pricing-preparation.md` | Creado | Este registro. |
| `ai-workspace/README.md` | Modificado | Índice de TASK023/TASK024, publicación del PR #3 y limitaciones actualizadas. |

No se modificaron archivos de código, dependencias, migraciones, modelos de clientes, routers ni bootstrap.

## 8. Validaciones ejecutadas

| Comprobación | Resultado real |
| --- | --- |
| `git diff --check` | **Sin errores.** |
| Verificación de enlaces relativos de la documentación nueva | **85 enlaces comprobados; 0 enlaces rotos.** |
| Coherencia de identificadores y ejemplos en los documentos nuevos | **53 marcadores comprobados; 0 ausentes.** |
| Confirmación de que solo cambian archivos Markdown | **Sí:** `ai-workspace/README.md` modificado y cuatro archivos `.md` nuevos. |
| Confirmación de que no cambian `backend/src`, `backend/pyproject.toml`, `backend/requirements.lock` ni migraciones | **Sin cambios:** `git diff --name-only` para esas rutas no devuelve entradas. |
| Pruebas funcionales | **No ejecutadas:** TASK024 no modifica código; las comprobaciones aplicables son documentales y de alcance. |

## 9. Recomendación para TASK025

No implementar el motor completo hasta que el propietario resuelva Q-02, PP-Q-01, Q-08 y Q-12, o autorice expresamente un alcance limitado a los enteros positivos aprobados.

Secuencia recomendada:

1. Cerrar las decisiones pendientes y registrarlas.
2. Crear el dominio `pricing` con los tramos aprobados.
3. Implementar `calculate_user_subtotal` para los seis ejemplos obligatorios.
4. Añadir pruebas de límites e invariantes.
5. Añadir los casos de 0, negativos, no enteros y máximo solo después de las decisiones.
6. Ejecutar Pytest, Ruff, mypy y la prueba de arquitectura.
7. Registrar TASK025 y actualizar la documentación.

TASK025 debe seguir siendo dominio puro: sin endpoint, sin persistencia, sin migración, sin dependencias nuevas y sin recibir el plan.

## 10. Riesgos y limitaciones

- Las decisiones Q-02, PP-Q-01, Q-08 y Q-12 siguen abiertas y bloquean la validación completa.
- La tabla de tramos puede ser sobreingeniería para tres tramos; se justifica por claridad de límites e invariantes.
- La precisión de `Decimal` con cantidades enormes no está decidida.
- Un redondeo prematuro podría contaminar el subtotal y futuros cálculos de impuestos o divisas.
- No hay endpoint ni persistencia, por lo que no habrá pruebas de integración en TASK025.
- No hay CI configurada; las comprobaciones dependen de ejecución local.
- Los hallazgos m-01 a m-04 de TASK021 siguen pendientes y son ajenos a esta tarea.

## 11. Referencias

- [Especificación 002](../../docs/specs/002-progressive-pricing/spec.md)
- [Plan 002](../../docs/specs/002-progressive-pricing/plan.md)
- [Tareas 002](../../docs/specs/002-progressive-pricing/tasks.md)
- [Requisitos funcionales](../../docs/requirements/functional-requirements.md)
- [ADR 0002](../../docs/adr/0002-architecture.md)
- [TASK023](TASK023-customer-publication.md)
- [ai-workspace/README.md](../README.md)
