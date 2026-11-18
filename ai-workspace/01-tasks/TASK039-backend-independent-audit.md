# TASK039 — Auditoría técnica independiente del backend acumulado

| Campo | Valor |
| --- | --- |
| Tarea | TASK039 — auditoría independiente, de solo lectura, del backend TASK035–TASK038 |
| Fecha | 2026-11-18 |
| Base auditada | Rama `feature/mvp-backend`; HEAD `b3c5ca81d23d279b478ed466757bada031aa1e1e`; `origin/main` en el mismo commit; `main` local en `8371f9f608ce6e06984cc501d8240e1b7edf34d5` |
| Alcance | 92 rutas pendientes de publicación (56 modificadas y 36 nuevas, sin contar el docx) más este informe |
| Veredicto | **APTA CON OBSERVACIONES** |
| Bloqueantes | Ninguno confirmado (0 CRÍTICA, 0 ALTA) |

> **Independencia metodológica.** Los informes de TASK035–TASK038 se han tratado como
> afirmaciones a contrastar, no como evidencia. Cada comprobación relevante se repitió
> con código, base de datos o ejecución propia. El auditor es el mismo agente que
> materializó tareas anteriores, por lo que la independencia es de método, no de
> identidad; se declara expresamente para no presentar esta revisión como una auditoría
> humana externa. No se ha modificado código, pruebas, migraciones, dependencias,
> configuración ni documentación existente.

## 1. Objetivo y alcance

El objetivo es decidir si el backend acumulado en TASK035–TASK038 es apto para una
publicación controlada, antes de iniciar TASK040. La revisión cubre:

- integridad del repositorio y de los cambios pendientes;
- validaciones técnicas reales (pruebas, Ruff, mypy, dependencias);
- requisitos funcionales FR-01–FR-12 en el alcance aprobado;
- arquitectura, puertos, composición y dependencias;
- clientes, identificadores fiscales, precios, impuestos y divisas;
- caché, concurrencia, persistencia histórica y migraciones;
- contratos HTTP, consultas, búsqueda Unicode, paginación y preview;
- seguridad, documentación, preparación para Angular y riesgos residuales;
- los hallazgos previos H-01–H-08 y un flujo integral independiente.

Quedan fuera del alcance: el frontend Angular (no existe), CI/CD, despliegue real,
carga y seguridad ofensiva. Tampoco se lee ni publica el documento original del reto
(`Prueba Devs con IA.docx`), que permanece sin seguimiento en Git.

## 2. Autorización, límites y método

Operaciones autorizadas y ejecutadas: `git fetch origin`, inspección del repositorio,
ejecución de la suite y de comprobaciones existentes, pruebas independientes con bases
de datos temporales y scripts fuera del repositorio, consultas puntuales de solo lectura
a fuentes públicas oficiales y creación de este único informe.

Operaciones prohibidas y no ejecutadas: `git add`, `git commit`, `git push`, creación de
pull requests, merge, rebase, stash, reset, clean, force-push, creación de ramas,
cualquier cambio en `main` local y cualquier modificación de código, pruebas,
migraciones, dependencias, configuración o documentación existente. Tampoco se actualizó
`ai-workspace/README.md`.

Método: lectura del código y de la documentación vigente; reproducción independiente de
los cálculos con oráculos propios en céntimos enteros; sondas HTTP contra la aplicación
ASGI real con bases de datos temporales; ciclos completos de migración; inspección física
de SQLite; pruebas de concurrencia y de caída del proveedor FX. No se usaron porcentajes
de cobertura ni números de línea no verificados. `pip check` se cita solo como
comprobación de consistencia de dependencias, **no** como auditoría de vulnerabilidades.

## 3. Estado de Git y árbol de trabajo (inicial)

| Comprobación | Resultado |
| --- | --- |
| Rama actual | `feature/mvp-backend` |
| HEAD | `b3c5ca81d23d279b478ed466757bada031aa1e1e` |
| `origin/main` | `b3c5ca81d23d279b478ed466757bada031aa1e1e` |
| `main` local | `8371f9f608ce6e06984cc501d8240e1b7edf34d5` |
| Índice (staged) | Vacío |
| Ficheros modificados | 56 |
| Ficheros nuevos sin seguimiento | 36, más `Prueba Devs con IA.docx` |
| Ficheros borrados | 0 |
| Artefactos ignorados | `TASKS.zip`, cachés, `.venv`, `*.egg-info`, bases SQLite locales |

El árbol contiene 92 rutas candidatas a publicación, excluyendo el docx. No hay cambios
preparados ni publicados. `main` local no se ha tocado.

## 4. Integridad del repositorio y comparación con TASK037/038

- Se guardó un manifiesto SHA-256 de las 92 rutas candidatas al inicio de la auditoría.
- Las 92 huellas se compararon de nuevo antes de redactar este informe: **0 faltantes y
  0 modificadas**.
- El manifiesto de TASK038 (102 entradas, 39 protegidas) no presenta discrepancias en las
  rutas protegidas. Las diferencias respecto al manifiesto de TASK037 se explican por las
  actualizaciones documentales autorizadas en TASK038.
- `LICENSE`, `backend/migrations/env.py` y las migraciones `0001` y `0002` no han cambiado
  respecto a HEAD.
- Las migraciones `0003` y `0004` y los registros de TASK035–TASK038 siguen presentes e
  intactos.
- El docx sigue sin seguimiento y no forma parte de los candidatos.
- No existía ningún `TASK039-backend-independent-audit.md` antes de esta tarea.

La comprobación final, ejecutada después de escribir este informe, se detalla en la
sección 30.

## 5. Validaciones técnicas ejecutadas

| Comprobación | Resultado real |
| --- | --- |
| `pytest` (suite completa) | **538 pruebas superadas**, 33,47 s |
| `ruff check` | Sin hallazgos |
| `ruff format --check` | 89 ficheros correctos |
| `mypy` | 87 ficheros, sin errores |
| `pip check` | Sin dependencias rotas |
| Pines de dependencias | 35 versiones instaladas coinciden con la metadata; sin entradas extra en `pip freeze` |
| Python | 3.13.17 |
| Versiones clave | FastAPI 0.163.1, Pydantic 2.14.3, SQLAlchemy 2.1.8, Alembic 1.20.1, httpx 0.28.1, pytest 9.2.0, Ruff 0.17.5, mypy 2.4.1, uvicorn 0.54.0 |

No se midió cobertura. No se ejecutaron análisis SAST/DAST, escaneo de CVE, pruebas de
carga ni pruebas de navegador. `pip check` no detecta vulnerabilidades; solo verifica que
las dependencias declaradas son coherentes entre sí.

