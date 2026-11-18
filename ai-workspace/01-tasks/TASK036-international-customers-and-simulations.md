# TASK036 — Internacionalización de clientes y ampliación de simulaciones

| Campo | Valor |
| --- | --- |
| Fecha | 2026-11-17 |
| Modalidad | Especificación e implementación local, sin publicación |
| Implementador | OpenCode, modelo GPT-6.1 Sol; no es auditoría independiente |
| Fuente | Instrucción TASK036 del propietario en esta conversación (recibida dos veces, mismo alcance) |
| Rama | `feature/mvp-backend` |
| HEAD | `b3c5ca81d23d279b478ed466757bada031aa1e1e` |

## 1. Resumen e instrucciones

Implementados seis países, cero usuarios, mensual, GB y llamadas mensuales estrictos,
rechazo de extras de simulación y calidad H-01/H-02/H-04/H-05/H-08. H-06/H-07
se conservan justificados; H-03 histórico sin cambios. Sin impuestos, FX, consultas,
preview, Angular, nuevas dependencias ni publicación. Autorizados análisis, rama,
documentación, implementación, migración y pruebas; no staging/commit/push/PR/merge.
La aprobación humana final y la revisión independiente siguen pendientes.

## 2. Git, preservación y hashes

Inicial: `docs/mvp-reconciliation`, HEAD esperado, 12 documentos modificados,
3 documentos nuevos TASK035 y docx no seguido; sin staged. Ejecutado fetch;
origin/main coincide con PR #5. Main local permanece en
`8371f9f608ce6e06984cc501d8240e1b7edf34d5`.

Registrados SHA-256 antes de `git switch -c feature/mvp-backend`; los 15 se
compararon inmediatamente después y coincidieron íntegramente. No stash ni reset.
Después se actualizaron solo documentos vigentes autorizados; el informe TASK035
no se modificó. Manifiesto original:

| Documento | SHA-256 inicial y tras cambio de rama |
| --- | --- |
| `README.md` | `5E5F123AA9002E64B9B4CA56F1782EBE774BB8A0DB981D88FCECAD43673757B3` |
| `ai-workspace/README.md` | `5064CF865BCE7CA72E19FD45EEC6205BE6301D31D1CBD16262DB090C095580A5` |
| `ai-workspace/01-tasks/TASK035-mvp-reconciliation.md` | `C7EE424D43F50C2C612078EFCDAFC1B2A4D345C8EC500C8FD8E9D0484E0BEFC8` |
| `docs/planning/mvp-roadmap.md` | `DC905FFE9F812C7235A2BCD3480F6A18C1129F2FE1DD5F08C5839663F8340E35` |
| `docs/requirements/functional-requirements.md` | `04E4C4993F423BA81AE5D30DFF0C030200B7BB89C30D375C2E7C210EB1EF7545` |
| `docs/requirements/requirements-traceability.md` | `E1D9DE088D71E859D110164203F2887F3054D0BA38C52A053D53E6E591B19ECF` |
| `docs/specs/001-customer-registration/plan.md` | `45E8F8429409BAF3AACF9422662972C999250D28C26F2173333647C14FF64DFB` |
| `docs/specs/001-customer-registration/spec.md` | `972C9D7E4B9F40DED3002C4E3048E57F50A30A7E18F448EB25E014883BDD3FE2` |
| `docs/specs/001-customer-registration/tasks.md` | `81E2600441DED63EACF04BF526AA0DB6BF089AADCF9C1FCFF6CD102A4485D3D5` |
| `docs/specs/002-progressive-pricing/plan.md` | `D9F00F51DFF4549D915B647A97D7200881A7E3518D82939F3117CBFA654EA4B8` |
| `docs/specs/002-progressive-pricing/spec.md` | `5D02A67AF83EE40D943A02AF6D25808BE780031C6E86ED04B32F24A20E8820C4` |
| `docs/specs/002-progressive-pricing/tasks.md` | `D766ACA55885AA29195D5CB836B2F1690107A2D8F649C94148CFBB0CBEC2D1E6` |
| `docs/specs/003-simulations/plan.md` | `F0B1DE1EDD3550E4F2260E15B86E3713898A1DC0B1BDAB46FEFBF94A5CF184D5` |
| `docs/specs/003-simulations/spec.md` | `461F4AB5B9E8F6E20259461B6BC7445A666B0869CD1BFAB4736DF7B7B3BDBC71` |
| `docs/specs/003-simulations/tasks.md` | `CDC3717FA11D8A00D915446170EE9BE25A47C99CAA6E5D02F994945A3B206499` |

## 3. Decisiones consolidadas

