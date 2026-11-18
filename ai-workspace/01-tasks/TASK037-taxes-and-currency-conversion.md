# TASK037 — Motor de impuestos y conversión multidivisa

| Campo | Valor |
| --- | --- |
| Fecha | 2026-11-17 |
| Modalidad | Especificación e implementación local; sin publicación |
| Implementador | OpenCode, GPT-6.1 Sol; no revisión independiente |
| Fuente de autorización | Instrucción TASK037 del propietario en la conversación |
| Rama | feature/mvp-backend, sin crear otra rama |
| HEAD/origin/main | b3c5ca81d23d279b478ed466757bada031aa1e1e |

## 1. Resumen ejecutivo

Implementados IVA general de seis países, total EUR, conversión EUR/USD/GBP,
Frankfurter v2 único, caché24h/timeout5s y snapshot reproducible exacto. 411 pruebas
superadas frente a 340 iniciales. Sin nuevas dependencias, publicación ni TASK038.
El trabajo acumulado TASK035/036 y sus informes se preservó.

## 2. Git y huellas iniciales

Estado inicial comprobado: rama correcta, HEAD/origin/main esperados tras fetch,
40 seguidos modificados, 10 nuevos de tareas anteriores y documento original no
seguido; índice vacío. Main local sigue en 8371f9f608ce6e06984cc501d8240e1b7edf34d5.

Antes de editar se registraron 80 rutas con SHA-256: inventario de cambios existente,
registros históricos adicionales y documento original. Manifiesto materializado como
evidencia en [TASK037-initial-hashes.json](TASK037-initial-hashes.json); su contenido
se comparó con el manifiesto temporal inicial, sin diferencias. No contiene el reto,
solo su nombre y hash. Los documentos vigentes autorizados pueden cambiar; registros
históricos y migraciones previas no. Estado final: misma rama/HEAD/main, índice vacío,
45 seguidos modificados y 24 nuevos acumulados, además del docx no seguido.

## 3. Decisiones consolidadas

Q-05/Q-22: generales ES21/PT23/FR20/DE19/IT22/NL21 contrastados, catálogo versionado,
sin fuente fiscal externa en ejecución. Fecha efectiva no verificada: NULL.
Q-06/Q-07/Q-23: Frankfurter v2 verificado, único servicio activo, EUR/USD/GBP,
TTL24h desde obtención exitosa y timeout5s. EUR identidad sin red.
Q-08: cadenas exactas, dos decimales en dinero y precisión original de tasas.
Q-16: convertir total EUR con impuestos y persistir resultado convertido.
Q-17/SIM-P14: snapshot de país/tasa/fuente/versión/fechas e importes históricos.
P-03/P-04 actualizadas en alcance MVP; P-01/P-05 y contratos TASK038 siguen pendientes.

## 4. Fuentes oficiales

Registro detallado, URLs, consulta y limitaciones en
[sources.md](../../docs/specs/005-taxes-and-currency-conversion/sources.md).
Consultadas 2026-11-17: Comisión Europea/Your Europe (tabla revisada 13/07/2026),
AEAT, AT portuguesa art.18, Ministerio de Economía francés, UStG §12.1 alemán,
FiscoOggi/Agenzia delle Entrate y Belastingdienst/portal gubernamental neerlandés.
Incidencias: búsquedas web canceladas y rutas antiguas 404; se localizaron páginas
oficiales alternativas. No se presentan los intentos fallidos como verificación.
Frankfurter: documentación y licencia oficiales, endpoint v2 y smoke real.

## 5. Tasas y ámbito

| País | Tasa exacta | Impuesto sobre 140 EUR | Total EUR |
| --- | --- | --- | --- |
| ES | 0.21 | 29.40 | 169.40 |
| PT | 0.23 | 32.20 | 172.20 |
| FR | 0.20 | 28.00 | 168.00 |
| DE | 0.19 | 26.60 | 166.60 |
| IT | 0.22 | 30.80 | 170.80 |
| NL | 0.21 | 29.40 | 169.40 |