## 6. Requisitos funcionales FR-01–FR-12

| Requisito | Backend local | Frontend | Observación |
| --- | --- | --- | --- |
| FR-01 Alta de clientes | Completado | Pendiente | Seis países, plan `standard`, validación estricta. |
| FR-02 Validación fiscal | Completado en alcance | Pendiente | Algoritmos oficiales ES (DNI/NIF/NIE/CIF); validación genérica normalizada fuera de ES. |
| FR-03 Simulaciones persistidas | Completado | Pendiente | Alta y persistencia con FK; sin edición ni borrado. |
| FR-04 Usuarios, GB y llamadas API | Completado | Pendiente | Rangos aprobados; enteros estrictos; NULL históricos. |
| FR-05 Tramos progresivos | Completado | Pendiente | 0 usuarios admitido; 15 usuarios = 140,00 EUR. |
| FR-06 Impuestos por país | Completado | Pendiente | IVA general de seis países, snapshot y HALF_UP. |
| FR-07 Búsqueda y dashboard | Backend completado | Pendiente | Listado/búsqueda Unicode; dashboard Angular no existe. |
| FR-08 Detalle e historial | Backend completado | Pendiente | Detalle e historial paginado; tarjetas responsive pendientes. |
| FR-09 Simulador y preview | Backend completado | Pendiente | Preview sin escritura y guardado explícito; slider pendiente. |
| FR-10 Divisas | Completado en alcance | Pendiente | EUR/USD/GBP aprobados (Q-07); “otras divisas” no aprobadas. |
| FR-11 Persistencia de conversión | Completado | Pendiente | Snapshot con base EUR, divisa, tasa, fecha, fuente y total convertido. |
| FR-12 Periodicidad mensual | Completado | Pendiente | `billing_period="monthly"` persistido y devuelto. |

El backend cubre la parte funcional de los doce requisitos en el alcance aprobado. No se
declara completado el MVP ni el frontend. La ausencia de Angular impide verificar el
flujo visual E2E y los criterios de interfaz.

## 7. Arquitectura y dependencias

- El análisis AST independiente no encontró violaciones de capas: `domain` solo importa
  `domain`; `application` importa `application` y `domain`; `infrastructure` importa
  `domain` e `infrastructure`; `presentation` importa `application` y `presentation`;
  `bootstrap` compone todas.
- `domain` no importa FastAPI, Pydantic, SQLAlchemy, Alembic, Starlette, uvicorn ni httpx.
- No se detectaron ciclos de importación ni imports dinámicos (`importlib`, `__import__`)
  en `src/`.
- Los puertos viven en el dominio y los adaptadores en infraestructura. La composición se
  concentra en `bootstrap`.
- `CalculateSimulation` se reutiliza en creación y preview; `MonthlyEstimator` se comparte
  mediante una instancia cacheada; no hay duplicación del motor de precios ni del catálogo
  fiscal.
- `calculate_user_subtotal` solo se invoca desde `CalculateSimulation`;
  `calculate_monthly` solo desde `MonthlyEstimator`.
- La prueba de arquitectura es estática y no cubre imports dinámicos; está documentado y
  no se encontraron imports dinámicos. Se registra como A39-10.
- El puerto `CustomerRepository` que recibe el calculador es más amplio de lo necesario
  (incluye escritura) y se usa en una ruta de solo lectura; se registra como A39-08.

## 8. Clientes y validación de identificadores fiscales

Verificado con sondas HTTP independientes:

- Seis países admitidos: ES, PT, FR, DE, IT y NL.
- España: DNI, NIF, NIE y CIF con algoritmos de comprobación; se aceptan ejemplos válidos y
  se rechazan inválidos.
- Fuera de España: validación genérica normalizada, sin presentarla como algoritmo oficial.
- Se rechazan caracteres de control, longitudes fuera de rango, países no admitidos y
  planes distintos de `standard`.
- Unicidad por `(country, tax_id)`: duplicado en el mismo país devuelve `409`; el mismo
  identificador en otro país devuelve `201`.
- La razón social se normaliza; el email se valida.
- Los campos desconocidos en `POST /customers` se ignoran. Es el comportamiento aprobado
  por Q-26 (“simulaciones `extra="forbid"`, no clientes”), no un defecto. Se registra como
  A39-09.

## 9. Pricing

Oráculo independiente en céntimos enteros, sin reutilizar el código de producción:

- Tramos 1–10 a 10,00 EUR; 11–50 a 8,00 EUR; 51+ a 5,00 EUR; 0 usuarios = 0,00 EUR.
- 15 usuarios = 140,00 EUR; 1.000.000 = 5.000.170,00 EUR; 10^40 usuarios se calcula de
  forma exacta.
- **0 discrepancias** en los límites y en 500 valores aleatorios deterministas.
- Los importes son `Decimal`; no se usa `float` en el dominio.
- Se rechazan `bool`, `float`, `str`, `None` y negativos, sin coerciones.
- La función es independiente del contexto Decimal del llamador: con `prec=2`, `Emax=5`,
  `rounding=ROUND_DOWN` y trampas activas, los resultados siguen siendo exactos.
- No hay constantes de precios duplicadas: el único origen es `domain/pricing/schedule.py`.

## 10. Impuestos

- Catálogo único y versionado: `general-vat-2026-11-17-v1`, verificado el 2026-11-17.
- Tipos generales: ES 21 %, PT 23 %, FR 20 %, DE 19 %, IT 22 %, NL 21 %.
- Todas las fuentes del catálogo usan HTTPS.
- Contraste puntual con fuentes oficiales públicas: los seis tipos generales coinciden.
- Oráculo independiente en céntimos enteros: **0 discrepancias** en seis países × 11
  subtotales.
- ES con 15 usuarios: subtotal 140,00; impuesto 29,40; total 169,40.
- Redondeo `ROUND_HALF_UP` confirmado: 0,005 → 0,01; 0,015 → 0,02; 0,0049 → 0,00.
- El impuesto se calcula sobre el subtotal EUR y se persiste en el snapshot.
- El catálogo es estático y sustituible por inyección; no se consulta un servicio fiscal
  externo. No se cubren tipos reducidos, exenciones ni reglas territoriales especiales,
  fuera del alcance aprobado.

## 11. Divisas y proveedor FX

- Único proveedor: Frankfurter v2; EUR/USD/GBP; EUR es identidad y no usa red.
- TTL de 24 h desde la obtención; timeout de 5 s.
- Validación estricta de la respuesta: objeto JSON, par `EUR/<divisa>` coherente, tipos
  correctos, fecha ISO válida y no futura, tasa positiva y finita, sin claves duplicadas.
