# Tareas 002 - Precios progresivos por usuarios

> TASK036 amplía mediante [TASKS-004](../004-international-customers-and-simulations/tasks.md).

| Campo | Valor |
| --- | --- |
| ID | TASKS-002 |
| Título | Desglose de implementación del motor de precios progresivos |
| Estado | **Implementado en TASK025, corregido en TASK027 y publicado en PR #4. Estado vigente verificado en TASK035** |
| Fecha | 2026-11-16 |
| Actualización | 2026-11-17 (TASK035) |
| Especificación | [spec.md](spec.md) |
| Plan | [plan.md](plan.md) |
| Implementación | [TASK025](../../../ai-workspace/01-tasks/TASK025-progressive-pricing-implementation.md); correcciones en [TASK027](../../../ai-workspace/01-tasks/TASK027-progressive-pricing-audit-fixes.md) |

## 1. Regla de alcance

TASK024 fue exclusivamente de análisis, documentación y planificación.

TASK025 implementa únicamente:

- El cálculo puro del subtotal de usuarios en EUR.
- Los tramos aprobados 1–10, 11–50 y 51 en adelante.
- Los seis ejemplos de aceptación obligatorios.
- La representación exacta con `Decimal`, sin `float`.

No se implementan impuestos, divisas, descuentos, periodicidades, precios de planes, persistencia, migraciones, endpoints ni frontend.

## 2. Decisiones aprobadas

- [x] Q-02 sustituida por Q-19: mínimo 0; subtotal exactamente 0.00.
- [x] PP-Q-01 actualizada: enteros no negativos; negativos, no enteros y `bool` rechazados.
- [x] Q-08: `Decimal` exacto en EUR, sin `float` ni redondeos innecesarios; formato y serialización HTTP quedan fuera.
- [x] Q-12: sin máximo comercial en el dominio; el límite de UI/API se decide por separado.
- [x] Registrar las decisiones en SPEC-002 y TASK025.

Las decisiones están cerradas. No quedan casos funcionales pendientes dentro del alcance del dominio.

## 3. Dominio

- [x] Crear `backend/src/saas_o_matic/domain/pricing/__init__.py`.
- [x] Crear `PricingBand` como objeto de valor inmutable con límite inferior, límite superior opcional y precio por usuario en EUR.
- [x] Validar que `lower_bound >= 1`, que `upper_bound` no sea menor que `lower_bound` y que el precio sea positivo y finito.
- [x] Crear `PricingSchedule` como tupla inmutable de tramos.
- [x] Validar que el primer tramo empiece en 1, que no haya huecos ni solapamientos y que exactamente el último tramo sea abierto.
- [x] Crear `APPROVED_USER_PRICING_SCHEDULE` con:
  - [x] 1–10 a `Decimal("10.00")`.
  - [x] 11–50 a `Decimal("8.00")`.
  - [x] 51 en adelante a `Decimal("5.00")`.
- [x] Implementar `calculate_user_subtotal(user_count: int) -> Decimal`.
- [x] Verificar que la función no recibe ni consulta el plan.
- [x] Verificar que la función no importa FastAPI, Pydantic, SQLAlchemy, SQLite ni capas exteriores.
- [x] No crear modelo SQLAlchemy, repositorio, migración ni router.

## 4. Errores y validación

- [x] Definir `InvalidUserCount` para cantidades distintas de un entero no negativo.
- [x] Definir `InvalidPricingSchedule` como error interno de invariante, sin exponerlo a HTTP.
- [x] Admitir 0 usuarios con subtotal 0.00 (TASK036 sustituye rechazo inicial).
- [x] Implementar el rechazo de negativos, no enteros y `bool`.
- [x] No imponer un máximo de usuarios en el dominio.
- [x] No truncar, redondear ni convertir silenciosamente entradas inválidas.
- [x] No aplicar `quantize()` ni un modo de redondeo de negocio.

## 5. Pruebas

- [x] `1` usuario devuelve `Decimal("10.00")`.
- [x] `10` usuarios devuelven `Decimal("100.00")`.
- [x] `11` usuarios devuelven `Decimal("108.00")`.
- [x] `50` usuarios devuelven `Decimal("420.00")`.
- [x] `51` usuarios devuelven `Decimal("425.00")`.
- [x] `100` usuarios devuelven `Decimal("670.00")`.
- [x] Probar los límites 9, 10, 11, 49, 50, 51, 52 y 101.
- [x] Probar las invariantes de `PricingBand` y `PricingSchedule`.
- [x] Probar que el resultado es `Decimal` y que no se usa `float`.
- [x] Añadir pruebas de 0, negativos, no enteros y `bool`.
- [x] Añadir pruebas de cantidades grandes y ausencia de máximo.
- [x] Ejecutar la prueba de arquitectura existente.
- [x] No crear pruebas de API, persistencia o migración porque no hay componentes de esas capas.

