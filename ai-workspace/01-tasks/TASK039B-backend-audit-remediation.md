# TASK039B — Remediación autorizada de la auditoría TASK039

| Campo | Valor |
| --- | --- |
| Tarea | TASK039B |
| Fecha | 2026-11-18 |
| Rama | `feature/mvp-backend` |
| HEAD | `b3c5ca81d23d279b478ed466757bada031aa1e1e` |
| Estado | Implementada y validada localmente; sin publicación |
| Auditoría fuente | [`TASK039-backend-independent-audit.md`](TASK039-backend-independent-audit.md) |
| Alcance autorizado | A39-01, A39-02, A39-03, A39-04 y A39-06; A39-05 solo documentación y pruebas |
| Alcance revisado sin corregir | A39-07 a A39-11 |
| Alcance diferido o aceptado | A39-12 a A39-15 |

## 1. Resumen ejecutivo

TASK039 auditó el backend acumulado con dictamen **APTA CON OBSERVACIONES** y sin
hallazgos bloqueantes. TASK039B aplica únicamente las correcciones autorizadas:

- A39-01: matriz de trazabilidad coherente con el backend real.
- A39-02: README del backend con migraciones 0001–0004, contrato vigente y
  limitaciones reales.
- A39-03: `.env.example` alineado con la única configuración consumida.
- A39-04: runtime y Alembic comparten la resolución de `DATABASE_URL`/SQLite.
- A39-06: límites técnicos de plausibilidad para tasas FX externas, rechazo antes
  de la caché y `503` controlado.

A39-05 se documenta y se protege con pruebas de regresión sin ocultar, reparar ni
omitir filas. A39-07 a A39-11 se revisan individualmente y no se corrigen por falta
de autorización específica. A39-12 a A39-15 se aceptan o difieren como
limitaciones del MVP.

La suite pasa de **538 pruebas** en el baseline a **579 pruebas**; las 41 nuevas
cubren configuración SQLite, tasas FX, caché, API, ausencia de filas parciales y
corrupción controlada del historial. No se añadieron dependencias, endpoints,
migraciones, Angular, autenticación, CORS, límites globales ni servicios externos.

## 2. Autorización y límites respetados

Se aplicaron solo los cambios autorizados. No se modificaron:

- `ai-workspace/01-tasks/TASK039-backend-independent-audit.md`;
- las migraciones `0001`–`0004`;
- `LICENSE`;
- los registros TASK001–TASK039;
- los manifiestos de TASK037/TASK038;
- el documento original `Prueba Devs con IA.docx`.

No se ejecutaron `git add`, commit, push, PR, merge, rebase, stash, reset, clean ni
force-push. La rama sigue siendo `feature/mvp-backend` y el índice está vacío.

## 3. Estado inicial

- Rama: `feature/mvp-backend`.
- HEAD: `b3c5ca81d23d279b478ed466757bada031aa1e1e`.
- `origin/main` en el mismo commit; `main` local en
  `8371f9f608ce6e06984cc501d8240e1b7edf34d5`.
- 56 ficheros modificados, 38 sin seguimiento, 0 eliminados y 0 staged.
- 93 candidatos iniciales con huella SHA-256, excluyendo el `.docx`.
- Baseline: **538 pruebas superadas en 52,13 s**, Ruff, formato, mypy y
  `pip check` correctos; 35 pines instalados.

## 4. Plan correctivo

1. Unificar la resolución SQLite en infraestructura y reutilizarla desde el
   runtime y Alembic (A39-04).
2. Añadir validación defensiva de tasas externas en el dominio, antes de la caché
   y del cálculo (A39-06).
3. Documentar el comportamiento controlado ante snapshots corruptos y fijarlo con
   pruebas (A39-05).
4. Corregir trazabilidad, README y plantilla de configuración (A39-01/02/03).
5. Revisar A39-07 a A39-11 sin cambiar código no autorizado.
6. Ejecutar validación completa y comparar huellas iniciales/finales.

## 5. Hallazgos y tratamiento

