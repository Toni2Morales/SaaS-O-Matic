# Plan técnico 002 - Precios progresivos por usuarios

> Vigente TASK036: Q-19 sustituye Q-02/PP-Q-01; cero admitido como 0.00.
> Véase [PLAN-004](../004-international-customers-and-simulations/plan.md).

| Campo | Valor |
| --- | --- |
| ID | PLAN-002 |
| Título | Plan técnico del motor de precios progresivos |
| Estado | **Implementado en TASK025, corregido en TASK027 y publicado en PR #4. Estado vigente verificado en TASK035** |
| Fecha | 2026-11-16 |
| Actualización | 2026-11-17 (TASK035) |
| Base arquitectónica | [ADR 0002](../../adr/0002-architecture.md) |
| Especificación | [spec.md](spec.md) |
| Tareas | [tasks.md](tasks.md) |

## 1. Principios

- Mantener el cálculo en `domain`, en Python puro, sin FastAPI, Pydantic, SQLAlchemy ni SQLite.
- No importar `infrastructure` ni `presentation` desde el dominio.
- No introducir un caso de uso, endpoint o persistencia mientras no exista un requisito aprobado.
- No recibir el plan como entrada ni consultar el catálogo de clientes.
- No usar `float`; usar `Decimal` construido desde cadenas o enteros exactos.
- Usar `Decimal` exacto, sin redondeos innecesarios; el formato de presentación y la serialización HTTP quedan fuera.
- No añadir dependencias nuevas.
- Mantener los tramos aprobados en una única fuente de verdad y cubrirlos con pruebas.

## 2. Estructura implementada

```text
backend/src/saas_o_matic/
└── domain/
    └── pricing/
        ├── __init__.py
        ├── errors.py
        ├── schedule.py
        ├── services.py
        └── value_objects.py

backend/tests/
└── test_pricing.py
```

No se crean paquetes de `application`, `infrastructure`, `presentation` ni cambios en `bootstrap/` para TASK025.

La estructura actual del backend agrupa por capa y después por funcionalidad. El módulo `pricing` sigue ese patrón. La frontera modular definitiva continúa pendiente (P-06 de ADR 0002), pero no impide mantener el cálculo aislado.

## 3. Componentes implementados

### 3.1 `PricingBand`

Objeto de valor inmutable con:

| Campo | Tipo | Invariante |
| --- | --- | --- |
| `lower_bound` | `int` | Mayor o igual que 1. |
| `upper_bound` | `int \| None` | Mayor o igual que `lower_bound`; `None` solo en el último tramo. |
| `price_per_user_eur` | `Decimal` | Mayor que cero y construido sin `float`. |

El objeto no conoce el catálogo de planes ni la divisa de presentación. `price_per_user_eur` documenta que el precio está expresado en EUR.

### 3.2 `PricingSchedule`

Objeto de valor inmutable que contiene una tupla ordenada de `PricingBand` y valida:

- Que no esté vacía.
- Que el primer tramo empiece en 1.
- Que los tramos sean contiguos, sin huecos ni solapamientos.
- Que exactamente el último tramo tenga `upper_bound = None`.
- Que todos los precios sean positivos.

La validación protege una invariante técnica del motor. No crea un catálogo configurable ni permite que un cliente HTTP cambie los precios.

### 3.3 Tabla de tramos aprobada

La constante de módulo `APPROVED_USER_PRICING_SCHEDULE` contiene:

```text
PricingBand(1, 10, Decimal("10.00"))
PricingBand(11, 50, Decimal("8.00"))
PricingBand(51, None, Decimal("5.00"))
```

Es una única fuente de verdad para el motor y las pruebas. Cualquier cambio de importes requiere una decisión del propietario y una actualización de requisitos, especificación y pruebas.

### 3.4 `calculate_user_subtotal`

Función pura:

```python
def calculate_user_subtotal(user_count: int) -> Decimal: ...
```

Responsabilidades:

1. Recibir únicamente el número de usuarios.
2. Recorrer los tramos aprobados.
3. Sumar `unidades_del_tramo × precio_por_usuario`.
4. Devolver el subtotal exacto en EUR.

No genera UUID, no persiste, no consulta base de datos, no conoce el plan y no formatea el resultado.

### 3.5 Errores de dominio

Implementados con las decisiones Q-02 y PP-Q-01:

| Error | Uso |
| --- | --- |
| `InvalidUserCount` | Cantidad distinta de un entero no negativo, incluidos negativos, no enteros y `bool`. |
| `InvalidPricingSchedule` | Invariante interna incumplida en la tabla de tramos. No se expone a HTTP. |

`InvalidUserCount` aplica mínimo 0 (Q-19 sustituye Q-02) y no impone máximo comercial. `InvalidPricingSchedule` sigue siendo defensa ante errores de programación.

