# TASK038 — Consultas, historial y previsualización de simulaciones

| Campo | Valor |
| --- | --- |
| Fecha de cierre | 2026-11-18 |
| Modalidad | Especificación e implementación local, sin publicación |
| Implementador | OpenCode, GPT-6.1 Sol; no auditoría independiente |
| Fuente | Instrucción TASK038 del propietario y continuación en esta conversación |
| Rama | feature/mvp-backend |
| HEAD/origin/main | b3c5ca81d23d279b478ed466757bada031aa1e1e |

## 1. Resumen ejecutivo

Implementados listado/búsqueda Unicode, detalle, historial paginado y preview sin
escrituras. Motor mensual y contratos anteriores conservados. 538 pruebas superadas
frente a 411 iniciales (+127). Sin dependencias, índices ni migraciones nuevas.
Componentes backend del alcance aprobado implementados, pero no UI ni auditoría final.

## 2. Estado Git y huellas

Fetch ejecutado; estado inicial coincide: 45 seguidos modificados, 24 nuevos (69
acumulados), docx no seguido, índice vacío y rama/HEAD esperados. Main local intacto
en 8371f9f608ce6e06984cc501d8240e1b7edf34d5. No rama nueva ni traslado con stash/reset.

Antes de editar se registraron 102 SHA-256 (pendientes, registros y migraciones)
en [TASK038-initial-hashes.json](TASK038-initial-hashes.json). Se comparó su contenido
con el manifiesto inicial temporal. Protegidos: 32 registros existentes TASK001–TASK037,
TASK037-initial-hashes.json, docx, env.py y revisiones0001–0004: 39 huellas intactas.
Los documentos vigentes se actualizaron solo en alcance autorizado.

Estado final: misma rama/HEAD/origin/main, main local intacto, índice vacío; 56 seguidos
modificados y 36 nuevos acumulados (92), docx aparte. TASK038 afecta 41 rutas frente
al estado inicial; las otras 51 pendientes conservan su contenido inicial.

## 3. Decisiones consolidadas

Q-09/Q-24/SIM-P10: historial inmutable por API, sin editar/borrar. Q-24/SIM-P11:
GET listado/detalle/historial, paginación20/100/offset y orden determinista.
Q-25: POST preview sin persistir y mismo cálculo de creación. Se conserva ausencia
de Location; no GET individual de simulación aprobado. P-01/P-05 pendientes.

## 4. Especificación y arquitectura

SPEC-006/spec, plan y tareas creados antes del código. Monolito modular intacto:
puertos de lectura segregados en dominio, casos de uso/DTO en aplicación, SQL en
infraestructura y esquemas/rutas en presentación. Bootstrap conecta dependencias
con sesiones por petición y MonthlyEstimator compartido. Dominio sin frameworks;
presentación no importa dominio. Sin servicios nuevos ni herramientas adicionales.

## 5. Listado y búsqueda

GET /customers, search opcional recortado, máximo255 tras recortar; vacío sin filtro.
Coincidencia parcial OR legal_name/tax_id. LIKE parametrizado, `%`, `_` y barra
inversa escapados como literales; entradas tipo SQL tratadas como datos.
Orden nombre casefold ASC con colación binaria SQLite, después UUID ASC.
COUNT y LIMIT/OFFSET en SQLite: como máximo dos SELECT, sin cargar tablas enteras.
Offset fuera de total produce [] y conserva total, incluso offsets mayores que
el entero enlazable de SQLite (se evita construir la consulta de página en ese caso).

## 6. Unicode

UDF unicode_casefold registrada por conexión con Python str.casefold; columnas y
patrón usan la misma transformación. É/é y Ü/ü coinciden; ß/ss también por casefold.
No eliminación de acentos, NFC/NFKC, búsqueda difusa ni colación lingüística.
École/ecole no coinciden; formas Unicode compuestas/descompuestas pueden diferir.
Alternativa descartada: SQLite lower/NOCASE nativos, limitados en Unicode. También
descartado filtrar todas las filas en Python. UDF no altera esquema ni necesita índice.

## 7. Detalle de cliente

