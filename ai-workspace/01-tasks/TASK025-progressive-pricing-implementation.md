# TASK025 — Implementación del motor de precios progresivos

| Campo | Valor |
| --- | --- |
| ID | TASK025 |
| Título | Implementación y pruebas del motor de precios progresivos por usuarios |
| Estado | **Completada; implementación local; pendiente de publicación** |
| Fecha | 2026-11-16 |
| Participantes | Propietario (decisiones) / OpenCode + DeepSeek (implementación, pruebas y documentación) |
| Autorización Git | **Ninguna publicación**: no `git add`, commit, push, PR ni merge. |

## 1. Objetivo y alcance

Implementar y probar el cálculo puro del subtotal de usuarios en EUR con los tramos progresivos aprobados.

Se implementó únicamente:

- El dominio `backend/src/saas_o_matic/domain/pricing/`.
- Los tramos 1–10, 11–50 y 51 en adelante.
- La validación estricta de cantidades.
- La representación exacta con `Decimal`.
- Las pruebas automatizadas y la documentación de trazabilidad.

No se crearon endpoints, casos de uso de aplicación, persistencia, migraciones, integración con clientes, frontend ni cambios en el catálogo de planes.

## 2. Decisiones aprobadas

| ID | Decisión registrada |
| --- | --- |
| Q-02 | Mínimo 1 usuario. Cero es inválido y no produce subtotal. |
| PP-Q-01 | Solo enteros positivos. Se rechazan cero, negativos, no enteros y `bool`, sin truncar, redondear, convertir cadenas ni aplicar coerciones. El error es `InvalidUserCount`. |
| Q-08 | `Decimal` exacto en EUR, sin `float` ni redondeos innecesarios. Formato de presentación, serialización HTTP y futuras conversiones de divisas quedan pendientes. |
| Q-12 | Sin máximo comercial de usuarios en el dominio. El eventual máximo de UI/API se decidirá por separado. |

## 3. Estado Git

### 3.1 Estado inicial

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/progressive-pricing` |
| `HEAD` | `88816201a01677760a68ded5b8be21565bf737fc` |
| `origin/main` | `88816201a01677760a68ded5b8be21565bf737fc` |
| Cambios locales | Solo los documentos esperados de TASK024: `ai-workspace/README.md` modificado y cuatro archivos `.md` nuevos. |
| Cambios staged | Ninguno |

### 3.2 Estado final

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/progressive-pricing` |
| `HEAD` | `88816201a01677760a68ded5b8be21565bf737fc` |
| `origin/main` | `88816201a01677760a68ded5b8be21565bf737fc` |
| `main` local | No tocada; `8371f9f608ce6e06984cc501d8240e1b7edf34d5` |
| `git add` / commit / push / PR / merge | No ejecutados |
| Cambios staged | Ninguno |

El detalle final de archivos se registra en las secciones 3.2 y 4.

## 4. Archivos creados o modificados

| Archivo | Acción | Contenido |
| --- | --- | --- |
| `backend/src/saas_o_matic/domain/pricing/__init__.py` | Creado | Exportaciones públicas del dominio. |
| `backend/src/saas_o_matic/domain/pricing/errors.py` | Creado | `PricingDomainError`, `InvalidUserCount` e `InvalidPricingSchedule`. |
| `backend/src/saas_o_matic/domain/pricing/value_objects.py` | Creado | `PricingBand` y `PricingSchedule`. |
| `backend/src/saas_o_matic/domain/pricing/schedule.py` | Creado | `APPROVED_USER_PRICING_SCHEDULE`. |
| `backend/src/saas_o_matic/domain/pricing/services.py` | Creado | `calculate_user_subtotal`. |
| `backend/tests/test_pricing.py` | Creado | 65 pruebas de aceptación, límites, entradas inválidas, invariantes e inmutabilidad. |
| `docs/specs/002-progressive-pricing/spec.md` | Modificado | Decisiones aprobadas, comportamiento implementado y criterios de aceptación. |
| `docs/specs/002-progressive-pricing/plan.md` | Modificado | Estado implementado, componentes, pruebas y riesgos actualizados. |
| `docs/specs/002-progressive-pricing/tasks.md` | Modificado | Tareas completadas y resultados reales. |
| `ai-workspace/01-tasks/TASK025-progressive-pricing-implementation.md` | Creado | Este registro. |
| `ai-workspace/README.md` | Modificado | Índice de TASK025 y estado del motor de precios. |