| ID | Severidad TASK039 | Tratamiento TASK039B | Clasificación |
| --- | --- | --- | --- |
| A39-01 | BAJA | Matriz, requisitos, roadmap e índice actualizados | **RESUELTO** |
| A39-02 | BAJA | README backend corregido | **RESUELTO** |
| A39-03 | BAJA | `.env.example` corregido | **RESUELTO** |
| A39-04 | BAJA | Resolución SQLite compartida y probada | **RESUELTO** |
| A39-05 | BAJA | Comportamiento controlado documentado y probado; sin ocultación | **RIESGO ACEPTADO** |
| A39-06 | OBSERVACIÓN | Límites FX y `503` antes de caché | **RESUELTO** |
| A39-07 | OBSERVACIÓN | Revisado; logging no autorizado | **PENDIENTE DE AUTORIZACIÓN** |
| A39-08 | OBSERVACIÓN | Revisado; puerto estrecho no autorizado | **PENDIENTE DE AUTORIZACIÓN** |
| A39-09 | OBSERVACIÓN | Asimetría Q-26 documentada | **RIESGO ACEPTADO** |
| A39-10 | OBSERVACIÓN | Limitación estática documentada | **RIESGO ACEPTADO** |
| A39-11 | OBSERVACIÓN | Escaneo lineal aceptado para el MVP; optimización futura | **DIFERIDO** |
| A39-12 | OBSERVACIÓN | Sin auth/CORS/límites; no exponer con datos reales | **DIFERIDO** |
| A39-13 | OBSERVACIÓN | DDL SQLite no transaccional; copia y prueba previas | **RIESGO ACEPTADO** |
| A39-14 | OBSERVACIÓN | Lock global durante FX; aceptado en MVP | **RIESGO ACEPTADO** |
| A39-15 | OBSERVACIÓN | Caché por proceso; aceptada en MVP | **RIESGO ACEPTADO** |

### A39-01 — Trazabilidad desactualizada

Se actualizaron `docs/requirements/requirements-traceability.md`,
`docs/requirements/functional-requirements.md`, `docs/planning/mvp-roadmap.md` y
`ai-workspace/README.md`. La matriz distingue backend local de E2E/UI, refleja
FR-01 a FR-12, incorpora TASK039/TASK039B, elimina la cifra obsoleta de 340
pruebas y deja de afirmar que faltan impuestos, divisas, búsqueda, historial o
preview en backend. La versión vigente es 1.2 de trazabilidad y 1.3 de requisitos.

### A39-02 — README del backend obsoleto

`backend/README.md` incluye ahora:

- migraciones `0001`–`0004`, incluida `0004_add_simulation_taxes_and_fx`;
- contrato actual con impuestos, total EUR, conversión y snapshot FX;
- resolución compartida de SQLite y semántica de `DATABASE_URL`;
- límites FX, comportamiento `503` y política A39-05;
- estructura de módulos, alcance, limitaciones y evidencia de 579 pruebas.

### A39-03 — `.env.example` no operativo

La plantilla contiene solo `DATABASE_URL`, la ruta predeterminada real y las
reglas de resolución. Declara expresamente que el backend no carga `.env`
automáticamente, que las rutas relativas se resuelven desde `backend/`, que solo
se admite SQLite de fichero y que no debe contener secretos. Se eliminaron
`APP_*`, `CORS_ORIGINS`, `EXCHANGE_RATE_API_*` y `TAX_RULES_SOURCE` porque no
tenían código que las consumiera.

### A39-04 — Runtime y Alembic con bases distintas

Se añadió en `backend/src/saas_o_matic/infrastructure/database.py`:

- `BACKEND_ROOT`, `DEFAULT_DATABASE_PATH` y `DEFAULT_DATABASE_URL`;
- `resolve_database_url`, `database_path_from_url` y `resolve_database_path`;
- normalización a ruta absoluta y formato único.

Prioridad: `DATABASE_URL` del proceso, URL configurada por Alembic y ruta
predeterminada `backend/var/saas_o_matic.sqlite3`. Las rutas relativas se
resuelven desde `backend/`, no desde el directorio de trabajo. Se rechazan otros
motores, `:memory:`, URLs vacías y parámetros de consulta con `ValueError`. No se
lee `.env` ni se abre una conexión al importar.

`bootstrap/main.py` y `migrations/env.py` usan la misma resolución. El motor del
runtime sigue siendo perezoso. La prueba `backend/tests/test_database_config.py`
contiene 12 casos: prioridad de entorno, URL configurada, ruta relativa,
configuración inválida, rechazo en runtime, base alternativa migrada y usada para
crear/leer un cliente, base no configurada sin crear y base predeterminada sin
cambios.