GET /customers/{customer_id}: reutiliza CustomerResponse, incluidos UUID, razón
social, fiscal, correo, país, plan y created_at existente UTC. Sin estadísticas ni
historial embebido. 200/404/422/500 problem+json cuando procede. Los placeholders
usan customer_id en código/OpenAPI por coherencia con DTO; URI real igual a /{id}.

## 8. Historial y paginación

GET /customers/{customer_id}/simulations. Tras validar parámetros, verificar
cliente antes de consultar simulaciones. Página filtrada por customer_id; orden
created_at DESC, id DESC. Como máximo tres SELECT (existencia/COUNT/página), sin
N+1. limit20 (1..100), offset0 no negativo; total previo a paginación.
Cliente existente sin datos200 vacío; ausente404; UUID/parámetros inválidos422.
No endpoints de edición/borrado ni protección append-only adicional en SQL directo.

## 9. Compatibilidad histórica

Tres generaciones representadas en pruebas: TASK032 (consumos/snapshot desconocidos),
TASK036 (consumos conocidos/snapshot desconocido) y TASK037 (snapshot completo).
Campos desconocidos siempre NULL, no cero, EUR ni país actual inferidos. Subtotal
se distingue de total con impuestos. Snapshot exacto conserva tasas, importes,
fuentes, versiones y fechas. Recuperación usa mapeador existente y validación de
integridad con referencias almacenadas, no nuevos importes ni catálogo actual.
Pruebas hacen fallar MonthlyEstimator, catálogo y proveedor si fueran consultados
por historial; sigue disponible. También se cambia país actual en una base temporal
y se comprueba conservación del país fiscal histórico. Filas físicas antes/después
de GET permanecen idénticas. No migraciones ni backfill.

## 10. Previsualización

POST /simulations/preview reutiliza exactamente SimulationCreateRequest. 200 con
customer_id, consumos, mensual, subtotal y todos los metadatos fiscales/FX de SPEC-005.
Sin id ni created_at de registro ni Location. Sí incluye obtención FX, que es un
metadato de referencia, no persistencia. EUR predeterminado/identidad; USD/GBP con
misma caché. 404/422/503/500 problem+json. No cotización bloqueada ni token de reserva.

## 11. Reutilización de cálculo

CalculateSimulation extrae validación técnica, existencia/país, pricing y llamada a
MonthlyEstimator. CreateSimulation añade UUID/fecha y persiste; PreviewSimulation
solo transforma el resultado y no recibe repositorio de simulaciones. No duplicadas
tarifas ni fórmulas. Ambos usan mismo estimador/catálogo/proveedor/caché de bootstrap.
Paridad comercial probada con referencias idénticas; timestamps de obtención pueden
diferir en identidad EUR y tasas futuras distintas pueden cambiar el guardado.
El servidor recalcula siempre; no confía en resultados enviados por frontend.

## 12. Ausencia de escrituras en preview

Test SQLite set_authorizer deniega INSERT/UPDATE/DELETE en todas las conexiones
del motor de prueba. Se comprueba que el control bloquea un UPDATE de prueba antes
del preview; luego se limpian los eventos registrados. Tres previews USD devuelven200,
sin eventos DML y con tabla simulations vacía; una única consulta FX falsa por caché.
Previews repetidos tampoco aumentan historial. Consultas con no_autoflush y sesiones
nuevas; rollback de lectura existente no escribe datos. Caché solo en memoria.

## 13. Contratos HTTP definitivos

| Ruta | Éxito | Salida | Errores |
| --- | --- | --- | --- |
| GET /customers | 200 | {items:[CustomerResponse],total,limit,offset} | 422/500 |
| GET /customers/{customer_id} | 200 | CustomerResponse existente | 404/422/500 |
| GET /customers/{customer_id}/simulations | 200 | {items:[HistoricalSimulationResponse],total,limit,offset} | 404/422/500 |
| POST /simulations/preview | 200 | SimulationPreviewResponse, sin id/created_at | 404/422/503/500 |

Historial incluye campos requeridos pero anulables para datos desconocidos;
cantidades/tasas como cadenas, fechas UTC/ISO. Los cuatro campos de entrada de
simulación siguen obligatorios y estrictos; EUR por defecto y forbid conservados.
Query usa conversión habitual de enteros HTTP, no strict sobre cadenas URL;
extras de query ignorados según política declarada, sin ampliar forbid a clientes.