No se modificaron `backend/pyproject.toml`, `backend/requirements.lock`, migraciones, modelos de clientes, routers, esquemas Pydantic, `bootstrap/` ni el entorno virtual.

## 5. Diseño implementado

### 5.1 `PricingBand`

Objeto de valor inmutable (`frozen=True`, `slots=True`) con:

- `lower_bound: int`
- `upper_bound: int | None`
- `price_per_user_eur: Decimal`

Valida:

- Límite inferior entero, no `bool`, mayor o igual que 1.
- Límite superior entero, no `bool`, o `None`, y no menor que el inferior.
- Precio de tipo `Decimal`, finito y positivo.
- Rechazo de `float`, `int`, cadenas, `NaN` e `Infinity` como precio.

### 5.2 `PricingSchedule`

Objeto de valor inmutable con una tupla de tramos. Valida:

- Tupla no vacía y compuesta por `PricingBand`.
- Inicio en 1.
- Continuidad sin huecos ni solapamientos.
- Solo el último tramo puede estar abierto.
- Existencia de un último tramo abierto.

### 5.3 Tabla aprobada

`APPROVED_USER_PRICING_SCHEDULE` contiene:

```text
PricingBand(1, 10, Decimal("10.00"))
PricingBand(11, 50, Decimal("8.00"))
PricingBand(51, None, Decimal("5.00"))
```

### 5.4 `calculate_user_subtotal`

```python
def calculate_user_subtotal(user_count: int) -> Decimal: ...
```

La función:

1. Valida que `user_count` sea un entero positivo y no `bool`.
2. Rechaza cualquier otro valor con `InvalidUserCount`.
3. Recorre la tabla aprobada.
4. Calcula las unidades de cada tramo.
5. Multiplica por el precio `Decimal` correspondiente.
6. Devuelve el subtotal exacto en EUR.

La precisión del contexto de `Decimal` se amplía dinámicamente según la cantidad para preservar la exactitud sin imponer un máximo. La función no conoce el plan, no persiste, no accede a base de datos ni formatea el resultado.

## 6. Resultados de los ejemplos obligatorios

| Usuarios | Resultado obtenido | Esperado | Estado |
| ---: | ---: | ---: | --- |
| 1 | 10,00 EUR | 10,00 EUR | Pasa |
| 10 | 100,00 EUR | 100,00 EUR | Pasa |
| 11 | 108,00 EUR | 108,00 EUR | Pasa |
| 50 | 420,00 EUR | 420,00 EUR | Pasa |
| 51 | 425,00 EUR | 425,00 EUR | Pasa |
| 100 | 670,00 EUR | 670,00 EUR | Pasa |

También se probaron los límites 9, 10, 11, 49, 50, 51, 52 y 101, los incrementos 10→11 y 50→51, la monotonicidad y una cantidad de `10**30` sin máximo.

## 7. Pruebas de entradas inválidas

Se rechazaron con `InvalidUserCount`:

- `0`, `-1`, `-100`.
- `1.0`, `1.5`, `float("inf")`, `float("nan")`.
- `Decimal("1")`, `Decimal("1.0")`.
- `"1"`, `""`.
- `None`.
- `True`, `False`.
- `object()`.
- `[1]`, `(1,)`.

No se truncó, redondeó ni convirtió ningún valor. La prueba comprueba además que el error conserva el valor original.

## 8. Pruebas de invariantes

Se probaron:

- Tabla válida con último tramo abierto.
- Tabla vacía.
- Primer tramo distinto de 1.
- Hueco entre tramos.
- Solapamiento.
- Tramo abierto intermedio.
- Falta de tramo final abierto.
- Límite inferior inválido, incluido `bool`, `float` y `Decimal`.
- Límite superior inválido, incluido `bool` y `float`.
- Precio cero, negativo, `NaN`, `Infinity`, `float`, `int` y cadena.
- Inmutabilidad de `PricingBand`, `PricingSchedule` y de la tupla de tramos.