- Se rechazan JSON inválido, respuestas incompletas, moneda incorrecta, tasa cero,
  negativa, `NaN`, `Infinity`, fechas inválidas o futuras, objetos y booleanos.
- Se aceptan tasas de alta precisión (se conservan exactamente) y campos extra.
- Timeout, error de conexión y HTTP 500 se traducen a `RateUnavailable`.
- Tras un fallo, la siguiente petición puede recuperarse; los errores no se cachean.
- Consulta real puntual de solo lectura: USD 1,0994 y GBP 0,83358 con fecha 2026-11-18.
  No se ha hecho depender la suite de Internet.
- Se aceptan exponentes extremos (`1e10000`, `1e999999`). Con `1e10000` se genera un total
  convertido de más de 10.000 dígitos; con `1e999999` el desbordamiento de `Decimal` se
  traduce a `InvalidCalculation` y la API responde `500` en lugar de `503`. Se registra
  como A39-06.

## 12. Caché y concurrencia

- La caché está separada por divisa y se guarda en memoria del proceso.
- TTL comprobado con reloj monotónico: a 24 h − 1 s no se repite la consulta; a 24 h
  exactas se renueva.
- EUR no realiza ninguna llamada externa.
- Los fallos no se almacenan: una divisa solicitada dos veces tras un error vuelve a
  intentar la consulta.
- Con 6 hilos concurrentes sobre la misma divisa se realizó **una sola** llamada externa y
  todos recibieron la misma tasa.
- El lock se mantiene durante la llamada de red, por lo que divisas distintas se
  serializan; se registra como A39-14.
- La caché es por proceso, se pierde al reiniciar y no se comparte entre workers; se
  registra como A39-15.

## 13. Persistencia histórica y snapshots

- Los importes se almacenan como `TEXT` decimal canónico, no como `float`.
- El snapshot fiscal/FX se almacena como JSON y conserva tasa, fuente, versión, territorio,
  fecha de verificación, fecha de obtención, divisa, tasa de cambio y total convertido.
- Una simulación histórica sin snapshot devuelve `200` con todos los campos fiscales y FX
  a `NULL`, `billing_period="monthly"` y `created_at` en UTC con sufijo `Z`. No se inventa
  EUR, cero ni una tasa actual.
- Una sesión nueva, con un catálogo alternativo (ES al 99 %) y un proveedor FX que falla,
  sigue leyendo la tasa 0,21, el impuesto 29,40, el total 169,40 y la versión original. El
  histórico no depende del catálogo ni del FX actuales.
- Los tipos físicos de SQLite son `text` para `user_subtotal_eur` y
  `calculation_snapshot`, y `null` para los consumos históricos ausentes.
- Una matriz de 10 variantes de snapshot corrupto devuelve `500`
  `application/problem+json` sin filtrar la traza. Una sola fila corrupta rompe toda la
  página de historial; se registra como A39-05.
- No hay backfill ni recálculo de históricos.

## 14. Migraciones

Ciclo independiente verificado con bases temporales:

- Vacío → head y head → base funcionan.
- `0001` → `0002` → `0003` con datos conserva identificadores, importes, relaciones y
  fechas.
- `0003` añade consumos y `billing_period` con valor por defecto `monthly`, sin inventar
  datos históricos.
- `0004` añade el snapshot nullable.
- Las restricciones CHECK rechazan rangos y tipos inválidos; `user_count=0` se acepta
  después de `0003`.
- El downgrade de `0004` se bloquea si hay snapshots y la columna permanece; el de `0003`
  se bloquea si hay consumos y las columnas permanecen.
- Los downgrades compatibles y el re-upgrade funcionan.
- La unicidad compuesta `(country, tax_id)` y la FK de simulaciones se aplican.
- `PRAGMA foreign_key_check` está vacío en todo el ciclo.
- SQLite usa DDL no transaccional y `0003`/`0004` reconstruyen tablas por lotes; las
  migraciones comprueban FKs antes y después y protegen los downgrades, pero un fallo a
  mitad de reconstrucción podría dejar un estado parcial. Se registra como A39-13.

## 15. Contratos HTTP y errores

- Seis endpoints: `POST /customers`, `GET /customers`, `GET /customers/{id}`,
  `GET /customers/{id}/simulations`, `POST /simulations` y
  `POST /simulations/preview`.
- Códigos observados: `201`, `200`, `409`, `422`, `404`, `503`, `405` y `500` controlado.
- Los éxitos usan `application/json`; los errores usan `application/problem+json` con
  `type`, `title`, `status`, `detail`, `instance` y, cuando aplica, `errors`.
- Los importes se serializan como cadenas decimales; las fechas en UTC.
- La paginación devuelve `items`, `total`, `limit` y `offset`; los límites son 1..100 y el
  offset no negativo.
- UUID inválido, cuerpo incompleto, tipos incorrectos y campos desconocidos en
  simulaciones devuelven `422`.
- `SimulationCreateRequest` declara `additionalProperties=false`; el preview comparte el
  mismo esquema de entrada.
- El preview no devuelve `id` ni `created_at`; el historial declara los campos históricos
  como nullable.
- No se emite cabecera `Location`, decisión aprobada.
- Un cuerpo de 100 KB se rechaza con `422` por longitud de campo; no se observó un límite
  global de tamaño de cuerpo.
- El `500` genérico no filtra la traza.

## 16. Consultas, búsqueda Unicode, paginación y aislamiento

- Búsqueda parcial por `legal_name` o `tax_id`, con `casefold` Unicode.
- `École`/`ÉCOLE`, `Müller`/`MÜLLER` y `Straße`/`STRASSE` coinciden.
- No se eliminan acentos: `nandu` no encuentra `Ñandú`. Es el comportamiento documentado.
- `%`, `_` y la barra inversa se tratan como literales.
- Cargas con aspecto de SQL (`' OR 1=1 --`, `"; DROP TABLE customers; --`,
  `' UNION SELECT 1 --`) devuelven 0 filas y no alteran la base.
- El historial de un cliente no incluye simulaciones de otro.
- El orden es `created_at DESC, id DESC` y es estable.
- El `total` es independiente de la página; un offset fuera de rango devuelve página vacía
  con el total correcto.
- `limit=0`, `limit=101` y `offset=-1` devuelven `422`.
- La búsqueda usa `LIKE '%término%'` sobre una UDF de `casefold`, lo que fuerza un escaneo
  completo y llamadas Python por fila; no hay índices para esa expresión. Se registra como
  A39-11.