### A39-05 — Fila corrupta en el historial

No se cambió la política de error. Se documenta y se fija con pruebas que una fila
con `calculation_snapshot` inválido o `user_subtotal_eur` no decimal produce un
`500 application/problem+json` controlado, sin detalles internos, sin ocultar
filas, sin inventar importes, sin reparar datos y sin modificar otras filas. La
corrupción no es alcanzable a través de la API porque los snapshots los escribe la
aplicación.

La prueba `test_corrupt_history_row_is_a_controlled_500_without_changes` cubre las
dos variantes y compara todas las filas antes y después de la petición.

### A39-06 — Tasas FX extremas y overflow

Se añadieron en `domain/simulations/calculation.py`:

- `MIN_EXCHANGE_RATE = 0.000001`;
- `MAX_EXCHANGE_RATE = 1000000`;
- `MAX_EXCHANGE_RATE_DIGITS = 32`;
- `validate_exchange_rate`, invocado por `ExchangeQuote`.

Los límites son técnicos de plausibilidad, no comerciales. EUR/USD y EUR/GBP se
mueven alrededor de 0,8–1,2; se dejan seis órdenes de magnitud de holgura y una
precisión muy superior a la del proveedor. Se rechazan tasas finitas positivas
fuera de rango, con exponente extremo, magnitud excesiva o más de 32 dígitos
significativos. El límite de respuesta externa sigue siendo 64 KiB.

El adaptador construye `ExchangeQuote` antes de escribir la caché. Una tasa
inválida se traduce a `RateUnavailable` y la API responde `503
application/problem+json`; no se redondea para hacerla válida, no se cachea, no se
convierte en `500` y no se persiste ninguna fila. Las tasas legítimas y los límites
técnicos siguen siendo calculables.

Las pruebas cubren tasas legítimas y de alta precisión, límites `0.000001` y
`1000000`, exponentes `1e10000`/`1e999999`/`1e-10000`, magnitud `1000000.1`,
precisión de 33 dígitos, cero, negativo, `NaN`, `Infinity`, recuperación tras una
respuesta inválida y no contaminación de caché. En API se prueba preview y
guardado con `503`, ausencia de filas parciales, historial vacío, recuperación y
EUR operativo.

## 6. Revisión de A39-07 a A39-11

- **A39-07 — errores sin registro:** confirmado. `_handle_unexpected_error`
  devuelve un 500 genérico sin logging. No se añadió logging estructurado porque
  no estaba autorizado. Clasificación: **PENDIENTE DE AUTORIZACIÓN**.
- **A39-08 — puerto de clientes amplio:** confirmado. `CalculateSimulation` recibe
  `CustomerRepository` y solo usa `get_country_by_id`. No se creó
  `CustomerCountryReader` porque no estaba autorizado. Clasificación:
  **PENDIENTE DE AUTORIZACIÓN**.
- **A39-09 — campos desconocidos en clientes:** confirmado y aprobado por Q-26.
  Simulaciones usan `extra="forbid"`; clientes conservan `ignore`. La asimetría
  queda documentada. Clasificación: **RIESGO ACEPTADO**.
- **A39-10 — prueba de arquitectura estática:** confirmado. La prueba cubre imports
  absolutos y relativos resolubles; no detecta cargas dinámicas. No se encontraron
  imports dinámicos en `src/`. Clasificación: **RIESGO ACEPTADO**.
- **A39-11 — búsqueda con escaneo completo:** confirmado. `LIKE`/UDF por fila no
  tiene índice; el coste es lineal. Para el volumen actual es aceptable; FTS5 o
  columna normalizada quedan para una revisión futura. Clasificación:
  **DIFERIDO**.

## 7. Revisión de A39-12 a A39-15

- **A39-12 — sin auth/CORS/límites globales:** no se añadieron. El backend no debe
  exponerse con datos reales antes de resolver autenticación, multi-tenancy,
  CORS/proxy y límites de cuerpo/tasa. Clasificación: **DIFERIDO** para la fase de
  publicación.
- **A39-13 — DDL SQLite no transaccional:** las migraciones 0003/0004 reconstruyen
  tablas por lotes y los guards de downgrade están probados. Se documenta copia de
  seguridad y prueba en copia antes de migrar datos reales. Clasificación:
  **RIESGO ACEPTADO**.
