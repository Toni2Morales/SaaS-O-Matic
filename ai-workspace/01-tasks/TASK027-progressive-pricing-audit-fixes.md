# TASK027 — Correcciones limitadas del motor de precios progresivos

| Campo | Valor |
| --- | --- |
| ID | TASK027 |
| Título | Correcciones limitadas del motor de precios progresivos |
| Estado | **Completada; correcciones locales; pendiente de publicación** |
| Fecha | 2026-11-16 |
| Participantes | Propietario (instrucción y decisiones) / OpenCode + DeepSeek (implementación, pruebas y documentación) |
| Autorización Git | **Ninguna publicación**: no `git add`, commit, push, PR ni merge. |

## 1. Objetivo y alcance

Resolver los hallazgos menores H-01 y H-02 de TASK026 y reforzar la cobertura del contexto decimal (H-04), sin alterar las reglas comerciales ni ampliar el alcance funcional del motor.

Se mantuvieron las decisiones vigentes:

- Q-02: mínimo 1 usuario; cero se rechaza.
- PP-Q-01: solo enteros positivos, sin coerciones.
- Q-08: cálculo exacto con `Decimal` en EUR; formato pendiente.
- Q-12: sin máximo comercial en el dominio; límite de UI/API pendiente.

No se introdujeron impuestos, descuentos, periodicidades, cargos adicionales, divisas nuevas ni precios dependientes del plan. No se crearon endpoints, casos de uso de aplicación, persistencia, migraciones ni cambios en clientes o bootstrap.

## 2. Estado Git

### 2.1. Estado inicial

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/progressive-pricing` |
| `HEAD` | `88816201a01677760a68ded5b8be21565bf737fc` |
| `origin/main` | `88816201a01677760a68ded5b8be21565bf737fc` |
| `main` local | `8371f9f608ce6e06984cc501d8240e1b7edf34d5` |
| Cambios staged | Ninguno |
| Cambios locales | `ai-workspace/README.md` modificado; TASK024, TASK025, el dominio `pricing`, `test_pricing.py` y `docs/specs/002-progressive-pricing/` sin rastrear |

El estado inicial coincidió con el esperado. No se descartó ni sobrescribió trabajo existente.

### 2.2. Estado final

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/progressive-pricing` |
| `HEAD` | `88816201a01677760a68ded5b8be21565bf737fc` |
| `origin/main` | `88816201a01677760a68ded5b8be21565bf737fc` |
| `main` local | `8371f9f608ce6e06984cc501d8240e1b7edf34d5` |
| `git add` / commit / push / PR / merge | No ejecutados |
| Cambios staged | Ninguno |

El estado final muestra `M` en `ai-workspace/README.md` y `docs/requirements/functional-requirements.md`; TASK024, TASK025, TASK027, el dominio `pricing`, `test_pricing.py` y `docs/specs/002-progressive-pricing/` permanecen sin rastrear. No hay cambios staged.

Los cambios de TASK027 permanecen locales. `HEAD` sigue coincidiendo con `origin/main`; no hay publicación.

## 3. Archivos creados y modificados

| Archivo | Acción | Contenido |
| --- | --- | --- |
| `backend/src/saas_o_matic/domain/pricing/services.py` | Modificado | Cota de dígitos con `int.bit_length()`; sin `str(validated_count)`. |
| `backend/tests/test_pricing.py` | Modificado | Pruebas de más de 4300 dígitos y de aislamiento del contexto decimal. |
| `docs/requirements/functional-requirements.md` | Modificado | Q-02, Q-08, Q-12, ASM-02 y referencias a SPEC-002/TASK025. |
| `docs/specs/002-progressive-pricing/spec.md` | Modificado | Estado, precisión y trazabilidad de TASK027. |
| `docs/specs/002-progressive-pricing/plan.md` | Modificado | Estrategia de precisión, pruebas, riesgos y archivos de TASK027. |
| `docs/specs/002-progressive-pricing/tasks.md` | Modificado | Estado y checklist de correcciones TASK027. |
| `ai-workspace/README.md` | Modificado | Índice y resumen de TASK027. |
| `ai-workspace/01-tasks/TASK027-progressive-pricing-audit-fixes.md` | Creado | Este registro. |