Estimación comercial simplificada por país: no regiones especiales, reducidos,
exenciones, inversión del sujeto pasivo ni regímenes B2B. No asesoría ni factura.
ES península/Baleares, PT continental, FR metropolitana; DE/IT/NL ámbito general
sin territorios excluidos. No se verifica región del cliente: limitación explícita.
Fechas de publicación y consulta no se usan como fechas de entrada en vigor.

## 6. Especificación y arquitectura

SPEC-005/spec, plan, tareas y fuentes creados antes del código. Dominio puro en
domain/simulations/calculation.py: reglas, catálogo validado, quote y cálculo.
Aplicación MonthlyEstimator reutilizable, puerto ExchangeRateProvider estructural.
Infraestructura implementa su firma sin importar aplicación, conservando capas.
Bootstrap compone un estimador/adaptador/cache por proceso. urllib estándar cierra
cada respuesta; no cliente HTTP persistente ni dependencia nueva. HTTPX solo dev.
Catálogo en un único módulo de infraestructura, sustituible por inyección y versionado.

## 7. Motor de impuestos

Base = subtotal del motor existente. Impuesto = base × fracción exacta, HALF_UP a
0.01. Total = base + impuesto. País obtenido del cliente registrado, nunca del cuerpo.
Catálogo cubre exactamente los seis países; no duplicados ni tasa por defecto.
Cada regla guarda fuente, consulta, territorio, versión y fecha efectiva disponible.
Consumos informativos y plan standard no cambian las fórmulas.

## 8. Frankfurter

API actual v2; v1 deprecada. Endpoint /v2/rate/EUR/USD o GBP: date/base/quote/rate.
Sin clave ni cuenta; referencias mezcladas del proveedor, no cotización continua
ni referencia oficial de un único banco. Publicación una o varias veces al día.
Uso comercial/caché documentados; servicio sin garantía, datos revisables y sujetos
a términos aplicables. No se encontró atribución general específica del feed mezclado;
se conserva source=frankfurter por trazabilidad. Sin proveedores alternativos activos.
Validación estricta de par, fecha no futura y tasa Decimal positiva finita; rechazar
JSON inválido/incompleto, duplicados, constantes no finitas y exponentes no representables.

## 9. Caché, errores y transacciones

TTL86400 monotónico desde éxito por divisa, lock por instancia para evitar consultas
duplicadas concurrentes. No guardar errores, no servir expirados, no tasas ficticias.
Fecha de referencia distinta de obtención/creación; festivo no invalida caché vigente.
No hay límite adicional de antigüedad de publicación; caché solo por proceso y se
pierde al reiniciar. Timeout urllib de socket 5s, no SLA de latencia total.
Errores externos se traducen a 503 problem+json sin filtrar detalles. EUR sin red.
Consulta de país finaliza su transacción de lectura con rollback antes de red;
el caso de uso usa sesión nueva sin escrituras pendientes. Todo cálculo precede
a INSERT; FK y rollback en infraestructura se conservan.

## 10. Contrato HTTP definitivo

Cuatro campos TASK036 siguen obligatorios y estrictos; display_currency opcional,
EUR por defecto; EUR/USD/GBP. Forbid sigue rechazando país fiscal, tasas, importes,
periodicidad arbitraria y extras. Respuesta conserva campos previos y añade:
tax_country, tax_rate, tax_source, tax_catalog_version, tax_verified_on,
tax_territory, tax_effective_from, tax_amount_eur, total_eur, display_currency,
exchange_rate, exchange_rate_date, exchange_rate_obtained_at,
exchange_rate_source y converted_total. Todas las tasas/importes son cadenas.
Fechas ISO; efectiva desconocida NULL; EUR referencia NULL/source identity/tasa1.
201/404/422/503/500, errores problem+json, sin Location ni nuevas rutas públicas.