Q-18–Q-21/Q-26 implementadas según instrucción; Q-19 sustituye mínimo 1 de
Q-02/PP-Q-01 y actualiza Q-12/SIM-P09 (slider futuro desde 0). Q-22 solo aprueba
impuestos futuros oficiales, no tabla/redondeo/vigencia. Q-23 solo proveedor único
preferente Frankfurter condicionado y EUR/USD/GBP, sin caché ni precisión aprobadas.
Q-24/Q-25 aprueban alcance futuro y separación preview/guardado, no contratos
detallados. P-01 = versión Angular/Vitest; P-05 = despliegue y SQLite fuera de
desarrollo (ADR 0001); ambas pendientes, no bloquean TASK036.

## 4. Especificación, arquitectura y secuencia real

[SPEC-004](../../docs/specs/004-international-customers-and-simulations/spec.md),
plan y tareas creados antes del código, junto con consolidación inicial de requisitos.
La matriz de trazabilidad y la documentación vigente se completaron durante el cierre.
Monolito modular intacto: presentación → aplicación → dominio; infraestructura
implementa puertos; bootstrap ensambla. Dominio sin frameworks; sin nuevas dependencias.
No se duplica pricing ni se introduce estado global, servicios fiscales o HTTP externo.

## 5. Internacionalización

CountryCode: ES/PT/FR/DE/IT/NL. SpanishTaxId intacto. GenericTaxId para el resto:
rechaza Cc/Cf/Cs antes de normalizar, colapsa espacios, mayúsculas, longitud final
1..64; conserva puntuación y caracteres significativos. No comprobación oficial.
Se consideró la propuesta anterior alfanumérica 4..20; se descartó porque eliminaba
caracteres potencialmente significativos y era más restrictiva que la instrucción.
TaxId es unión de ambos objetos; selector por país en aplicación y mapeador.
Unicidad compuesta ya existía: conservada en puerto, consulta y SQLite; mismo 409.
Tax_id String(64), sin cambiar validación ES de nueve caracteres. Clientes siguen
ignorando extras; Q-26 no se extendió unilateralmente.

## 6. Pricing

Cambio mínimo: admitir cero y devolver exactamente Decimal("0.00"). Tarifas y
tabla de unidades desde 1 intactas. Sin float, plan, impuestos ni cargos nuevos.
Dominio sin máximo; cálculo por tres bandas, no por usuario; casos >4300 dígitos conservados.

| Usuarios | EUR |
| ---: | ---: |
| 0 | 0.00 |
| 1 | 10.00 |
| 10 | 100.00 |
| 11 | 108.00 |
| 15 | 140.00 |
| 50 | 420.00 |
| 51 | 425.00 |
| 100 | 670.00 |
| 1000000 | 5000170.00 |

## 7. Contrato HTTP

Petición POST /simulations: customer_id UUID, user_count 0..1.000.000,
storage_gb 0..1.000.000 y api_calls_per_month 0..1.000.000.000 obligatorios.
Enteros estrictos, forbid extras incluyendo billing_period. Servidor fija monthly.
Respuesta añade consumos y periodo, mantiene cadena monetaria y UTC/Z. 201/404/422/500
y problem+json intactos; sin Location. Ruptura explícita: antiguos cuerpos sin
consumos dejan de aceptarse. No añadir importes fiscales ni de divisas inexistentes.

## 8. Migración y conservación

0003_international_simulations, sin modificar 0001/0002. Batch SQLite amplía tax_id,
rango de usuarios y columnas. Tipos/rangos CHECK para usuarios/consumos; monthly
obligatorio con default de servidor y CHECK. NULL permitido solo como representación
histórica en persistencia; aplicación nueva exige consumos. Ningún valor inventado.
Preflight/postflight foreign_key_check. Las pruebas comparan valores completos
de filas antiguas, importe TEXT y fecha preservados; FK aplicada en conexiones app.

Downgrade bloqueado antes del DDL para no ES/tax_id largo, usuarios cero o consumos
conocidos (incluso cero); no borrar ni transformar para revertir. Ciclo reversible
probado con datos históricos compatibles. Alembic declara DDL SQLite no transaccional:
usar copia de seguridad antes de operar datos reales; no se tocó ninguna base real.

## 9. Hallazgos

| Hallazgo | Resultado |
| --- | --- |
| H-01 | Corregido: traps locales aislados, precisión suficiente, invalidación explícita sin redondeo silencioso; contexto externo intacto. |
| H-02 | SQL físico TEXT, nueva sesión, Decimal y UTC, 15 y regresión sencilla de cuatro fronteras. |
| H-03 | Histórico de pricing sin cambios. |
| H-04 | Validar antes de consultar; cliente antes del motor; prueba con motor que fallaría si se ejecutase. |
| H-05 | Forbid y 422 problem+json probados. |
| H-06 | Residual justificado: mantener FK y rollback. No hay borrado público; no clasificar cualquier IntegrityError como cliente ausente. Prueba de huérfano rechaza y no deja filas. |
| H-07 | Sin CHECK monetario adicional: una expresión GLOB parcial sería insuficiente para todos los formatos, y convertir a REAL perdería exactitud. Mantener TEXT y validación canónica en mapeador/aplicación; SQL directo puede saltarla, riesgo documentado. |
| H-08 | Requisitos, matriz, roadmap, specs y README vigentes actualizados; registros históricos intactos. |