No se modificaron TASK024 ni TASK025. No se modificaron `backend/pyproject.toml`, `backend/requirements.lock`, migraciones, modelos de clientes, routers, esquemas Pydantic, `bootstrap/` ni el entorno virtual.

## 4. Corrección H-01

### 4.1. Cambio aplicado

Se sustituyó el dimensionado basado en la conversión del entero a cadena por una cota entera:

```python
def _decimal_digits_upper_bound(value: int) -> int:
    """Devuelve una cota superior segura de los dígitos decimales de un entero."""

    return (value.bit_length() // 9 + 1) * 3


validated_count = _validate_user_count(user_count)
price_digits = max(len(band.price_per_user_eur.as_tuple().digits) for band in schedule.bands)
digits_bound = _decimal_digits_upper_bound(validated_count)
precision = max(28, digits_bound + price_digits + 10)
```

No se usa `str(validated_count)`, `float`, `sys.set_int_max_str_digits(0)` ni un máximo comercial. `int.bit_length()` es una operación entera y no depende del límite de conversión `int → str`.

### 4.2. Justificación matemática

Para un entero positivo `N` con `b` bits, sea `b = 9q + r` con `0 <= r < 9`.

- `2^9 = 512 < 10^3 = 1000`.
- `2^r <= 2^8 = 256 < 10^3`.
- Por tanto, `N < 2^b = 2^(9q) × 2^r < 10^(3q) × 10^3 = 10^(3q + 3)`.
- En consecuencia, `N` tiene como máximo `3q + 3 = (b // 9 + 1) × 3` dígitos decimales.

La cota puede sobreestimar ligeramente, pero nunca infravalora el número de dígitos.

Para los precios aprobados, `price_digits = 4`. Si la cantidad tiene como máximo `D` dígitos:

- Cada producto `unidades × precio` tiene como máximo `D + 4` dígitos significativos.
- La suma de tres productos tiene como máximo `D + 5` dígitos.
- La precisión usada es `D + 4 + 10 = D + 14`, con mínimo 28, suficiente para multiplicaciones y sumas exactas.

Ejemplos:

| Cantidad | Bits | Cota de dígitos | Precisión | Resultado |
| ---: | ---: | ---: | ---: | --- |
| `10**30` | 100 | 36 | 50 | Exacto |
| `10**4300` | 14285 | 4764 | 4778 | Exacto |

## 5. Resultado de la prueba con más de 4300 dígitos

Se añadió `test_calculate_user_subtotal_supports_counts_beyond_int_str_limit` con `user_count = 10**4300`, que tiene 4.301 dígitos decimales.

La prueba comprueba:

- Que no se produce el `ValueError` de conversión `int → str`.
- Que el resultado es `Decimal`.
- Que el resultado coincide con la referencia independiente `Decimal(5 × user_count + 170)`.
- Que los seis ejemplos aprobados y `10**30` siguen cubiertos por la suite existente.

Resultado real: **pasó**. No se modificaron los límites globales de conversión de enteros de Python. La biblioteca `Decimal` no presentó una limitación independiente para esta cantidad; el resultado fue exacto.

## 6. Cambios documentales H-02

Se actualizaron exclusivamente los apartados afectados de `docs/requirements/functional-requirements.md`:

- Versión 0.8 y estado con Q-02, Q-08, Q-12 y PP-Q-01 registradas.
- Q-02: mínimo 1 usuario; cero se rechaza.
- Q-08: `Decimal` exacto en EUR, sin `float` ni redondeo de negocio; formato y serialización pendientes.
- Q-12: sin máximo comercial de usuarios en el dominio; límite de UI/API y rangos de almacenamiento/llamadas pendientes.
- ASM-02: entrada válida de al menos 1 usuario.
- Casos límite de 0 usuarios e importes actualizados.
- Referencias a [SPEC-002](../../docs/specs/002-progressive-pricing/spec.md) y [TASK025](TASK025-progressive-pricing-implementation.md).

No se cerraron otras preguntas. No se reescribió TASK024.

## 7. Resultado de la prueba de aislamiento Decimal

Se añadió `test_calculate_user_subtotal_isolates_decimal_context`:

```python
with localcontext() as context:
    context.prec = 2

    result = calculate_user_subtotal(100)

    assert result == Decimal("670.00")
    assert context.prec == 2
```

La prueba configura una precisión externa baja, ejecuta el cálculo, comprueba que el resultado es exacto y verifica que el contexto externo conserva su precisión. El uso de `localcontext()` en la propia prueba garantiza la restauración automática incluso si se produce un error.

Resultado real: **pasó**.

## 8. Estado de H-03

H-03 sigue siendo una observación pendiente: `localcontext()` aísla `prec`, pero hereda `Emax`, `Emin`, traps y modo de redondeo del contexto del llamador. TASK027 no reestructura el manejo de contextos decimales ni introduce un contexto nuevo.

La corrección H-01 no empeora este comportamiento: el cálculo sigue usando `localcontext()` y no modifica el contexto global. No se ha demostrado un defecto de exactitud bajo un contexto externo razonable.

## 9. Validaciones ejecutadas

Todas las órdenes se ejecutaron desde `backend/` con `backend/.venv/Scripts/python.exe`, que resolvió a:

```text
C:\Users\Toni\Desktop\Proyectos\Sass-O-Matic\backend\.venv\Scripts\python.exe
```

| Comando | Resultado real |
| --- | --- |
| `python -m pytest` | **167 passed in 2.65s** |
| `python -m pytest tests/test_pricing.py -q` | **67 passed in 0.16s** |
| `python -m pytest tests/test_architecture.py tests/test_pricing.py -q` | **74 passed in 0.16s** |
| `python -m ruff check .` | **All checks passed!** |
| `python -m ruff format --check .` | **50 files already formatted** |
| `python -m mypy .` | **Success: no issues found in 48 source files** |
| `python -m pip check` | **No broken requirements found.** |
| `git diff --check` | **Sin errores en archivos rastreados** |

La suite de pricing pasó de 65 a 67 casos: se añadieron las pruebas de más de 4300 dígitos y de aislamiento del contexto decimal. Los seis ejemplos comerciales y `10**30` siguen pasando.

Se comprobó también que los archivos nuevos y no rastreados no contienen espacios ni tabulaciones finales: **0 problemas**. La coherencia documental de Q-02, PP-Q-01, Q-08 y Q-12 se revisó en requisitos, SPEC-002 y este registro.

## 10. Dependencias, migraciones y endpoints

- No se añadieron dependencias.
- No se modificaron `backend/pyproject.toml` ni `backend/requirements.lock`.
- No se crearon migraciones ni bases de datos.
- No se crearon endpoints, casos de uso de aplicación, repositorios ni esquemas Pydantic.
- No se modificaron clientes, bootstrap ni capas de infraestructura o presentación.
- No se modificó `backend/.venv`.
- El dominio sigue usando únicamente biblioteca estándar y módulos propios de `domain/pricing`.

## 11. Riesgos pendientes

- **H-03:** `localcontext()` hereda `Emax`, `Emin`, traps y redondeo del llamador. Es una observación, no un defecto demostrado en el alcance aprobado.
- **Sin CI:** no hay `.github/` ni comprobaciones automáticas; la validación es local.
- **Q-12 parcial:** el dominio no impone máximo comercial, pero el límite de UI/API y los rangos de almacenamiento/llamadas siguen pendientes.
- **Cantidades extremas:** aunque se eliminó el límite de `int → str`, el cálculo sigue sujeto a los recursos disponibles y a las propiedades del contexto decimal. No se introduce un máximo comercial.

No quedan bloqueantes conocidos para el alcance de TASK027.

## 12. Recomendación para TASK028

Procede preparar **TASK028 de publicación controlada del PR #4**, con autorización explícita del propietario.

TASK028 debería:

1. Revisar el diff completo y confirmar que solo incluye TASK024, TASK025, TASK027 y los cambios autorizados.
2. Incluir en la descripción del PR las decisiones Q-02, PP-Q-01, Q-08 y Q-12, las correcciones H-01/H-02/H-04 y la observación H-03.
3. Mantener el merge como competencia exclusiva del propietario.

No se ha preparado el PR #4 ni se ha ejecutado ninguna operación Git de publicación en TASK027.