## 11. Persistencia y migración

0004 añade calculation_snapshot TEXT nullable: JSON versionado autocontenido,
dinero/tasas en cadenas, no números JSON/REAL. El subtotal original sigue separado
del total con IVA. Codec reconstruye Decimal/fechas y valida fórmulas sin catálogo
actual ni nueva consulta externa. Nuevas simulaciones contienen snapshot completo;
antiguas quedan NULL y no se recalculan. Registros y relaciones preservados.
Downgrade bloqueado antes del DDL si existe cualquier snapshot. Ciclo reversible
con históricos NULL probado, junto con FK y conservación de filas. 0001–0003 intactas.

## 12. Exactitud monetaria

Decimal desde JSON externo (parse_float/parse_int/parse_constant), sin float monetario.
Tasa con precisión original. Contextos locales independientes y precisión suficiente;
único redondeo de negocio en impuesto y conversión a céntimos con HALF_UP.
Tiempos monotónicos usan float únicamente para temporización, no dinero/tasas.
Ejemplos fiscales, máximo técnico y fracciones de céntimo probados. Contexto del
llamador (precisión, exponentes, traps y flags) preservado. Números enormes de pricing intactos.

## 13. Deuda técnica

H-03 resuelto acotadamente: pricing usa Context independiente, no traps/exponentes
heredados; no cambia tarifas ni complejidad. H-01 sigue corregido, formateador
ampliado a aislamiento de exponentes. H-06 conserva FK/rollback y riesgo de carrera
sin traducir todo IntegrityError a 404. H-07 conserva TEXT y validación al reconstruir;
no CHECK decimal/JSON adicional: SQL directo puede saltarse validación, riesgo residual.
No se alteran informes históricos para cambiar sus veredictos previos.

## 14. Inventario completo acumulado

69 archivos de código/documentación pendientes respecto a HEAD (45 seguidos
modificados, 24 nuevos), más docx no seguido. Ningún eliminado. Notación de llaves:
cada nombre representa un fichero independiente.

Documentación (28):

- README.md, backend/README.md, ai-workspace/README.md.
- docs/requirements/{functional-requirements,requirements-traceability}.md.
- docs/planning/mvp-roadmap.md.
- docs/adr/{0001-technology-stack,0002-architecture}.md.
- docs/specs/001-customer-registration/{spec,plan,tasks}.md.
- docs/specs/002-progressive-pricing/{spec,plan,tasks}.md.
- docs/specs/003-simulations/{spec,plan,tasks}.md.
- docs/specs/004-international-customers-and-simulations/{spec,plan,tasks}.md.
- docs/specs/005-taxes-and-currency-conversion/{spec,plan,tasks,sources}.md (nuevos TASK037).
- ai-workspace/01-tasks/TASK035-mvp-reconciliation.md (heredado intacto).
- ai-workspace/01-tasks/TASK036-international-customers-and-simulations.md (heredado intacto).
- ai-workspace/01-tasks/TASK037-taxes-and-currency-conversion.md (nuevo).
- ai-workspace/01-tasks/TASK037-initial-hashes.json (evidencia nueva autorizada, no artefacto de build).

Fuente bajo backend/src/saas_o_matic/ (23):

- application/customers/use_cases.py.
- application/simulations/{dto,errors,estimator,use_cases}.py.
- bootstrap/simulations.py.
- domain/customers/{entities,ports,value_objects}.py.
- domain/pricing/{errors,services}.py.
- domain/simulations/{calculation,entities}.py.
- infrastructure/customers/{mappers,models,repositories}.py.
- infrastructure/simulations/{mappers,models}.py.
- infrastructure/{frankfurter,tax_catalog}.py.
- presentation/problems.py.
- presentation/simulations/{router,schemas}.py.

Migraciones nuevas acumuladas (2):

- backend/migrations/versions/0003_international_simulations.py (TASK036, intacta).
- backend/migrations/versions/0004_add_simulation_taxes_and_fx.py (TASK037).