## 9. Validaciones ejecutadas

Todas las herramientas Python se ejecutaron desde `backend/` con `backend/.venv`.

| Comprobación | Resultado real |
| --- | --- |
| `python -m pytest tests/test_pricing.py -q` | **65 passed** |
| `python -m pytest` | **165 passed** |
| `python -m pytest tests/test_architecture.py tests/test_pricing.py -q` | **72 passed** |
| `tests/test_architecture.py` | **7 passed**, incluida en la suite completa |
| `python -m ruff check .` | **All checks passed** |
| `python -m ruff format --check .` | **50 files already formatted** |
| `python -m mypy .` | **Success: no issues found in 48 source files** |
| `python -m pip check` | **No broken requirements found** |
| Coherencia de `requirements.lock` con el entorno | **35 entradas, 0 ausentes, 0 versiones distintas** |
| `git diff --check` | **Sin errores en archivos rastreados** |
| Espacios o tabulaciones en archivos nuevos/modificados | **0 problemas** |
| Enlaces relativos en documentación modificada | **6 archivos comprobados, 0 problemas** |
| Cambios en dependencias o migraciones | **Ninguno** |
| Cambios staged | **Ninguno** |

No se ejecutaron pruebas de API, persistencia o migración nuevas porque TASK025 no crea esos componentes. Las pruebas existentes de esas capas se ejecutaron dentro de la suite completa y siguen pasando.

## 10. Restricciones respetadas

- Sin endpoints ni routers nuevos.
- Sin casos de uso de aplicación.
- Sin persistencia, modelos SQLAlchemy, repositorios ni migraciones.
- Sin cambios en el catálogo de planes ni en clientes.
- Sin dependencias nuevas.
- Sin `float` para precios o subtotales.
- Sin impuestos, divisas, descuentos, periodicidades ni cargos adicionales.
- Sin `git add`, commit, push, PR, merge, rebase ni operaciones destructivas.
- Sin modificar `main`.

## 11. Cuestiones aplazadas

- Formato de presentación y serialización HTTP del importe.
- Reglas de redondeo para futuros impuestos o conversiones de divisas.
- Persistencia de simulaciones y decisión Q-16 sobre la magnitud económica persistida.
- Endpoint de simulación y contrato OpenAPI.
- Rango y paso del control deslizante de FR-09.
- Límite de usuarios de una futura UI o API.
- Integración con clientes y catálogo de planes.
- Cualquier precio o prestación específica por plan.

## 12. Riesgos y limitaciones

- El motor no tiene contrato HTTP ni prueba de integración porque no hay endpoint aprobado.
- La representación exacta se apoya en `Decimal`; futuras operaciones con impuestos o divisas necesitarán una decisión de redondeo.
- La ampliación dinámica de precisión cubre cantidades grandes, pero no sustituye una política monetaria para operaciones futuras.
- No hay CI configurada; las comprobaciones se ejecutaron localmente.
- No consta revisión independiente humana de TASK025.
- No se abordan hallazgos ajenos de tareas anteriores.

## 13. Recomendación para TASK026

Revisar y aprobar TASK025 antes de abrir una nueva funcionalidad.

No hay una TASK026 definida en esta instrucción. Si el propietario decide continuar con simulaciones, la siguiente unidad coherente sería el caso de uso de simulación y su persistencia, pero requiere decisiones previas sobre Q-16, el contrato de API, el formato monetario, el rango de usuarios y el modelo de datos. No debe implementarse por inferencia.

Alternativamente, TASK026 podría limitarse a consolidar la validación local o preparar la publicación de TASK024/TASK025, pero esa decisión corresponde al propietario.

## 14. Referencias

- [Especificación 002](../../docs/specs/002-progressive-pricing/spec.md)
- [Plan 002](../../docs/specs/002-progressive-pricing/plan.md)
- [Tareas 002](../../docs/specs/002-progressive-pricing/tasks.md)
- [Requisitos funcionales](../../docs/requirements/functional-requirements.md)
- [ADR 0002](../../docs/adr/0002-architecture.md)
- [TASK024](TASK024-progressive-pricing-preparation.md)
- [ai-workspace/README.md](../README.md)