## 10. Inventario completo

Estado respecto a HEAD: 40 ficheros seguidos modificados y 10 Markdown/Python nuevos,
incluidos los tres documentos heredados de TASK035; docx no seguido aparte. Ningún eliminado.

Documentación actualizada (los tres nombres de cada conjunto son ficheros separados):

- `README.md`, `backend/README.md`, `ai-workspace/README.md`.
- `docs/requirements/functional-requirements.md`.
- `docs/requirements/requirements-traceability.md` (nuevo desde TASK035).
- `docs/planning/mvp-roadmap.md` (nuevo desde TASK035).
- `docs/specs/001-customer-registration/{spec,plan,tasks}.md`.
- `docs/specs/002-progressive-pricing/{spec,plan,tasks}.md`.
- `docs/specs/003-simulations/{spec,plan,tasks}.md`.
- Nuevos: `docs/specs/004-international-customers-and-simulations/{spec,plan,tasks}.md`.
- Nuevo: `ai-workspace/01-tasks/TASK036-international-customers-and-simulations.md`.
- Heredado sin modificar: `ai-workspace/01-tasks/TASK035-mvp-reconciliation.md`.

Código modificado bajo `backend/src/saas_o_matic/`:

- `application/customers/use_cases.py`.
- `application/simulations/dto.py`, `application/simulations/use_cases.py`.
- `domain/customers/entities.py`, `domain/customers/ports.py`, `domain/customers/value_objects.py`.
- `domain/pricing/errors.py`, `domain/pricing/services.py`.
- `domain/simulations/entities.py`.
- `infrastructure/customers/mappers.py`, `infrastructure/customers/models.py`, `infrastructure/customers/repositories.py`.
- `infrastructure/simulations/mappers.py`, `infrastructure/simulations/models.py`.
- `presentation/simulations/router.py`, `presentation/simulations/schemas.py`.

Nuevo: `backend/migrations/versions/0003_international_simulations.py`.
Sin cambios en dependencias, configuración, LICENSE, bootstrap ni migraciones previas.

## 11. Inventario de pruebas

Modificados en `backend/tests/`:

- `test_architecture.py`: cuatro fronteras.
- `test_customer_api.py`: seis países, genérico, unicidad y extras compatibles.
- `test_customer_repository.py`: sesión nueva, mapeo internacional, unicidad final SQLite.
- `test_customer_schemas.py`: país no soportado actualizado de FR a US.
- `test_customer_use_case.py`: doble acepta TaxId, unicidad por país y país no soportado.
- `test_migrations.py`: revisión head y columnas nuevas.
- `test_pricing.py`: nueve ejemplos, cero exacto; enormes y algoritmos existentes preservados.
- `test_simulation_api.py`: consumos/periodo, cero/15, límites, obligatorios, extras, sin parciales.
- `test_simulation_repository.py`: SQL físico, Decimal/UTC desde sesión nueva; negativo sustituye antiguo cero inválido.
- `test_simulation_schemas.py`: nuevo contrato, min0, forbid en lugar de ignore.
- `test_simulation_use_case.py`: consumos defensivos, cliente antes de cálculo, traps/flags/contexto y cero/15.

Nuevos: `test_generic_tax_id.py` y `test_increment_migrations.py`.
No se eliminaron ficheros ni funcionalidades de prueba; se adaptaron expectativas
incompatibles solo por las decisiones aprobadas. No se midió porcentaje de cobertura.

## 12. Baseline y comparación

Antes de código: 240 passed (7.10 s), Ruff correcto, 71 ficheros formateados,
mypy 69 ficheros sin errores, pip check correcto y 35 pines coincidentes.
Primera regresión: 333 passed; mypy correcto. Ruff detectó 11 incidencias de imports
y líneas largas en cambios nuevos; corregidas con ordenación de imports y formato.
Cierre: 340 passed, +100 netas; no fallos, omisiones ni cantidad objetivo inventada.

## 13. Validaciones

Ejecutadas exclusivamente con backend/.venv, sin instalar nada:

| Comando/control | Resultado |
| --- | --- |
| python -m pytest | 340 passed |
| python -m ruff check . | All checks passed |
| python -m ruff format --check . | 74 files already formatted |
| python -m mypy . | 72 source files, sin errores |
| python -m pip check | No broken requirements found |
| requirements.lock | 35 pines iguales a metadata y pip freeze --exclude-editable; lock intacto |

