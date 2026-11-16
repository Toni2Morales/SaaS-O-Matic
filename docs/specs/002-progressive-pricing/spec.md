# Especificación 002 - Precios progresivos por usuarios

| Campo | Valor |
| --- | --- |
| ID | SPEC-002 |
| Título | Motor de cálculo de precios progresivos por número de usuarios |
| Estado | **Decisiones Q-02, PP-Q-01, Q-08 y Q-12 aprobadas; implementada en TASK025 y corregida en TASK027. Cambios locales no publicados.** |
| Fecha | 2026-11-16 |
| Rama | `feature/progressive-pricing` |
| Base | `origin/main` en `88816201a01677760a68ded5b8be21565bf737fc` (PR #3 fusionado) |
| Implementación | `backend/src/saas_o_matic/domain/pricing/` |
| Alcance | Cálculo puro del subtotal de usuarios en EUR; sin impuestos, divisas, persistencia, simulaciones ni endpoints |

## 1. Fuentes

- [Requisitos funcionales](../../requirements/functional-requirements.md), especialmente FR-05, sección 2, CON-03, ASM-02, ASM-03, Q-02, Q-08 y Q-12.
- [ADR 0001 - Stack tecnológico](../../adr/0001-technology-stack.md): Python 3.13, calidad del backend y divisa base EUR.
- [ADR 0002 - Arquitectura](../../adr/0002-architecture.md): monolito modular, dominio puro, módulo `pricing` y reglas de dependencia.
- [Especificación 001 - Alta de clientes](../001-customer-registration/spec.md): D-02 y separación entre catálogo de planes y precios.
- [Evaluación inicial del repositorio](../../assessment/001-repository-assessment.md): contexto de precisión decimal y redondeo.
- [Proceso de desarrollo asistido por IA](../../process/ai-assisted-development.md): flujo requisitos → especificación → plan → tareas → aprobación.
- [TASK024 - Preparación del motor de precios progresivos](../../../ai-workspace/01-tasks/TASK024-progressive-pricing-preparation.md): análisis previo y cierre del PR #3.
- [TASK025 - Implementación del motor de precios progresivos](../../../ai-workspace/01-tasks/TASK025-progressive-pricing-implementation.md): decisiones aprobadas, implementación y evidencias.
- [TASK027 - Correcciones limitadas del motor de precios progresivos](../../../ai-workspace/01-tasks/TASK027-progressive-pricing-audit-fixes.md): corrección de precisión y pruebas adicionales.

## 2. Objetivo y límites

Definir el comportamiento de un motor de cálculo que obtenga el subtotal de usuarios en EUR aplicando los tramos progresivos aprobados.

Quedan fuera de esta especificación:

- Impuestos, tasas y reglas fiscales (FR-06).
- Conversión de divisas y divisas distintas de EUR (FR-10, FR-11).
- Persistencia de simulaciones (FR-03, FR-11).
- Simulador, control deslizante y frontend (FR-09).
- Endpoints HTTP y contratos OpenAPI.
- Catálogo de planes, precios o prestaciones asociados a un plan.
- Descuentos, periodicidades, cargos de almacenamiento o de API.
- Autenticación, autorización, facturación y aprovisionamiento.

El motor calcula únicamente el subtotal de usuarios. No calcula el total de una simulación ni decide qué magnitud debe persistirse (Q-16). El motor es un cálculo puro: sin persistencia y sin endpoints.

## 3. Requisitos y decisiones confirmados

### 3.1 Regla progresiva aprobada

El coste se calcula por tramos progresivos acumulativos: cada usuario se cobra al precio del tramo en el que cae. No se aplica el precio del último tramo alcanzado a todos los usuarios.

| Tramo | Usuarios | Precio por usuario dentro del tramo |
| --- | --- | ---: |
| 1 | 1–10 | 10,00 EUR |
| 2 | 11–50 | 8,00 EUR |
| 3 | 51 en adelante | 5,00 EUR |

Fuente: FR-05 y sección 2 de los requisitos funcionales. La formulación «51 en adelante» equivale a «más de 50» en la tabla original.

### 3.2 Ejemplos de aceptación obligatorios

| Usuarios | Cálculo | Subtotal |
| ---: | --- | ---: |
| 1 | 1 × 10,00 | 10,00 EUR |
| 10 | 10 × 10,00 | 100,00 EUR |
| 11 | (10 × 10,00) + (1 × 8,00) | 108,00 EUR |
| 50 | (10 × 10,00) + (40 × 8,00) | 420,00 EUR |
| 51 | (10 × 10,00) + (40 × 8,00) + (1 × 5,00) | 425,00 EUR |
| 100 | (10 × 10,00) + (40 × 8,00) + (50 × 5,00) | 670,00 EUR |

Estos seis resultados son criterios de aceptación obligatorios. No son ejemplos orientativos ni pueden modificarse durante la implementación.

### 3.3 Independencia del catálogo de planes

D-02 y ASM-03 confirman que:

- El catálogo del MVP contiene únicamente el plan `standard`.
- El plan no modifica los tramos progresivos de precio por número de usuarios.
- No existen precios ni prestaciones adicionales asociados al plan.
- El motor de precios no recibe el plan como entrada ni consulta el catálogo de clientes.

La independencia es una decisión aprobada. Cualquier precio o prestación por plan requeriría una decisión posterior y quedaría fuera de esta especificación.

### 3.4 Moneda y representación

- La divisa base es EUR (CON-03 y ADR 0001).
- No se introducen divisas adicionales en este motor.
- La representación técnica aprobada es `Decimal`, nunca `float`, para evitar errores de coma flotante.
- No se aplica redondeo de negocio. Con los precios y cantidades aprobados, los subtotales son importes exactos y enteros de euro.
- El formato de presentación, la serialización HTTP y las futuras reglas de conversión de divisas quedan fuera del cálculo puro y no se han decidido en esta tarea.

## 4. Decisiones aprobadas en TASK025

| ID | Decisión aprobada |
| --- | --- |
| Q-02 | El mínimo es 1 usuario. Cero usuarios es inválido y no produce subtotal. |
| PP-Q-01 | Solo se aceptan enteros positivos. Se rechazan cero, negativos, valores no enteros y `bool`, sin truncar, redondear, convertir cadenas ni aplicar coerciones. El error de dominio es `InvalidUserCount`. |
| Q-08 | Se usa `Decimal` exacto y EUR. No se usa `float` ni se introducen redondeos innecesarios. El formato de presentación, la serialización HTTP y las futuras conversiones de divisas quedan pendientes. |
| Q-12 | No se establece un máximo comercial de usuarios en el dominio. El eventual máximo de la interfaz o de una futura API se decidirá por separado. No se introduce un límite arbitrario. |

Estas decisiones están aprobadas y sustituyen a las preguntas abiertas registradas en TASK024. Q-16 y el rango del control deslizante de FR-09 siguen fuera del alcance del cálculo puro. TASK027 corrige el dimensionado de la precisión para no depender de la conversión `int → str` y añade pruebas de cantidades superiores a 4300 dígitos y de aislamiento del contexto decimal, sin cambiar las reglas comerciales.

## 5. Trazabilidad de las decisiones

`PP-Q-01` es un identificador local de esta especificación y de TASK024/TASK025. No sustituye ni renumera las preguntas globales Q-01 a Q-17 de los requisitos funcionales; sirve para trazar la validación estricta del motor de precios.

Las decisiones Q-02, PP-Q-01, Q-08 y Q-12 se registran como aprobadas en TASK025. No se reinterpretan como preguntas abiertas.

## 6. Entradas y salidas

### 6.1 Entrada

```text
user_count: int
```

- Representa el número de usuarios activos.
- Debe ser un entero positivo mayor o igual que 1.
- Se rechazan cero, negativos, `float`, `Decimal`, cadenas, `None`, `bool` y otros tipos no enteros con `InvalidUserCount`.
- No se acepta `plan`, país, divisa, impuesto, periodicidad ni precios externos.
- No se trunca, redondea ni convierte silenciosamente ningún valor.
- No hay máximo comercial en el dominio (Q-12).

### 6.2 Salida

```text
subtotal_eur: Decimal
```

- Es el subtotal de usuarios en EUR.
- No incluye impuestos, conversión de divisas, descuentos ni cargos adicionales.
- No se aplica redondeo de negocio.
- El formato final (por ejemplo `670`, `670.00` o `"670.00"`) no forma parte del cálculo puro y queda pendiente para la presentación o serialización.
- Las pruebas comparan el valor decimal, no la representación textual.

### 6.3 Contrato implementado

La función de dominio implementada es:

```python
def calculate_user_subtotal(user_count: int) -> Decimal: ...
```

No se crea un DTO de aplicación, un esquema Pydantic ni un endpoint. El caso de uso de simulación, cuando se apruebe, podrá invocar esta función y decidir cómo presentar el resultado.

## 7. Algoritmo de referencia

La regla se implementa sobre una tupla inmutable de tramos:

```text
total = 0
para cada tramo en orden:
    si user_count < límite_inferior: terminar
    límite_superior = límite_superior_del_tramo o user_count
    unidades = min(user_count, límite_superior) - límite_inferior + 1
    total += unidades × precio_por_usuario
devolver total
```

Con los tramos aprobados:

| Tramo | Límite inferior | Límite superior | Precio |
| --- | ---: | ---: | ---: |
| 1 | 1 | 10 | `Decimal("10.00")` |
| 2 | 11 | 50 | `Decimal("8.00")` |
| 3 | 51 | sin límite | `Decimal("5.00")` |

El algoritmo se aplica únicamente a enteros positivos. Cero, negativos y valores no enteros se rechazan antes de calcular. La implementación amplía la precisión del contexto de `Decimal` según una cota superior de dígitos calculada con `int.bit_length()`, sin convertir el entero completo a cadena, para preservar la exactitud sin imponer un máximo comercial.

## 8. Validaciones y casos límite

| Caso | Estado | Tratamiento |
| --- | --- | --- |
| 1, 10, 11, 50, 51, 100 | Aprobado e implementado | Criterios de aceptación obligatorios de la sección 3.2. |
| Límites de tramo | Aprobado e implementado | Probar 10/11 y 50/51 para verificar que cada tramo solo cobra sus unidades. |
| 0 usuarios | Aprobado e implementado | Rechazar con `InvalidUserCount`; no devolver subtotal. |
| Negativos | Aprobado e implementado | Rechazar con `InvalidUserCount`. |
| No enteros | Aprobado e implementado | Rechazar con `InvalidUserCount`; no truncar ni convertir. |
| `bool` como entrada | Aprobado e implementado | Rechazar con `InvalidUserCount`, aunque `bool` sea subtipo de `int`. |
| Máximo de usuarios | Aprobado e implementado | Sin máximo en el dominio; el límite de UI/API se decide aparte. |
| Cantidades muy grandes | Aprobado e implementado | Sin máximo comercial; precisión ampliada con una cota entera y probada con `10**30` y más de 4300 dígitos. |
| Plan, país, divisa, impuestos | Fuera de alcance | No son entradas del motor. |
| Persistencia | Fuera de alcance | No se crea modelo, repositorio ni migración. |

## 9. Dependencias y restricciones

- ADR 0002: `domain` es Python puro y no importa FastAPI, Pydantic ni SQLAlchemy.
- ADR 0002: las dependencias apuntan hacia el dominio; este motor no importa capas exteriores.
- El módulo implementado es `pricing`, con tramos y cálculo exacto del subtotal. No aplica redondeo de negocio.
- Python 3.13, mypy estricto y Ruff según la configuración existente.
- Se permite la biblioteca estándar, en particular `decimal` y `dataclasses`; no se añaden dependencias.
- No se modifica el catálogo `standard` ni el modelo de clientes.
- No se crean endpoints, migraciones, modelos SQLAlchemy ni repositorios.
- No se implementan impuestos, divisas, descuentos, periodicidades ni prestaciones de planes.

## 10. Criterios de aceptación

1. `calculate_user_subtotal(1)` devuelve 10,00 EUR.
2. `calculate_user_subtotal(10)` devuelve 100,00 EUR.
3. `calculate_user_subtotal(11)` devuelve 108,00 EUR.
4. `calculate_user_subtotal(50)` devuelve 420,00 EUR.
5. `calculate_user_subtotal(51)` devuelve 425,00 EUR.
6. `calculate_user_subtotal(100)` devuelve 670,00 EUR.
7. Cada tramo cobra únicamente las unidades comprendidas en ese tramo.
8. El resultado se calcula con representación exacta, sin `float`.
9. El motor no recibe ni consulta el plan y no altera el catálogo `standard`.
10. El motor no aplica impuestos, divisas, descuentos, periodicidades ni cargos adicionales.
11. El dominio no importa FastAPI, Pydantic, SQLAlchemy, SQLite ni capas exteriores.
12. No se crea persistencia ni endpoint.
13. Cero, negativos, no enteros y `bool` se rechazan con `InvalidUserCount`.
14. No se impone un máximo comercial de usuarios en el dominio.
15. Las pruebas y comprobaciones de calidad aplicables pasan con resultados reales, incluidas las de más de 4300 dígitos y aislamiento del contexto decimal.

## 11. Fuera de alcance

- `POST` u otros endpoints de cálculo.
- Persistencia de simulaciones o de resultados.
- Impuestos por país.
- Conversión EUR/USD/GBP u otras divisas.
- Precios o prestaciones por plan.
- Descuentos, promociones, periodos de facturación o prorrateos.
- Cargos por almacenamiento o llamadas a la API.
- Formato de presentación o serialización HTTP del importe.
- Frontend, control deslizante, autenticación y facturación.

## 12. Referencias

- [Requisitos funcionales](../../requirements/functional-requirements.md)
- [ADR 0001 - Stack tecnológico](../../adr/0001-technology-stack.md)
- [ADR 0002 - Arquitectura](../../adr/0002-architecture.md)
- [Especificación 001 - Alta de clientes](../001-customer-registration/spec.md)
- [Plan técnico 002](plan.md)
- [Tareas 002](tasks.md)
- [TASK024 - Preparación del motor de precios progresivos](../../../ai-workspace/01-tasks/TASK024-progressive-pricing-preparation.md)
- [TASK025 - Implementación del motor de precios progresivos](../../../ai-workspace/01-tasks/TASK025-progressive-pricing-implementation.md)
- [TASK027 - Correcciones limitadas del motor de precios progresivos](../../../ai-workspace/01-tasks/TASK027-progressive-pricing-audit-fixes.md)