Pruebas acumuladas (16), bajo backend/tests/:

- test_architecture.py.
- test_customer_{api,repository,schemas,use_case}.py.
- test_generic_tax_id.py, test_increment_migrations.py, test_migrations.py.
- test_pricing.py.
- test_simulation_{api,repository,schemas,use_case}.py.
- test_frankfurter.py, test_monthly_calculation.py, test_tax_fx_migration.py (nuevos TASK037).

42 rutas corresponden a cambios propios TASK037 frente al inventario inicial;
las otras 27 conservan íntegro su contenido previo. Sin cambios de dependencias,
configuración, LICENSE ni migraciones 0001–0003.

## 15. Pruebas añadidas/modificadas en TASK037

Nuevas: test_monthly_calculation, test_frankfurter y test_tax_fx_migration.
Modificadas: test_customer_use_case (puerto de país), test_migrations (head y columna),
test_simulation_api (cálculo completo, manipulación, 503, sesión sin transacción),
test_simulation_schemas (respuesta ampliada), test_simulation_use_case (puerto/composición).
No eliminadas pruebas previas; gigantes, validadores fiscales y contratos siguen activos.
Todos los nuevos tests externos usan dobles/relojes/transportes falsos, nunca Internet.

## 16. Baseline, comparación e incidencias

Antes de código: 340 passed (17.66 s), Ruff correcto, 74 ficheros formateados,
mypy 72 ficheros y pip check correctos. Verificación explícita de los 35 pines
realizada durante implementación y cierre, sin instalaciones ni cambios al lock.
Primera regresión: 337 passed/3 failed por una expectativa incorrecta introducida
al extender head en test de downgrade: 0004 se revierte válidamente con snapshot NULL
antes de que 0003 bloquee. Se restauró expectativa 0003, sin cambiar migraciones previas.
También se corrigieron reexport explícito para mypy, tipo de cabecera HTTPError,
imports y líneas largas. Después: 401, 409 y finalmente 411 pruebas superadas.
Diferencia final +71 sobre 340; sin objetivo ficticio ni porcentaje de cobertura inventado.

## 17. Validaciones

Exclusivamente backend/.venv, sin instalar paquetes:

| Control | Resultado |
| --- | --- |
| python -m pytest | 411 passed |
| python -m ruff check . | Correcto |
| python -m ruff format --check . | 82 files already formatted |
| python -m mypy . | 80 source files, sin errores |
| python -m pip check | No broken requirements found |
| requirements.lock | 35 pines intactos y entorno coincidente |

Controles de cierre: 27 Markdown, cero enlaces relativos rotos y cero espacios finales;
`git diff --check` correcto. Verificadas 33 huellas protegidas (31 registros históricos,
docx y migración0003); 0001/0002, configuración, dependencias y LICENSE sin diff.
Manifiesto de 80 huellas idéntico al inicial. Sin artefactos de build/bases en cambios
ni coincidencias de patrones de claves privadas/tokens (no es garantía exhaustiva de
ausencia de secretos). Índice vacío; rama/HEAD/main correctos; sin TASK038.
La revisión propia no sustituye la auditoría independiente TASK039 ni aceptación humana.

## 18. Ejemplos reales y smoke separado

Smoke urllib real: USD 1.1014 y GBP 0.8339, referencia 2026-11-17, obtenciones
2026-11-17T17:30:05.860886+00:00 y 17:30:06.138990+00:00 respectivamente.
Después se ejecutó HTTPX/ASGI sobre SQLite temporal, usando el adaptador real;
no servidor desplegado ni datos de clientes reales. Cliente ES ficticio id
405829ad-6cbf-4747-84ec-b3e37945901a. Petición real:

```json
{"customer_id":"405829ad-6cbf-4747-84ec-b3e37945901a","user_count":15,"storage_gb":250,"api_calls_per_month":100000,"display_currency":"USD"}
```