## 17. Previsualización sin escritura y paridad con guardado

- El preview usa el mismo cuerpo, el mismo `CalculateSimulation` y el mismo
  `MonthlyEstimator` que el guardado.
- Con un autorizador de SQLite que deniega `INSERT`, `UPDATE` y `DELETE`, tres previews
  consecutivos devuelven `200` y el número de filas de `simulations` permanece en 0.
- La paridad de datos comerciales se confirmó en EUR, USD y GBP: el preview y el guardado
  coinciden en subtotal, impuesto, total, divisa, tasa y total convertido, salvo `id` y
  `created_at`.
- Con FX caído y caché vacía, preview y guardado devuelven `503`; no se crean filas
  parciales. EUR y el historial siguen funcionando.
- El preview no recibe un repositorio de simulaciones, pero sí un `CustomerRepository`
  con capacidad de escritura; se registra como A39-08.

## 18. Seguridad y gestión de riesgos

- No se encontraron secretos, tokens, claves privadas, rutas absolutas de Windows, rutas
  de usuario ni correos personales en las 92 rutas candidatas. Los correos son sintéticos
  (`example.com`, `ejemplo.es`).
- No hay ficheros `.env`, bases SQLite, logs ni ficheros `.db` entre los candidatos.
- No hay URLs externas controladas por el usuario; el único destino es Frankfurter, por lo
  que no se identificó un vector SSRF.
- Las consultas están parametrizadas y los comodines de búsqueda se escapan.
- La FK y la integridad referencial se aplican por conexión; `foreign_key_check` e
  `integrity_check` están limpios.
- Los repositorios hacen rollback ante error; un alta duplicada deja una sola fila y no
  crea huérfanos.
- No hay autenticación, autorización ni multi-tenancy; es una exclusión aprobada y está
  documentada. La aplicación no debe exponerse públicamente con datos reales.
- No hay middleware CORS ni límite global de tamaño de cuerpo o de tasa de peticiones. Se
  registra como A39-12.
- `pip check` no es una auditoría de vulnerabilidades; no se ejecutó un escaneo CVE.

## 19. Hallazgos previos H-01–H-08

| ID | Estado | Evidencia independiente |
| --- | --- | --- |
| H-01 | Resuelto | Con contexto hostil (`prec=2`, `Emax=5`, `ROUND_DOWN`, trampas) los subtotales, productos y formatos siguen siendo exactos; el contexto global no se altera. |
| H-02 | Atendido | Existen pruebas de regresión para TEXT, sesión nueva, `Decimal`/UTC, 15 usuarios y límites; no se midió cobertura. |
| H-03 | Resuelto | `calculate_user_subtotal`, `rounded_product` y `format_eur_amount` crean un `Context` propio; no heredan precisión, `Emax`/`Emin`, trampas ni redondeo del llamador. |
| H-04 | Resuelto | El orden es validar → comprobar cliente → pricing → estimador. Con cliente inexistente no se invoca pricing; con payload inválido tampoco. |
| H-05 | Resuelto en simulaciones | Simulaciones rechazan campos desconocidos con `422`; clientes los ignoran, conforme a Q-26. |
| H-06 | Riesgo residual | La unicidad y la FK cubren la carrera; un alta duplicada se traduce a `DuplicateCustomerTaxId`, hace rollback y deja una sola fila. El riesgo de carrera sigue existiendo, mitigado por la restricción. |
| H-07 | Riesgo residual | No hay CHECK monetario en SQLite; el SQL directo acepta `'no-es-un-importe'` y `'1.234'`, pero la reconstrucción los rechaza y no los transforma en datos válidos. |
| H-08 | Atendido parcialmente | Se corrigieron incoherencias previas, pero quedan afirmaciones desactualizadas en la matriz de trazabilidad, el README del backend y `.env.example` (A39-01, A39-02 y A39-03). |

## 20. Preparación para Angular

El contrato backend es suficiente para construir el listado, la búsqueda, el formulario, el
detalle, el historial, el slider, el preview y el guardado:

- seis endpoints con contratos claros y OpenAPI;
- errores `problem+json` consumibles;
- paginación explícita;
- preview sin escritura y guardado explícito;
- históricos con `null` para datos desconocidos;
- importes como cadenas decimales;
- divisa de visualización en el cuerpo de simulación/preview.

Quedan pendientes, como trabajo de frontend/integración y no como defectos del backend:
CORS o proxy de desarrollo, URL base configurable, cancelación de peticiones, estados de
carga y error, representación de `null` históricos, formato de importes y el propio slider.
No existe Angular, por lo que el flujo visual E2E no se puede verificar (NO VERIFICADA).

## 21. Documentación y coherencia

- El README raíz describe correctamente el estado local, los seis endpoints, los rangos,
  el `503`, la ausencia de frontend y la exclusión de autenticación.
- El README del backend es detallado, pero contiene referencias obsoletas a migraciones
  0001–0003, una nota de TASK036 que dice “sin impuestos ni divisas” y una mención de
  `DATABASE_URL` que solo aplica a Alembic (A39-02 y A39-04).
- La matriz de trazabilidad conserva tablas de partida y una conclusión (sección 8) que
  afirma que faltan impuestos, divisas, búsqueda, historial y preview, en contradicción con
  el delta de TASK037/038 y con el código (A39-01).
- La hoja de ruta identifica el estado de partida como histórico y el delta vigente; es
  coherente, aunque el lector debe interpretar las tablas inferiores con ese delta.
- `.env.example` es una plantilla provisional que define variables no consumidas por el
  runtime, con una ruta de base distinta (A39-03).
- `ai-workspace/README.md` refleja el estado previo a TASK039; no se actualiza en esta
  tarea por restricción expresa.

## 22. Seguridad de publicación

Las 92 rutas candidatas son aptas para revisión y publicación controlada: no contienen
secretos, credenciales, bases de datos, logs ni rutas privadas. Los manifiestos de
TASK037/038 contienen solo rutas relativas y huellas. El docx permanece sin seguimiento y
no se publica. Este informe no incluye rutas absolutas ni datos personales.

Antes de la publicación documental se recomienda corregir A39-01, A39-02 y A39-03, y antes
de un despliegue real, A39-04. Ninguna de estas correcciones es un cambio de código
funcional ni bloquea la auditoría.

## 23. Flujo integral independiente

Se reprodujo un flujo completo con una base temporal creada por Alembic y la aplicación
ASGI real:

1. Altas de clientes en FR, DE y ES, incluidos `École Müller`, `Straße Nord` y
   `Ñandú Ibérica`.