## 4. Separación de responsabilidades

| Capa | TASK025 | Justificación |
| --- | --- | --- |
| `domain` | Implementa tramos, invariantes, cálculo y errores. | Es la regla de negocio pura. |
| `application` | Sin cambios. | No hay caso de uso ni endpoint aprobado. |
| `infrastructure` | Sin cambios. | No hay persistencia ni integración externa. |
| `presentation` | Sin cambios. | No se crean endpoints ni esquemas HTTP. |
| `bootstrap` | Sin cambios. | No hay nueva dependencia que inyectar. |

TASK025 es dominio puro: sin persistencia y sin endpoint. Cuando se apruebe una simulación, un caso de uso de `application` podrá invocar el motor y mapear sus errores. Ese caso de uso no debe reimplementar los tramos ni pasar el plan al cálculo.

## 5. Algoritmo y exactitud

### 5.1 Cálculo

Para cada tramo:

```text
si user_count < límite_inferior:
    terminar
límite_superior = límite_superior_del_tramo o user_count
unidades = min(user_count, límite_superior) - límite_inferior + 1
total += unidades × precio_por_usuario
```

Con los tramos aprobados, los seis ejemplos de la especificación producen exactamente los totales esperados.

### 5.2 Representación

- `Decimal("10.00")`, `Decimal("8.00")` y `Decimal("5.00")` se construyen desde cadenas; no desde literales `float`.
- `Decimal(unidades)` multiplicado por un precio decimal es exacto para los casos aprobados.
- No se llama a `quantize()` ni se aplica un modo de redondeo de negocio.
- Las pruebas comparan valores decimales (`== Decimal("108.00")`), no cadenas formateadas.
- Q-12 confirma que no hay máximo comercial. La implementación amplía la precisión del contexto de `Decimal` según una cota de dígitos calculada con `int.bit_length()`, sin convertir el entero a cadena, y prueba `10**30` y un valor de más de 4300 dígitos.
- TASK027 mantiene el uso de `localcontext()` y no reestructura el contexto decimal. La herencia de `Emax`, `Emin`, traps y modo de redondeo del llamador queda registrada como H-03, pendiente de una decisión futura si se exige aislamiento completo.

## 6. Alternativas consideradas

| Alternativa | Valoración | Motivo |
| --- | --- | --- |
| A. Tabla de tramos + iteración genérica | **Recomendada** | Los límites y precios quedan explícitos, se prueban como datos y se evita repetir números mágicos. |
| B. Fórmula directa con constantes | Sencilla | Menos código, pero mezcla límites y cálculo y dificulta verificar invariantes si cambian los tramos. |
| C. Caso de uso de aplicación ahora | No recomendada | No hay endpoint ni simulación aprobada; añadiría ceremonia sin uso real. |
| D. Persistencia o configuración de precios | No autorizada | No existe requisito y permitiría cambiar reglas comerciales sin decisión. |

La alternativa A es una decisión técnica, no una decisión de negocio. No autoriza a cambiar los importes ni los límites.

## 7. Estrategia de pruebas

| Nivel | Qué se prueba | Estado |
| --- | --- | --- |
| Dominio | 1, 10, 11, 50, 51 y 100 usuarios con los totales aprobados. | Implementado |
| Dominio | Que 10/11 y 50/51 no apliquen el precio del tramo superior a todos los usuarios. | Implementado |
| Dominio | Invariantes de `PricingBand` y `PricingSchedule`: inicio en 1, continuidad, sin solapamientos y último tramo abierto. | Implementado |
| Dominio | Resultado `Decimal` exacto, sin `float`. | Implementado |
| Dominio | 0 usuarios, negativos, no enteros y `bool`. | Implementado |
| Dominio | Sin máximo y cantidades muy grandes. | Implementado |
| Dominio | Cantidad de más de 4300 dígitos sin depender de `int → str`. | Implementado en TASK027 |
| Dominio | Aislamiento de la precisión decimal externa y restauración del contexto. | Implementado en TASK027 |
| Arquitectura | El dominio no importa frameworks ni capas exteriores. | `test_architecture.py` ejecutado |
| Aplicación/API/BD | No aplica: no hay caso de uso, endpoint ni persistencia. | No planificado |

Las pruebas de casos límite se implementaron con las decisiones aprobadas y no contienen expectativas inventadas.

## 8. Orden de implementación ejecutado

1. **Puerta de decisión:** Q-02, PP-Q-01, Q-08 y Q-12 se cerraron en TASK025.
2. Crear el paquete `domain/pricing/`.
3. Implementar `PricingBand` y `PricingSchedule` con sus invariantes.
4. Crear `APPROVED_USER_PRICING_SCHEDULE` con los tres tramos aprobados.
5. Implementar `calculate_user_subtotal` para los casos aprobados.
6. Añadir las pruebas de los seis ejemplos y de los límites 10/11 y 50/51.
7. Añadir las pruebas de invariantes de la tabla.
8. Añadir los casos de 0, negativos, no enteros, `bool` y cantidades grandes.
9. Ejecutar Pytest, Ruff, mypy y la prueba de arquitectura.
10. Registrar el resultado en TASK025 y actualizar la documentación.