Las pruebas de pricing se ejecutaron con **65 casos** y la suite completa con **165 casos**. La ejecución conjunta de arquitectura y pricing terminó con **72 passed**.

## 6. Calidad y validación

- [x] `python -m pytest`: **165 passed**.
- [x] `python -m ruff check .`: **All checks passed**.
- [x] `python -m ruff format --check .`: **50 files already formatted**.
- [x] `python -m mypy .`: **Success: no issues found in 48 source files**.
- [x] `python -m pip check`: **No broken requirements found**.
- [x] Coherencia de `requirements.lock`: **35 entradas, 0 ausentes, 0 versiones distintas**.
- [x] `git diff --check`: **sin errores en archivos rastreados**.
- [x] Espacios o tabulaciones en archivos nuevos/modificados: **0 problemas**.
- [x] Enlaces relativos en documentación modificada: **6 archivos, 0 problemas**.
- [x] Confirmar que no se modifican `backend/pyproject.toml` ni `backend/requirements.lock`.
- [x] Confirmar que no se crean bases SQLite, migraciones ni archivos generados.
- [x] Confirmar que solo se modifican los archivos previstos en el plan y la documentación de trazabilidad.

## 7. Documentación y trazabilidad

- [x] Crear `ai-workspace/01-tasks/TASK025-progressive-pricing-implementation.md`.
- [x] Registrar las decisiones aprobadas.
- [x] Actualizar `spec.md`, `plan.md` y `tasks.md`.
- [x] Actualizar el índice de `ai-workspace/` para TASK025.
- [x] No reescribir los registros históricos de tareas anteriores.

## 8. Criterio de finalización

El motor se considera terminado cuando:

1. Los seis ejemplos obligatorios pasan con resultados exactos. **Cumplido.**
2. Cada tramo aplica su precio solo a sus unidades. **Cumplido.**
3. El resultado usa representación exacta, sin `float`. **Cumplido.**
4. El motor no recibe ni consulta el plan. **Cumplido.**
5. No se introducen impuestos, divisas, descuentos, periodicidades ni cargos adicionales. **Cumplido.**
6. No se crea persistencia ni endpoint. **Cumplido.**
7. El dominio no importa frameworks ni capas exteriores. **Cumplido.**
8. Las decisiones Q-02, PP-Q-01, Q-08 y Q-12 están resueltas. **Cumplido.**
9. Las pruebas y comprobaciones de calidad aplicables pasan con resultados reales. **Cumplido.**
10. La documentación y el registro TASK025 están actualizados. **Cumplido.**

## 9. Correcciones TASK027

- [x] H-01: sustituir el dimensionado basado en `str(validated_count)` por una cota entera basada en `int.bit_length()`.
- [x] H-01: probar una cantidad de más de 4300 dígitos, el tipo `Decimal` y la exactitud con `5 × user_count + 170`.
- [x] H-01: mantener los seis ejemplos y `10**30`.
- [x] H-02: actualizar Q-02, Q-08, Q-12 y ASM-02 en los requisitos, con referencias a SPEC-002 y TASK025.
- [x] H-04: probar un contexto decimal externo bajo y verificar su restauración.
- [x] H-03: mantener `localcontext()` sin reestructuración y registrar la observación pendiente.
- [x] Ejecutar Pytest, Ruff, mypy, `pip check` y `git diff --check`.
- [x] No añadir dependencias, migraciones, endpoints ni cambios de arquitectura.

TASK025 dejó 65 casos de pricing; TASK027 añade 2 casos y la suite de pricing queda en 67.

## 10. Fuera de alcance

- Cálculo de impuestos.
- Conversión de divisas.
- Persistencia de simulaciones.
- Endpoints y OpenAPI.
- Catálogo de planes y precios por plan.
- Descuentos, periodos de facturación y prorrateos.
- Formato de presentación y serialización HTTP.
- Frontend y control deslizante.
- Autenticación, facturación y aprovisionamiento.