2. Búsquedas `école`, `ÉCOLE`, `École`, `müller`, `MÜLLER`, `straße` y `STRASSE` con
   coincidencias correctas; `nandu` no coincide con `Ñandú` (sin eliminación de acentos).
3. Detalle del cliente e historial inicial vacío.
4. Preview de 15 usuarios: 140,00 de subtotal, 29,40 de impuesto y 169,40 de total; no se
   persiste ninguna fila.
5. Guardados EUR, USD y GBP: 169,40 / 182,95 / 145,68, con tasas 1 / 1,08 / 0,86 y
   redondeo HALF_UP.
6. Historial en orden DESC, con snapshots y tipos físicos `text`; lectura correcta en una
   sesión nueva.
7. Caída de FX: guardado y preview USD/GBP devuelven `503`, no se crean filas, EUR y el
   historial siguen respondiendo; tras calentar la caché, la tasa cacheada se reutiliza.
8. `foreign_key_check` e `integrity_check` limpios al final.

## 24. Rendimiento y consumo de recursos

- El cálculo de precios recorre tres tramos, no los usuarios; 1.000.000 y 10^40 se calculan
  sin bucles proporcionales.
- El cálculo fiscal y la conversión son operaciones `Decimal` acotadas.
- La respuesta FX se limita a 64 KB; una tasa extrema puede amplificar el total convertido
  (A39-06).
- La búsqueda puede escanear la tabla y ejecutar una UDF por fila (A39-11).
- No se observaron consultas N+1 en el historial: se hace un COUNT y una consulta paginada.
- No se ejecutaron pruebas de carga, estrés ni concurrencia multi-worker.

## 25. Observabilidad y diagnóstico

- No se encontró configuración de logging en la aplicación.
- El manejador de errores inesperados devuelve un `500` genérico sin registrar la excepción
  (A39-07).
- Los logs de acceso de uvicorn, si se activan, no incluyen cuerpos de petición.
- No hay identificador de correlación, métricas ni trazas.
- Un snapshot corrupto o un importe almacenado inválido produce un `500` controlado, pero
  sin diagnóstico en logs; la fila afectada no se identifica.

## 26. Riesgos residuales y deuda técnica

| Riesgo | Estado | Mitigación actual | Recomendación |
| --- | --- | --- | --- |
| Snapshot corrupto rompe el historial | Aceptado | `500` controlado, sin datos inventados | Aislar por fila y registrar la fila (A39-05/A39-07). |
| Tasa FX extrema | Aceptado | Límite de 64 KB y validación de tipos | Acotar magnitud y mapear overflow a `503` (A39-06). |
| DDL no transaccional en SQLite | Aceptado | Comprobaciones de FK y guards | Copia de seguridad y prueba en copia (A39-13). |
| Caché por proceso | Aceptado | TTL y deduplicación por lock | Caché compartida si se añaden workers (A39-15). |
| Sin autenticación/multitenancy | Exclusión aprobada | Herramienta interna | No exponer públicamente; añadir antes de producción (A39-12). |
| Sin límite global de cuerpo/rate | Aceptado | Validaciones de campo | Añadir límites en despliegue (A39-12). |
| Documentación desactualizada | Abierto | Delta en la parte superior | Corregir A39-01, A39-02 y A39-03. |
| `DATABASE_URL` solo en Alembic | Abierto | La ruta local coincide si se ejecuta desde `backend/` | Alinear runtime o documentar (A39-04). |

## 27. Hallazgos de la auditoría

### Resumen

| ID | Severidad | Tipo | Bloqueante |
| --- | --- | --- | --- |
| A39-01 | BAJA | Documentación/trazabilidad | No |
| A39-02 | BAJA | Documentación | No |
| A39-03 | BAJA | Configuración/documentación | No |
| A39-04 | BAJA | Configuración de runtime/despliegue | No |
| A39-05 | BAJA | Robustez/observabilidad | No |
| A39-06 | OBSERVACIÓN | Robustez FX | No |
| A39-07 | OBSERVACIÓN | Observabilidad | No |
| A39-08 | OBSERVACIÓN | Arquitectura/ISP | No |
| A39-09 | OBSERVACIÓN | Validación aprobada | No |
| A39-10 | OBSERVACIÓN | Cobertura de pruebas arquitectónicas | No |
| A39-11 | OBSERVACIÓN | Rendimiento de búsqueda | No |
| A39-12 | OBSERVACIÓN | Seguridad/alcance | No |
| A39-13 | OBSERVACIÓN | Migraciones/SQLite | No |
| A39-14 | OBSERVACIÓN | Concurrencia FX | No |
| A39-15 | OBSERVACIÓN | Caché por proceso | No |

### A39-01 — Matriz de trazabilidad con afirmaciones desactualizadas

- **Severidad:** BAJA. **Tipo:** documentación/trazabilidad. **Bloqueante:** No.
- **Fichero y línea:** `docs/requirements/requirements-traceability.md`, sección 3
  (líneas 130–141), línea 190 y sección 8 (líneas 230–232).
- **Evidencia:** la sección 3 marca FR-06 a FR-11 como “Pendiente” o “Parcial”; la línea
  190 cita “340 pruebas locales”; la sección 8 concluye que “faltan impuestos, divisas,
  búsqueda, historial, previsualización y todo el frontend Angular”. El delta de la parte
  superior del mismo documento afirma que TASK037/038 completaron esos componentes backend
  y que la suite tiene 538 pruebas.
- **Reproducción:** leer el documento y compararlo con el delta y con el código de
  `backend/src/saas_o_matic/`; ejecutar la suite (538 pruebas).
- **Esperado:** un estado único y coherente, o secciones históricas etiquetadas como tales.
- **Observado:** afirmaciones contradictorias dentro del mismo documento.
- **Impacto:** un evaluador o revisor puede concluir que el backend está incompleto;
  disminuye la credibilidad de la trazabilidad.
- **Recomendación:** actualizar las secciones 3, 6 y 8 con el delta TASK037/038, o
  etiquetarlas explícitamente como históricas. No requiere cambios de código.
- **Bloqueante:** No.

### A39-02 — README del backend con migraciones y contrato obsoletos

- **Severidad:** BAJA. **Tipo:** documentación. **Bloqueante:** No.
- **Fichero y línea:** `backend/README.md`, línea 255; líneas 223–224; sección “Alembic y
  base de datos” (líneas 297–311).
- **Evidencia:** el árbol indica “Revisiones 0001, 0002 y 0003” y omite `0004`; la nota de
  TASK036 dice “Sin cargos por GB/llamadas, impuestos ni divisas”, aunque TASK037 añadió
  impuestos y FX; la sección de Alembic describe 0001–0003 pero no 0004.