- **A39-14 — lock global durante FX:** un único lock serializa la consulta externa
  de hasta 5 s. La deduplicación es correcta, pero divisas distintas se serializan.
  Aceptado para el MVP. Clasificación: **RIESGO ACEPTADO**.
- **A39-15 — caché por proceso:** se pierde al reiniciar y no se comparte entre
  workers. Aceptado para el MVP; una caché compartida requiere infraestructura
  nueva. Clasificación: **RIESGO ACEPTADO**.

## 8. Pruebas añadidas y resultados

Distribución de las 41 pruebas nuevas:

| Área | Pruebas | Evidencia |
| --- | ---: | --- |
| Configuración SQLite runtime/Alembic | 12 | `backend/tests/test_database_config.py` |
| Tasas FX legítimas y límites | 6 | `backend/tests/test_frankfurter.py` |
| Recuperación y no contaminación de caché | 1 | `backend/tests/test_frankfurter.py` |
| Respuestas FX inválidas | 6 | `backend/tests/test_frankfurter.py` |
| Límites de tasa en dominio | 12 | `backend/tests/test_monthly_calculation.py` |
| API `503`, sin filas y corrupción de historial | 4 | `backend/tests/test_queries_and_preview.py` |

Resultados reales:

- Baseline: **538 passed in 52.13s**.
- Final: **579 passed in 48.10s**.
- `ruff check .`: correcto.
- `ruff format --check .`: 90 ficheros ya formateados.
- `mypy .`: sin incidencias en 88 ficheros fuente.
- `pip check`: sin requisitos rotos.
- `requirements.lock`: 35 pines, 0 ausentes y 0 discrepancias.

## 9. Validación de configuración, migraciones y repositorio

- `alembic heads`: `0004_add_simulation_taxes_and_fx (head)`.
- `alembic upgrade head` sobre base temporal: 0001 → 0002 → 0003 → 0004 sin
  errores.
- `alembic current`: `0004_add_simulation_taxes_and_fx (head)`.
- Base temporal eliminada; `backend/var/saas_o_matic.sqlite3` no existe.
- `git diff --check`: sin errores.
- Whitespace: 97 ficheros revisados, 0 líneas con espacios finales.
- Secretos/rutas privadas: 97 ficheros revisados, 0 hallazgos.
- Artefactos SQLite de aplicación: 0. Los únicos `.db` encontrados son caché de
  mypy ignorada.
- Staged: 0 ficheros.
- `.docx`: sin seguimiento, no leído ni modificado; SHA-256
  `63fbd74eed52eb5b8f2495e46ffd82e059c8421892c3b6b8517aaed2a9741cdf`, idéntico
  al manifiesto de TASK038.
- Huellas iniciales: 93 candidatos, 78 sin cambios, 15 modificados
  intencionadamente y 0 ausentes. TASK039, 0003 y 0004 conservan su huella.
- Enlaces relativos: 127 enlaces comprobados en 10 documentos, 0 rotos.

## 10. Documentación actualizada

- `docs/requirements/requirements-traceability.md`: delta TASK039B, matriz
  FR-01–FR-12, CH, DISC, evidencias y conclusión.
- `docs/requirements/functional-requirements.md`: versión 1.3, estado y resultados
  TASK039/TASK039B.
- `docs/planning/mvp-roadmap.md`: estado vigente, tabla de tareas, dependencias,
  auditoría/publicación y siguiente paso.
- `ai-workspace/README.md`: estado, estructura e índice de TASK039/TASK039B.
- `backend/README.md`: estado, migraciones, contrato, SQLite, FX, alcance,
  limitaciones y pruebas.
- `.env.example`: configuración real y límites de uso.
- `docs/specs/001-customer-registration/plan.md`: resolución SQLite compartida.
- `docs/specs/005-taxes-and-currency-conversion/spec.md`: límites FX y `503`.
- `docs/specs/006-customer-queries-and-preview/spec.md`: estado TASK039/TASK039B.
- `README.md`: estado TASK039B, 579 pruebas y configuración SQLite.

## 11. Checklist de 28 puntos