Respuesta real 201:

```json
{"id":"19857a51-f98a-479b-b762-375a2781b52c","customer_id":"405829ad-6cbf-4747-84ec-b3e37945901a","user_count":15,"storage_gb":250,"api_calls_per_month":100000,"billing_period":"monthly","user_subtotal_eur":"140.00","tax_country":"ES","tax_rate":"0.21","tax_source":"https://sede.agenciatributaria.gob.es/Sede/iva/calculo-iva-repercutido-clientes/tipos-impositivos-iva.html","tax_catalog_version":"general-vat-2026-11-17-v1","tax_verified_on":"2026-11-17","tax_territory":"Península y Baleares","tax_effective_from":null,"tax_amount_eur":"29.40","total_eur":"169.40","display_currency":"USD","exchange_rate":"1.1014","exchange_rate_date":"2026-11-17","exchange_rate_obtained_at":"2026-11-17T17:36:13.393761Z","exchange_rate_source":"frankfurter","converted_total":"186.58","created_at":"2026-11-17T17:36:13.393899Z"}
```

EUR: 201, id b066b257-ab76-4d45-854e-56bb32a1f368, total/convertido 169.40,
tasa1, identity y referencia NULL. GBP: 201, id 56027825-7b3a-4b47-a421-2df52491c367,
tasa0.8339, convertido141.26, referencia2026-11-17. No tasas ficticias presentadas como reales.
503 y manipulación se probaron determinísticamente con transporte falso, sin provocar
fallos deliberados ni carga adicional sobre el servicio público.

## 19. Criterios de aceptación

1–6: fuentes y seis generales, país del cliente, pricing y consumos sin cargos, total
mensual verificados. 7–11: tres divisas, EUR offline, proveedor único, caché/timeout
y errores externos probados. 12–14: Decimal, HALF_UP y reconstrucción histórica
probados. 15–16: migración poblada y NULL históricos sin backfill. 17–18: problem+json
y suite offline. 19: calidad técnica correcta. 20–21: huellas históricas y sin publicación.
Aceptación final humana y auditoría independiente pendientes.

## 20. Requisitos funcionales

FR-03/06/10/11 backend local completados en alcance aprobado; FR-01/02/04/05/12
conservados. FR-07/08/09 siguen pendientes de consultas/historial/preview y UI.
Todo E2E que exige frontend continúa pendiente. No se declara terminado el MVP.

## 21. Riesgos y decisiones pendientes

Simplificación fiscal por país, sin datos territoriales/B2B, fechas efectivas NULL y
catálogo con mantenimiento manual verificado. Proveedor sin SLA, referencias
revisables, caché independiente por proceso y sin persistencia operativa. No stale
fallback; caída sin caché válida implica503 (no EUR). JSON TEXT permite SQL directo
inválido fuera de aplicación; H-06/H-07 residuales. DDL SQLite no transaccional:
backup previo a migrar bases reales; solo se tocaron temporales en esta tarea.
Snapshot no tiene índices fiscales porque no hay consultas públicas en este alcance.
P-01/P-05 y contratos TASK038 siguen pendientes. Sin frontend/CI/despliegue.

## 22. Ausencia de publicación

Sin add, commit, push, PR, merge, rebase, stash, reset, clean ni force-push.
Main local intacto; no rama nueva; índice vacío. Documento original no seguido,
solo su huella registrada, sin publicar contenido. No creado TASK038 ni iniciadas
sus funcionalidades. Registros TASK001–TASK036 preservados.

## 23. Recomendación TASK038

Revisar este incremento y aprobar contratos de lectura, búsqueda, detalle e historial
inmutable y previsualización sin persistencia. Reutilizar MonthlyEstimator y el snapshot,
con DTOs de lectura que representen correctamente históricos NULL, sin recalcularlos.
No iniciar TASK038 hasta autorización específica. Detenerse tras esta entrega.