## 14. OpenAPI y Angular

Probados rutas/response codes/problem+json, mismo $ref de petición para preview y
guardado, schemas de páginas, límites/defaults, search255, strings monetarios,
nullability histórica y ausencia de id/created_at en preview. Composición real del
bootstrap también probada, no solo dependencias sustituidas en el harness de tests.
Guía Angular en SPEC-006: buscar→seleccionar→detalle/historial→preview con debounce
y descarte/cancelación de respuestas obsoletas→guardar explícitamente→refrescar
historial. Cancelación cliente no garantiza cancelar cálculo servidor. No UI ni
cliente TypeScript generados. Mostrar NULL como desconocido, no cero.

## 15. Inventario completo acumulado

92 archivos pendientes frente a HEAD: 56 seguidos modificados y 36 nuevos; docx
no seguido aparte. Ningún eliminado. Notación de llaves representa ficheros separados.

Documentación/evidencias (33):

- README.md, backend/README.md, ai-workspace/README.md.
- docs/requirements/{functional-requirements,requirements-traceability}.md.
- docs/planning/mvp-roadmap.md.
- docs/adr/{0001-technology-stack,0002-architecture}.md (conservados TASK037).
- docs/specs/001-customer-registration/{spec,plan,tasks}.md.
- docs/specs/002-progressive-pricing/{spec,plan,tasks}.md.
- docs/specs/003-simulations/{spec,plan,tasks}.md.
- docs/specs/004-international-customers-and-simulations/{spec,plan,tasks}.md.
- docs/specs/005-taxes-and-currency-conversion/{spec,plan,tasks,sources}.md.
- docs/specs/006-customer-queries-and-preview/{spec,plan,tasks}.md (nuevos).
- ai-workspace/01-tasks/TASK035-mvp-reconciliation.md (heredado intacto).
- ai-workspace/01-tasks/TASK036-international-customers-and-simulations.md (heredado intacto).
- ai-workspace/01-tasks/TASK037-taxes-and-currency-conversion.md (heredado intacto).
- ai-workspace/01-tasks/TASK037-initial-hashes.json (heredado intacto).
- ai-workspace/01-tasks/TASK038-customer-queries-and-preview.md (nuevo).
- ai-workspace/01-tasks/TASK038-initial-hashes.json (evidencia nueva, no build).

Fuente bajo backend/src/saas_o_matic/ (39):

- application/customers/{dto,errors,queries,use_cases}.py.
- application/simulations/{calculator,dto,errors,estimator,queries,use_cases}.py.
- application/pagination.py.
- bootstrap/{customers,main,simulations}.py.
- domain/customers/{entities,ports,value_objects}.py.
- domain/pricing/{errors,services}.py.
- domain/simulations/{calculation,entities,ports}.py.
- infrastructure/customers/{mappers,models,repositories}.py.
- infrastructure/simulations/{mappers,models,repositories}.py.
- infrastructure/{database,frankfurter,tax_catalog}.py.
- presentation/customers/{dependencies,router,schemas}.py.
- presentation/simulations/{dependencies,router,schemas}.py.
- presentation/{pagination,problems}.py.

Pruebas acumuladas (18), bajo backend/tests/:

- test_architecture.py; test_customer_{api,repository,schemas,use_case}.py.
- test_generic_tax_id.py; test_increment_migrations.py; test_migrations.py; test_pricing.py.
- test_simulation_{api,repository,schemas,use_case}.py.
- test_frankfurter.py; test_monthly_calculation.py; test_tax_fx_migration.py.
- test_queries_and_preview.py; test_query_use_cases.py (nuevos TASK038).

Migraciones pendientes heredadas (2): backend/migrations/versions/
0003_international_simulations.py y 0004_add_simulation_taxes_and_fx.py, intactas.
0001/0002/env.py tampoco modificados. Sin cambios de dependencias, configuración,
LICENSE ni modelos de persistencia por TASK038. Inventario propio: 41 rutas,
12 ficheros nuevos y 29 actualizados en alcance autorizado.

## 16. Pruebas añadidas y modificadas