| # | Punto | Resultado |
| ---: | --- | --- |
| 1 | Objetivo y alcance TASK039B | Delimitado a A39-01/02/03/04/06, A39-05 documental y revisión 07–15. |
| 2 | Rama y HEAD | `feature/mvp-backend`; HEAD sin cambios. |
| 3 | Estado inicial y baseline | 538 pruebas; 56 modificados, 38 sin seguimiento, 0 staged. |
| 4 | Autorizaciones respetadas | Sin cambios en TASK039, migraciones, LICENSE, TASK001–039, manifiestos ni docx. |
| 5 | A39-01 | RESUELTO: trazabilidad y documentos de estado corregidos. |
| 6 | A39-02 | RESUELTO: README con 0001–0004 y contrato vigente. |
| 7 | A39-03 | RESUELTO: `.env.example` solo con configuración real. |
| 8 | A39-04 | RESUELTO: resolución SQLite compartida y 12 pruebas. |
| 9 | A39-05 | RIESGO ACEPTADO: 500 controlado, sin ocultación ni reparación. |
| 10 | A39-06 | RESUELTO: límites FX, rechazo antes de caché y 503. |
| 11 | A39-07 | PENDIENTE DE AUTORIZACIÓN: sin logging estructurado. |
| 12 | A39-08 | PENDIENTE DE AUTORIZACIÓN: sin puerto estrecho. |
| 13 | A39-09 | RIESGO ACEPTADO: asimetría Q-26 documentada. |
| 14 | A39-10 | RIESGO ACEPTADO: cobertura estática documentada. |
| 15 | A39-11 | DIFERIDO: optimización de búsqueda futura. |
| 16 | A39-12 | DIFERIDO: auth/CORS/límites antes de exponer. |
| 17 | A39-13 | RIESGO ACEPTADO: DDL SQLite y copia previa. |
| 18 | A39-14 | RIESGO ACEPTADO: lock global FX en MVP. |
| 19 | A39-15 | RIESGO ACEPTADO: caché por proceso en MVP. |
| 20 | Pruebas nuevas | 41 pruebas; 579 finales. |
| 21 | Calidad | Ruff, formato, mypy y pip check correctos. |
| 22 | Lock | 35 pines, 0 ausentes, 0 discrepancias. |
| 23 | Git y whitespace | `git diff --check` limpio; 0 espacios finales. |
| 24 | Huellas | 78/93 sin cambios; TASK039, 0003 y 0004 intactos. |
| 25 | Migraciones | Heads/current 0004; upgrade completo en base temporal. |
| 26 | Secretos y rutas | 0 hallazgos; sin base SQLite de aplicación. |
| 27 | Staged y docx | 0 staged; docx sin cambios y sin seguimiento. |
| 28 | Estado final | Local, sin publicación; TASK040 requiere autorización. |

## 12. Riesgos residuales y decisiones pendientes

- A39-07 y A39-08 requieren autorización específica antes de cambiarse.
- A39-12 debe resolverse antes de exponer el backend con datos reales.
- A39-11, A39-14 y A39-15 son aceptables para el MVP, pero deben revisarse si
  crece el volumen o se añaden workers.
- A39-13 exige copia de seguridad y prueba en copia antes de migrar datos reales.
- No se eligieron límites comerciales de FX; los valores implementados son cotas
  técnicas de plausibilidad.
- No se verificó cobertura porcentual, SAST/DAST, CVE, carga, concurrencia
  multi-worker, accesibilidad, responsive, CI/CD ni despliegue.
- La auditoría TASK039/TASK039B es metodológica; no sustituye una revisión humana
  externa.

## 13. Estado Git y publicación

- Rama: `feature/mvp-backend`.
- HEAD: `b3c5ca81d23d279b478ed466757bada031aa1e1e`.
- Estado final: 58 ficheros modificados, 40 sin seguimiento, 0 eliminados y 0 staged.
- Índice: vacío.
- Sin commit, push, PR, merge, rebase, stash, reset, clean ni force-push.
- Sin publicación. TASK040 requiere autorización específica del propietario.

## 14. Conclusión

TASK039B deja aplicadas las correcciones autorizadas, con pruebas de regresión y
documentación coherente. El backend sigue siendo una implementación local del
alcance aprobado, no publicada y sin frontend. TASK039 mantiene su dictamen **APTA
CON OBSERVACIONES**; TASK039B no introduce hallazgos bloqueantes nuevos y deja
explícitos los riesgos aceptados, diferidos y pendientes de autorización.