TASK027 aplica después una corrección limitada:

1. Sustituir el dimensionado basado en `str(validated_count)` por una cota entera basada en `int.bit_length()`.
2. Añadir pruebas de más de 4300 dígitos y de aislamiento del contexto decimal.
3. Actualizar los requisitos generales para Q-02, Q-08, Q-12 y ASM-02.
4. Repetir Pytest, Ruff, mypy y `pip check`.

No quedaron casos funcionales pendientes dentro del alcance del dominio.

## 9. Archivos implementados

| Archivo | Acción | Contenido |
| --- | --- | --- |
| `backend/src/saas_o_matic/domain/pricing/__init__.py` | Crear | Exportaciones públicas del módulo. |
| `backend/src/saas_o_matic/domain/pricing/errors.py` | Crear | Errores de dominio. |
| `backend/src/saas_o_matic/domain/pricing/value_objects.py` | Crear | `PricingBand` y `PricingSchedule`. |
| `backend/src/saas_o_matic/domain/pricing/schedule.py` | Crear | Tabla de tramos aprobada. |
| `backend/src/saas_o_matic/domain/pricing/services.py` | Crear; modificar en TASK027 | `calculate_user_subtotal` y cota de precisión con `int.bit_length()`. |
| `backend/tests/test_pricing.py` | Crear; modificar en TASK027 | Pruebas de aceptación, límites, invariantes, >4300 dígitos y contexto decimal. |
| `docs/requirements/functional-requirements.md` | Modificar en TASK027 | Q-02, Q-08, Q-12 y ASM-02 alineados con SPEC-002. |
| `ai-workspace/01-tasks/TASK025-progressive-pricing-implementation.md` | Creado | Registro de implementación y evidencias. |
| `ai-workspace/01-tasks/TASK027-progressive-pricing-audit-fixes.md` | Creado en TASK027 | Registro de correcciones limitadas y validaciones. |

No se modificaron `backend/pyproject.toml`, `backend/requirements.lock`, migraciones, modelos de clientes, routers, esquemas Pydantic ni bootstrap.

## 10. Riesgos y decisiones

| Riesgo | Impacto | Mitigación |
| --- | --- | --- |
| Decisiones Q-02, PP-Q-01, Q-08 y Q-12 | Resueltas en TASK025. | Registradas en SPEC-002 y TASK025. |
| Sobreingeniería de la tabla para tres tramos | Más código del necesario. | Mantener la tabla inmutable y sin configuración externa; valorar la fórmula directa si el equipo prefiere menos abstracción. |
| Precisión de `Decimal` con cantidades enormes | Resultados inexactos si no se controla el contexto. | La implementación amplía la precisión con una cota entera, prueba `10**30` y más de 4300 dígitos; no se impone máximo comercial. |
| Contexto decimal externo (H-03) | `localcontext()` hereda `Emax`, `Emin`, traps y modo de redondeo del llamador. | Observación pendiente; no se reestructura el contexto sin una necesidad demostrada. |
| Redondeo futuro de impuestos o divisas | Un redondeo prematuro podría contaminar el subtotal. | No se redondea en el motor; el formato y las divisas futuras quedan fuera. |
| Acoplamiento accidental al plan | Rompería D-02. | No incluir `plan` en la firma ni en las pruebas del motor. |
| Falta de endpoint o persistencia | No hay prueba de integración. | Aceptado: el alcance es dominio puro. |
| Sin CI | Las comprobaciones dependen de ejecución local. | Ejecutadas en TASK025 y TASK027: Pytest, Ruff, mypy, `pip check` y `git diff --check`. |

## 11. Referencias

- [Especificación 002](spec.md)
- [Tareas 002](tasks.md)
- [Requisitos funcionales](../../requirements/functional-requirements.md)
- [ADR 0002 - Arquitectura](../../adr/0002-architecture.md)
- [Especificación 001 - Alta de clientes](../001-customer-registration/spec.md)
- [TASK024 - Preparación del motor de precios progresivos](../../../ai-workspace/01-tasks/TASK024-progressive-pricing-preparation.md)
- [TASK025 - Implementación del motor de precios progresivos](../../../ai-workspace/01-tasks/TASK025-progressive-pricing-implementation.md)
- [TASK027 - Correcciones limitadas del motor de precios progresivos](../../../ai-workspace/01-tasks/TASK027-progressive-pricing-audit-fixes.md)