Nuevas: test_queries_and_preview.py (115 casos) y test_query_use_cases.py (12).
Cubren Unicode/literales/inyección/orden/páginas, detalle de seis países, tres
generaciones y aislamiento/NULL, preview/límites/países/divisas/manipulación/503,
SQL authorizer, composición real, OpenAPI y flujo completo. Consultas acotadas
probadas (2 listado, 3 historial) y registros físicos sin cambios tras lecturas.
Única adaptación de prueba previa: target del monkeypatch de pricing en
test_simulation_use_case.py apunta al servicio extraído; conserva la comprobación
de cliente antes del motor. No se eliminan pruebas ni se reduce cobertura funcional.
No se ha medido porcentaje de cobertura.

## 17. Comparación con baseline e incidencias

Antes de código: 411 passed (26.23s), Ruff correcto, 82 formateados, mypy80 correcto,
pip check correcto y 35 pines iguales a metadata/pip freeze. Primera regresión
tras extracción: las mismas411 pasan. Luego91 nuevos y finalmente538 (+127).
No fallos de pruebas de funcionalidad durante esta tarea. Incidencias de calidad:
tres anotaciones de responses para mypy, imports, líneas largas y un import json
no usado; corregidas. No se presenta el resultado de revisión propia como auditoría.

## 18. Validaciones finales

Ejecutables exclusivamente backend/.venv/Scripts/python.exe; sin instalar paquetes.

| Control | Resultado |
| --- | --- |
| python -m pytest | 538 passed |
| python -m ruff check . | Correcto |
| python -m ruff format --check . | 89 files already formatted |
| python -m mypy . | 87 source files, sin errores |
| python -m pip check | Sin incompatibilidades |
| requirements.lock | 35 pines intactos y entorno coincidente |

Controles de cierre ejecutados: 31 Markdown, cero enlaces relativos rotos y cero
espacios finales; git diff --check correcto. Las 102 huellas iniciales están
registradas y las 39 protegidas coinciden. Revisiones0001–0004/env.py intactos;
sin quinta migración, cambios de configuración/dependencias/LICENSE, bases ni
artefactos de build en el inventario. Cero coincidencias de patrones de claves
privadas/tokens (no garantía exhaustiva de ausencia de secretos). Índice vacío,
docx sin seguimiento, rama/HEAD/main correctos y sin TASK039. Lock35 también
comprobado contra pip freeze. No comprobación no ejecutada se presenta como realizada.

## 19. Ejemplos reales

Flujo ejecutado con HTTPX/ASGI contra bootstrap real, sesiones SQLite temporales
migradas y cálculo EUR real de aplicación, sin proveedor externo ni base real.
Cliente ficticio creado: École ACME, ES, 12345678Z, test@example.com, standard.
Id devuelto: 560e1a4d-49f2-4bf7-a3e5-fb53ac4d14ec; created_at
2026-11-18T14:19:43.911428Z. GET /customers?search=%C3%89COLE&limit=20&offset=0
devolvió200, items con ese cliente, total1/limit20/offset0; detalle devolvió lo mismo.

Petición real POST /simulations/preview:

```json
{"customer_id":"560e1a4d-49f2-4bf7-a3e5-fb53ac4d14ec","user_count":15,"storage_gb":250,"api_calls_per_month":100000}
```

Respuesta200 real completa:

```json
{"customer_id":"560e1a4d-49f2-4bf7-a3e5-fb53ac4d14ec","user_count":15,"storage_gb":250,"api_calls_per_month":100000,"billing_period":"monthly","user_subtotal_eur":"140.00","tax_country":"ES","tax_rate":"0.21","tax_source":"https://sede.agenciatributaria.gob.es/Sede/iva/calculo-iva-repercutido-clientes/tipos-impositivos-iva.html","tax_catalog_version":"general-vat-2026-11-17-v1","tax_verified_on":"2026-11-17","tax_territory":"Península y Baleares","tax_effective_from":null,"tax_amount_eur":"29.40","total_eur":"169.40","display_currency":"EUR","exchange_rate":"1","exchange_rate_date":null,"exchange_rate_obtained_at":"2026-11-18T14:19:43.947092Z","exchange_rate_source":"identity","converted_total":"169.40"}
```