- **Reproducción:** leer el README y listar `backend/migrations/versions/`.
- **Esperado:** árbol y sección de migraciones con 0001–0004; contrato actualizado.
- **Observado:** referencias incompletas y una frase que sugiere ausencia de impuestos y
  divisas.
- **Impacto:** confusión sobre el esquema y los campos de respuesta.
- **Recomendación:** actualizar el árbol, la nota de TASK036 y la sección de Alembic para
  incluir 0004 y el contrato vigente.
- **Bloqueante:** No.

### A39-03 — `.env.example` no alineado con la configuración real

- **Severidad:** BAJA. **Tipo:** configuración/documentación. **Bloqueante:** No.
- **Fichero y línea:** `.env.example`, líneas 1–31.
- **Evidencia:** la plantilla dice que “todavía no existe código que los consuma” y define
  `APP_ENV`, `APP_DEBUG`, `APP_HOST`, `APP_PORT`, `DATABASE_URL` con
  `sqlite:///./data/saas_o_matic.db`, `CORS_ORIGINS`, `EXCHANGE_RATE_API_URL`,
  `EXCHANGE_RATE_API_KEY` y `TAX_RULES_SOURCE`. El runtime no consume esas variables; solo
  Alembic lee `DATABASE_URL`, y la ruta por defecto real es
  `backend/var/saas_o_matic.sqlite3`. Frankfurter no requiere clave y el catálogo fiscal es
  estático.
- **Reproducción:** comparar `.env.example` con `bootstrap/main.py`, `migrations/env.py` y
  `infrastructure/tax_catalog.py`.
- **Esperado:** una plantilla que refleje la configuración real o que esté marcada como
  propuesta futura.
- **Observado:** variables sin efecto y una ruta de base distinta.
- **Impacto:** un despliegue podría configurar valores que no se aplican y migrar una base
  distinta de la que usa la aplicación.
- **Recomendación:** alinear la plantilla o marcarla como no operativa; documentar la ruta
  real y que Frankfurter no necesita clave.
- **Bloqueante:** No (P-05 pendiente).

### A39-04 — El runtime ignora `DATABASE_URL`

- **Severidad:** BAJA. **Tipo:** configuración de runtime/despliegue. **Bloqueante:** No.
- **Fichero y línea:** `backend/src/saas_o_matic/bootstrap/main.py`, línea 35
  (`_DATABASE_PATH`) y línea 47; `backend/README.md`, línea 304.
- **Evidencia:** la aplicación construye el motor con una ruta fija
  `backend/var/saas_o_matic.sqlite3`; `migrations/env.py` sí lee `DATABASE_URL`. El README
  menciona `DATABASE_URL` en la sección de Alembic, pero no advierte de que el runtime no
  la usa.
- **Reproducción:** definir `DATABASE_URL` a una base temporal, ejecutar
  `alembic upgrade head`, arrancar la aplicación y crear un cliente; la fila aparece en la
  base por defecto, no en la temporal.
- **Esperado:** aplicación y migraciones apuntan a la misma base, o la limitación está
  documentada de forma inequívoca.
- **Observado:** migraciones y runtime pueden usar bases distintas.
- **Impacto:** riesgo de desplegar con una base sin migrar o de migrar una base que la
  aplicación no utiliza. En local, la ruta coincide si ambos comandos se ejecutan desde
  `backend/`.
- **Recomendación:** hacer que el runtime respete `DATABASE_URL` o una variable propia, o
  documentar explícitamente que solo afecta a Alembic; añadir una comprobación de arranque.
- **Bloqueante:** No (P-05 pendiente).

### A39-05 — Una fila corrupta rompe toda la página de historial

- **Severidad:** BAJA. **Tipo:** robustez/observabilidad. **Bloqueante:** No.
- **Fichero y línea:** `backend/src/saas_o_matic/application/simulations/queries.py`,
  líneas 18–34; `backend/src/saas_o_matic/presentation/problems.py`, líneas 212–225.
- **Evidencia:** con 10 variantes de `calculation_snapshot` corrupto, el historial devuelve
  `500` `application/problem+json` sin traza. Una sola fila corrupta impide leer el resto
  de la página. Los errores observados varían: `JSONDecodeError`, `KeyError:
  'schema_version'`, `InvalidCalculation`, `ValueError` e `InvalidOperation`.
- **Reproducción:** insertar una simulación con un snapshot corrupto o un
  `user_subtotal_eur` no decimal y solicitar
  `GET /customers/{id}/simulations`.
- **Esperado:** un error controlado que no oculte el resto del historial, y un registro de
  la fila afectada.
- **Observado:** toda la página falla y no hay log.
- **Impacto:** una corrupción puntual deniega el historial completo del cliente y dificulta
  el diagnóstico. La corrupción no es alcanzable a través de la API: los snapshots los
  escribe la aplicación.
- **Recomendación:** aislar la reconstrucción por fila y devolver un marcador o `null`
  controlado sin inventar valores; registrar el `id` y el error. Alternativamente,
  devolver el resto de la página con una advertencia explícita.
- **Bloqueante:** No.

### A39-06 — Tasas FX extremas y overflow no mapeado a 503

- **Severidad:** OBSERVACIÓN. **Tipo:** robustez FX. **Bloqueante:** No.
- **Fichero y línea:** `backend/src/saas_o_matic/infrastructure/frankfurter.py`, líneas
  79–87; `backend/src/saas_o_matic/domain/simulations/calculation.py`, líneas 94–106.
- **Evidencia:** el adaptador acepta `1e10000` y `1e999999`. Con `1e10000` se genera un
  `converted_total` de más de 10.000 dígitos; con `1e999999` el desbordamiento de `Decimal`
  produce `InvalidCalculation("Importe no representable.")`, que no se traduce a
  `RateUnavailable`, por lo que la API responde `500` en lugar de `503`.
- **Reproducción:** inyectar una respuesta FX con `rate=1e999999` y solicitar preview o
  guardado.
- **Esperado:** rechazar magnitudes implausibles (por ejemplo, `0 < rate <= 1e6`) o mapear
  el overflow de cálculo a `503`.
- **Observado:** tasas extremas aceptadas; overflow con `500`.
- **Impacto:** un proveedor comprometido o defectuoso puede provocar un `500` y amplificar
  el tamaño de la respuesta; no se escribe ninguna fila.
- **Recomendación:** acotar la tasa en `ExchangeQuote` o en el adaptador y traducir
  `InvalidCalculation` del estimador a `RateUnavailable`.
- **Bloqueante:** No.