Controles documentales y Git: 20 Markdown revisados, cero enlaces relativos rotos,
cero espacios finales; sin coincidencias en patrones de claves privadas/tokens,
sin bases ni artefactos generados en el inventario de cambios. Es una comprobación
de patrones, no garantía exhaustiva de ausencia de secretos. `git diff --check`
correcto. Índice vacío, migraciones previas/configuración/lock/LICENSE intactos.
Registros históricos seguidos sin cambios y SHA-256 de TASK035 idéntico al inicial.
No hay archivo TASK037. Documento original no seguido.

## 14. Ejemplos reales

Ejecutados con HTTPX/ASGI sobre SQLite temporal migrada; no servidor desplegado ni
base real. UUID y fechas siguientes proceden de esa ejecución, no del ejemplo de la tarea.

POST /customers: `{"legal_name":"Client International","tax_id":" ab-12 /  34 ","email":"client@example.com","country":"FR","plan":"standard"}`.
201 con id `ef9679f2-6cfd-4cad-b193-c49847b93790`, tax_id `AB-12 / 34`, país FR,
plan standard y created_at `2026-11-17T16:57:03.079692Z`.

POST /simulations:

```json
{"customer_id":"ef9679f2-6cfd-4cad-b193-c49847b93790","user_count":15,"storage_gb":250,"api_calls_per_month":100000}
```

Respuesta 201:

```json
{"id":"0c496af4-8fbf-43e1-837e-80392c6c3339","customer_id":"ef9679f2-6cfd-4cad-b193-c49847b93790","user_count":15,"storage_gb":250,"api_calls_per_month":100000,"billing_period":"monthly","user_subtotal_eur":"140.00","created_at":"2026-11-17T16:57:03.110538Z"}
```

La petición equivalente con cero produjo 201, subtotal `0.00`, id
`6e8eaab1-29c3-4066-b0d7-1b4526d7edb0` y fecha `2026-11-17T16:57:03.096563Z`.
Añadir `billing_period="yearly"` produjo 422, content-type application/problem+json,
error `body.billing_period`, `Extra inputs are not permitted`.

## 15. Criterios de aceptación

1–4 seis países/ES/genérico/unicidad: probados. 5–6 cero/tarifas: nueve ejemplos
y enormes. 7–10 consumos sin cargos, mensual y forbid: probados HTTP/aplicación.
11–13 migración, NULL históricos y exactitud: probados SQL y sesión nueva.
14 hallazgos: corregidos o justificados sección 9. 15 validaciones: sección 13.
16 TASK035: hashes conservados al cambiar rama, actualizaciones vigentes autorizadas;
registro intacto. 17 docx sigue sin seguimiento. 18 sin staging ni publicación.

## 16. Requisitos funcionales

FR-01/02/04/05/12 backend completados en alcance local; todos E2E pendientes por UI.
FR-03 parcial por cálculo futuro ampliado; FR-11 parcial (solo EUR/subtotal).
FR-06/10 pendientes TASK037, FR-07/08/09 pendientes TASK038 y frontend.
No se declara completo el MVP. Matriz y requisitos contienen el delta vigente.

## 17. Decisiones pendientes

Impuestos: tabla, tasas oficiales concretas, vigencia, base, redondeo y snapshot.
FX: verificar Frankfurter vigente, caché/caducidad/precisión/errores y persistencia.
Consultas/preview: contratos detallados. P-01 y P-05 siguen sin aprobar.
No se han adoptado automáticamente las recomendaciones de TASK035.

## 18. Riesgos y limitaciones

H-06/H-07 residuales documentados, SQLite DDL no transaccional, validación genérica
no oficial, ruptura HTTP deliberada y downgrade protegido. Sin autenticación,
frontend, CI ni despliegue. No auditoría independiente del trabajo propio.
No instalación nueva, base real modificada ni proveedor externo consultado.

## 19. Estado final y ausencia de publicación

Rama feature/mvp-backend; HEAD/origin/main iguales al merge PR #5. Main local
intacto, índice vacío. 40 seguidos modificados y 10 nuevos (incluidos 3 TASK035),
más docx no seguido. Registros TASK001–TASK035 preservados.
Sin add, commit, push, PR, merge, rebase, stash, reset ni clean. Documento original
no publicado. No creado TASK037.

## 20. Recomendación TASK037

Revisar TASK036 y concretar primero impuestos oficiales y única integración FX
Frankfurter condicionada. Solo después autorizar SPEC/implementación de impuestos
y divisas. TASK038 lectura/historial/preview; TASK039 auditoría backend; TASK040
publicación controlada; TASK041–TASK047 provisionales. Detenerse tras esta entrega.