Historial antes del guardado200: {items:[],total:0,limit:20,offset:0}.
Guardado de la misma entrada:201, id5b054ea4-6147-409a-96a8-f8ef7e974b22,
created_at2026-11-18T14:19:43.957280Z y mismo importe169.40. Obtención identidad
2026-11-18T14:19:43.957198Z: timestamp distinto, no precio distinto. GET historial
posterior200 con un elemento exactamente igual al guardado. USD/GBP/503 se
probaron offline con dobles, no se inventan tasas reales para este incremento.

## 20. Evidencia del flujo completo

| Paso | Estado | Evidencia |
| --- | --- | --- |
| Alta | 201 | Cliente anterior |
| Búsqueda | 200 | ÉCOLE encuentra École, total1 |
| Detalle | 200 | Misma representación que creación |
| Preview | 200 | 140.00 + 29.40 = 169.40, sin id/created_at |
| Historial previo | 200 | total0 |
| Guardado explícito | 201 | Id/fecha nuevos y169.40 |
| Historial posterior | 200 | total1 y snapshot preservado |

También probado automáticamente por test_complete_backend_flow y composición
real en test_production_composition_wires_new_routes. No es un E2E de Angular ni
un despliegue público; no se fabrican capturas ni conversaciones.

## 21. Criterios de aceptación

1–6 listado/búsqueda parametrizada/Unicode/paginación/orden: verificados.
7–10 detalle/404/aislamiento/historial descendente: verificados.
11–13 NULL/snapshots sin nuevas referencias/FX offline: verificados.
14–17 preview sin persistir ni DML y cálculo/paridad compartidos: verificados.
18–20 exactitud, problem+json y OpenAPI: verificados.
21–22 flujo backend y calidad: verificados. 23–25 registros, sin publicación y
docx fuera de Git: comprobados. Aceptación humana y auditoría independiente pendientes.

## 22. Cumplimiento de requisitos

| Requisitos | Backend local | E2E visual |
| --- | --- | --- |
| FR-01/02 | Alta seis países/validación conservadas | Pendiente |
| FR-03/04/05/06 | Simulación/consumos/pricing/impuestos conservados | Pendiente |
| FR-07 | Listado y buscador completados | Dashboard pendiente |
| FR-08 | Detalle e historial completados | Tarjetas responsive pendientes |
| FR-09 | Preview y guardado explícito completados | Slider/formulario pendiente |
| FR-10/11/12 | FX/snapshots/mensual conservados | Selector y presentación pendientes |

No se declara finalizado todo el MVP ni el frontend. Backend preparado para revisión,
no aprobado por su propio implementador.

## 23. Riesgos, limitaciones y deuda

LIKE/UDF puede escanear tablas; sin índices especulativos. Offset no garantiza
snapshot estable con escrituras concurrentes. Casefold no colación local, no
eliminación de acentos ni equivalencias Unicode de composición. Inmutabilidad por
API, no frente a SQL externo. Snapshot corrupto provoca error, no datos inventados.
H-01/H-03/H-04/H-05 resueltos conservados; H-02/H-08 atendidos; H-06/H-07 residuales.
Caché por proceso, proveedor sin SLA y simplificación fiscal de TASK037 sin cambios.
Sin autenticación/multitenancy/CI/despliegue. Revisión independiente futura TASK039.

## 24. Decisiones pendientes

P-01 versión Angular/Vitest y P-05 despliegue/SQLite fuera de desarrollo permanecen
pendientes; no imprescindibles aquí. El propietario decide aceptación, publicación
controlada posterior y los incrementos visuales. No se infieren funcionalidades nuevas.

## 25. Ausencia de publicación

Sin add, commit, push, PR, merge, rebase, stash, reset, clean ni force-push. Sin
modificación de main local, rama nueva ni contenido original del reto publicado.
Sin dependencias/migraciones nuevas. Índice vacío y TASK001–TASK037 intactos.
TASK039 no creado ni iniciado. Solo preparar cambios para revisión local.

## 26. Recomendación TASK039

Solicitar auditoría independiente del backend acumulado: capas, contratos/OpenAPI,
consultas Unicode/paginación, datos históricos/Decimal, preview sin DML, FX/caché,
migraciones y riesgos H-06/H-07. Proporcionar evidencias reales y diff acumulado;
no autorizar publicación por inferencia. Detenerse tras esta entrega.
