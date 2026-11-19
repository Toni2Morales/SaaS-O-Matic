# Integración continua

## Workflows

| Workflow    | Archivo                             | Trigger                                                            | Jobs                                                                                                                         |
| ----------- | ----------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| Quality     | `.github/workflows/quality.yml`     | PR a `main`; push a `main`/`docs/final-delivery`; ejecución manual | Backend estático/Pytest; frontend typecheck/lint/formato/Vitest-cobertura/build/audits; Playwright Chromium/Firefox/WebKit   |
| Quick Start | `.github/workflows/quick-start.yml` | mismos triggers                                                    | Ubuntu y Windows: ejecutar scripts, alta sintética, preview sin persistencia, guardar, parar/reiniciar y comprobar historial |

Ambos son CI sin deployment. Usan `permissions: contents: read`, runners efímeros,
`timeout-minutes`, concurrencia cancelable, actions de GitHub verificadas y referenciadas por
SHA completa. No usan `pull_request_target`, secretos, permisos de repositorio ni
`continue-on-error`. El código de PR se ejecuta en runner aislado; no se publica artefacto.

Backend instala `.[dev]` dentro del entorno Python del runner con `requirements.lock` como
constraints; las pruebas usan `DATABASE_URL` aislada y fixtures de proveedor. Frontend
ejecuta `npm ci --ignore-scripts`. El job Playwright instala browsers oficiales y
dependencias de sistema dentro del runner GitHub efímero mediante
`npx playwright install --with-deps chromium firefox webkit`. La suite no requiere la API
real de Frankfurter; escenarios de proveedor externo real no forman parte de CI obligatoria.

Quick Start usa versiones de runtime compatibles y base nueva del runner. El escenario
HTTP prueba alta con datos sintéticos, 15 usuarios EUR, preview sin DML, save/historial,
parada segura, segunda ejecución y conservación del snapshot. No cambia código de tests ni
configuración global del repositorio.

El job Playwright además inicia, en puerto libre de runner, una app FastAPI temporal con
Alembic y el fixture FX determinista inyectado mediante los dependency overrides ya usados
por la integración de producto. La prueba real de UI se ejecuta una vez en Chromium; después
reinicia únicamente el backend propio sobre la misma SQLite y verifica la lectura del
historial. Las tasas del fixture están etiquetadas en el job como test data. La suite normal
multibrowser sigue usando los route fixtures existentes; los casos opt-in continúan siendo
skips y no se cuentan como PASS.

## Evidencia y badges

El workflow está versionado en `docs/final-delivery`, pero resultados deben consultarse en
los runs vinculados a [Actions](https://github.com/Toni2Morales/SaaS-O-Matic/actions).
No considerar CI validada hasta que los jobs aparezcan y terminen. Al documentar una
ejecución, registrar run ID/URL, evento, SHA, jobs, duración observada y logs relevantes.
Un fallo por workflow se puede corregir en esa configuración; un fallo de código/tests
existentes se reporta y detiene la corrección automática.

Los badges del README solo se añadirán después de runs reales y señalarán expresamente la
rama `docs/final-delivery` mientras no se integren en `main`. No se infiere status a partir
del workflow YAML ni se publica una cifra histórica como cobertura dinámica.

## Límites de seguridad

Los workflows verifican calidad básica, no constituyen auditoría integral de seguridad,
SAST/DAST, branch protection, autorización ni preparación para producción. Auditorías npm
dependen de registry/advisories en la fecha del run. Las dependencias Python usan constraints
sin hashes y build isolation no queda plenamente bloqueada.