### A39-07 — Errores inesperados sin registro

- **Severidad:** OBSERVACIÓN. **Tipo:** observabilidad. **Bloqueante:** No.
- **Fichero y línea:** `backend/src/saas_o_matic/presentation/problems.py`, líneas
  212–225.
- **Evidencia:** `_handle_unexpected_error` devuelve un `500` genérico sin registrar `exc`;
  no se encontró configuración de logging en la aplicación.
- **Reproducción:** provocar un `500` (por ejemplo, con un snapshot corrupto) y comprobar
  que no hay entrada de log con la excepción.
- **Esperado:** registro de la excepción con un identificador de petición, sin exponer
  detalles al cliente.
- **Observado:** respuesta controlada pero sin diagnóstico.
- **Impacto:** los fallos internos son invisibles en operación.
- **Recomendación:** añadir logging estructurado de excepciones inesperadas.
- **Bloqueante:** No.

### A39-08 — Puerto de clientes más amplio de lo necesario en preview

- **Severidad:** OBSERVACIÓN. **Tipo:** arquitectura/ISP. **Bloqueante:** No.
- **Fichero y línea:** `backend/src/saas_o_matic/application/simulations/calculator.py`,
  línea 35; `backend/src/saas_o_matic/domain/customers/ports.py`.
- **Evidencia:** `CalculateSimulation` recibe `CustomerRepository`, que incluye `add` y
  `exists_by_tax_id`, pero solo usa `get_country_by_id`. `PreviewSimulation` no recibe un
  repositorio de simulaciones (correcto), pero sí el puerto de clientes completo.
- **Reproducción:** inspeccionar la firma del constructor y el uso real del puerto.
- **Esperado:** un puerto de lectura de país para el calculador.
- **Observado:** dependencia con capacidad de escritura en una ruta de solo lectura.
- **Impacto:** riesgo de escritura accidental si el calculador evoluciona; no se explota
  actualmente.
- **Recomendación:** definir un puerto estrecho `CustomerCountryReader`.
- **Bloqueante:** No.

### A39-09 — Campos desconocidos ignorados en clientes

- **Severidad:** OBSERVACIÓN. **Tipo:** validación aprobada. **Bloqueante:** No.
- **Fichero y línea:** `backend/src/saas_o_matic/presentation/customers/schemas.py`;
  `docs/requirements/functional-requirements.md`, línea 24 (Q-26).
- **Evidencia:** `POST /customers` ignora campos desconocidos; `POST /simulations` los
  rechaza con `422`. Q-26 aprueba expresamente esta asimetría.
- **Reproducción:** enviar un campo extra a ambos endpoints.
- **Esperado:** el comportamiento aprobado.
- **Observado:** clientes ignoran; simulaciones rechazan.
- **Impacto:** ninguno funcional; un cliente podría creer que fijó un campo ignorado.
- **Recomendación:** mantener la decisión y documentar la asimetría en la API.
- **Bloqueante:** No.

### A39-10 — La prueba de arquitectura solo analiza imports estáticos

- **Severidad:** OBSERVACIÓN. **Tipo:** cobertura de pruebas arquitectónicas.
  **Bloqueante:** No.
- **Fichero y línea:** `backend/tests/test_architecture.py`; `backend/README.md`, línea
  291.
- **Evidencia:** el análisis cubre imports absolutos y relativos resolubles; no detecta
  `importlib.import_module`, `__import__` ni cargas dinámicas. La limitación está
  documentada y no se encontraron imports dinámicos en `src/`.
- **Reproducción:** leer la prueba y buscar imports dinámicos.
- **Esperado:** la limitación conocida.
- **Observado:** cobertura estática suficiente para el estado actual.
- **Impacto:** bajo; un import dinámico futuro podría eludir la prueba.
- **Recomendación:** mantener la limitación documentada y, opcionalmente, añadir una
  comprobación de imports dinámicos.
- **Bloqueante:** No.

### A39-11 — Búsqueda con escaneo completo y UDF por fila

- **Severidad:** OBSERVACIÓN. **Tipo:** rendimiento. **Bloqueante:** No.
- **Fichero y línea:** `backend/src/saas_o_matic/infrastructure/customers/repositories.py`,
  líneas 58–63; `backend/src/saas_o_matic/infrastructure/database.py`, líneas 41–42.
- **Evidencia:** `LIKE '%término%'` sobre `unicode_casefold(legal_name)` y
  `unicode_casefold(tax_id)`; no hay índices para esas expresiones.
- **Reproducción:** inspeccionar la consulta generada y el esquema.
- **Esperado:** un escaneo aceptado para el MVP.
- **Observado:** coste lineal con el número de clientes.
- **Impacto:** degradación con volúmenes altos; no afecta a la corrección.
- **Recomendación:** documentar y revisar si crece el volumen; valorar FTS5 o una columna
  normalizada.
- **Bloqueante:** No.

### A39-12 — Sin autenticación, CORS ni límites globales

- **Severidad:** OBSERVACIÓN. **Tipo:** seguridad/alcance. **Bloqueante:** No.
- **Fichero y línea:** `README.md`, línea 150; `backend/README.md`, línea 364;
  `backend/src/saas_o_matic/presentation/app.py`.
- **Evidencia:** no hay autenticación, autorización ni multi-tenancy (exclusión aprobada);
  no se encontró middleware CORS; no hay límite global de tamaño de cuerpo ni de tasa. Una
  petición de 100 KB se rechaza por longitud de campo, no por límite de cuerpo.
- **Reproducción:** revisar `app.py` y el alcance aprobado; enviar un cuerpo grande.
- **Esperado:** herramienta interna no expuesta.
- **Observado:** sin controles de exposición.
- **Impacto:** no debe publicarse con datos reales; un cuerpo enorme podría consumir
  memoria.
- **Recomendación:** documentar la restricción y añadir auth/tenant, CORS/proxy y límites
  antes de P-05.
- **Bloqueante:** No.

### A39-13 — DDL no transaccional y reconstrucción de tablas en SQLite

- **Severidad:** OBSERVACIÓN. **Tipo:** migraciones/SQLite. **Bloqueante:** No.
- **Fichero y línea:** `backend/migrations/versions/0003_international_simulations.py`,
  `backend/migrations/versions/0004_add_simulation_taxes_and_fx.py`.
- **Evidencia:** Alembic registra “Will assume non-transactional DDL”; 0003 y 0004
  reconstruyen tablas por lotes. Las migraciones comprueban FKs antes y después y protegen
  los downgrades, pero un fallo a mitad de reconstrucción podría dejar un estado parcial.
- **Reproducción:** leer las migraciones y el log de Alembic; el ciclo completo se ejecutó
  sin fallos.
- **Esperado:** migraciones seguras con copia de seguridad.
- **Observado:** guards y comprobaciones correctos; limitación de SQLite.
- **Impacto:** bajo en local; riesgo operativo en una migración interrumpida.
- **Recomendación:** documentar copia de seguridad/restauración y probar en una copia.
- **Bloqueante:** No.

### A39-14 — Lock global durante la llamada FX

- **Severidad:** OBSERVACIÓN. **Tipo:** concurrencia. **Bloqueante:** No.
- **Fichero y línea:** `backend/src/saas_o_matic/infrastructure/frankfurter.py`, líneas
  59–102.
- **Evidencia:** un único `threading.Lock` se mantiene durante la petición de red (hasta
  5 s). Con 6 hilos se observó una sola llamada externa (deduplicación correcta), pero las
  divisas distintas se serializan.
- **Reproducción:** ejecutar peticiones concurrentes con un proveedor lento.
- **Esperado:** deduplicar sin bloquear divisas distintas.
- **Observado:** bloqueo global.
- **Impacto:** un proveedor lento detiene todas las consultas FX; bajo en el MVP.
- **Recomendación:** locks por divisa o consulta fuera del lock con doble comprobación.
- **Bloqueante:** No.

### A39-15 — Caché en memoria por proceso

- **Severidad:** OBSERVACIÓN. **Tipo:** caché. **Bloqueante:** No.
- **Fichero y línea:** `backend/src/saas_o_matic/infrastructure/frankfurter.py`, líneas 53
  y 102.
- **Evidencia:** `_cache` es un `dict` de instancia; se pierde al reiniciar y no se comparte
  entre workers.
- **Reproducción:** inspeccionar la implementación; reiniciar el proceso y comprobar que
  se vuelve a consultar.
- **Esperado:** caché por proceso para el MVP.
- **Observado:** sin caché compartida.
- **Impacto:** más llamadas externas si se añaden workers; no afecta a la corrección.
- **Recomendación:** documentar; usar caché compartida si se escala horizontalmente.
- **Bloqueante:** No.

## 28. Comprobaciones no realizadas y limitaciones

Las siguientes comprobaciones **no se ejecutaron** y se declaran NO VERIFICADAS:

- Flujo visual E2E con Angular: no existe frontend.
- CORS real en navegador: no hay frontend ni prueba de navegador.
- CI/CD, despliegue, staging y configuración de producción.
- Cobertura de pruebas: no se ejecutó `pytest-cov` ni se calculó porcentaje.
- SAST, DAST, escaneo de CVE y auditoría de dependencias más allá de `pip check`.
- Pruebas de carga, estrés, concurrencia multi-worker y memoria.
- Fuzzing exhaustivo de todos los endpoints; solo se hicieron sondas dirigidas.
- Accesibilidad, responsive y comportamiento visual.
- Cambios futuros de tipos fiscales, fechas de vigencia y tipos reducidos.
- Contenido del docx original del reto; no se lee ni se publica.
- Contenido de `TASKS.zip`; es un artefacto ignorado y no forma parte del repositorio.
- Simulación de un fallo a mitad de migración; la observación A39-13 se basa en el
  comportamiento documentado de SQLite/Alembic y en la inspección del código.

No se ha presentado ninguna de estas comprobaciones como superada.

## 29. Veredicto final

**APTA CON OBSERVACIONES.**

No se confirmó ningún hallazgo CRÍTICO ni ALTA. Los 15 hallazgos son 5 BAJA y 10
OBSERVACIÓN; ninguno es bloqueante para una publicación controlada. El backend cubre los
requisitos funcionales en el alcance aprobado, las validaciones técnicas pasan, la
arquitectura respeta las dependencias, los cálculos son exactos e independientes del
contexto, los históricos son inmutables y el flujo integral funciona sin escrituras en el
preview.

Antes de la publicación documental se recomienda corregir A39-01, A39-02 y A39-03. Antes de
un despliegue real (P-05) se recomienda resolver A39-04 y planificar autenticación,
aislamiento, CORS/proxy y límites (A39-12). A39-05, A39-06 y A39-07 son mejoras de
robustez y observabilidad que no bloquean la revisión actual.

## 30. Anexo: evidencias y estado final

### Evidencias principales

- Suite completa: 538 pruebas superadas.
- Ruff, formato y mypy: sin hallazgos.
- `pip check`: sin dependencias rotas (no es auditoría de vulnerabilidades).
- Oráculo de precios: 0 discrepancias en límites y 500 valores aleatorios; 10^40 exacto.
- Oráculo fiscal: 0 discrepancias en seis países × 11 subtotales; HALF_UP confirmado.
- FX: validación estricta, errores traducidos, recuperación sin caché de error, TTL y
  concurrencia correctos; consulta real puntual USD 1,0994 / GBP 0,83358.
- Histórico: independiente del catálogo y del FX actuales; legacy con `null`; corrupción
  controlada.
- Migraciones: ciclo completo, datos preservados, guards y FKs correctos.
- HTTP: seis endpoints, códigos y problem+json verificados; OpenAPI coherente.
- Consultas: Unicode, literales, aislamiento, orden y paginación verificados.
- Preview: sin DML con autorizador SQLite; paridad con guardado; FX caído sin filas.
- Seguridad: sin secretos, rutas privadas, bases, logs ni SSRF; inyección SQL sin efecto.
- Flujo integral: altas multi-país, búsquedas, preview, guardados EUR/USD/GBP, historial,
  persistencia física, sesión nueva y caída de FX.

### Estado final de Git y del árbol

La comprobación final se ejecutó después de escribir este informe:

- Rama: `feature/mvp-backend`.
- HEAD: `b3c5ca81d23d279b478ed466757bada031aa1e1e` (sin cambios).
- `origin/main`: `b3c5ca81d23d279b478ed466757bada031aa1e1e`.
- `main` local: `8371f9f608ce6e06984cc501d8240e1b7edf34d5` (sin cambios).
- Índice: vacío; no se ejecutó `git add`, commit, push ni PR.
- 92 rutas previas: 0 faltantes y 0 modificadas respecto al manifiesto inicial.
- Candidatos finales: 93 rutas sin contar el docx (92 previas + este informe).
- Docx: sin seguimiento.
- `git diff --check`: sin errores.
- Sin operaciones destructivas ni reescritura de historial.

Los scripts de comprobación se ejecutaron fuera del repositorio, sobre bases temporales, y
no se versionan. Este informe es el único fichero nuevo de la tarea.
