# Integración continua

## Workflows

| Workflow    | Archivo                             | Trigger actual | Jobs                                                                                                                         |
| ----------- | ----------------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Quality     | `.github/workflows/quality.yml`     | Solo manual (`workflow_dispatch`) | Backend estático/Pytest; frontend typecheck/lint/formato/Vitest-cobertura/build/audits; Playwright Chromium/Firefox/WebKit   |
| Quick Start | `.github/workflows/quick-start.yml` | Solo manual (`workflow_dispatch`) | Ubuntu y Windows: ejecutar scripts, alta sintética, preview sin persistencia, guardar, parar/reiniciar y comprobar historial |

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

## Validación local y resultados históricos

La campaña de aceptación para esta entrega es local y reproducible en Windows 10, desde un
clon limpio de `docs/final-delivery`; el informe TASK047F registra SHA, tiempos y comandos.
GitHub Actions permanece disponible solo como infraestructura futura y no se despachará en
TASK047F. No hay badges en el README.

Los resultados de estos runs son históricos y corresponden a push/SHA anteriores. No
representan el estado actual del trigger ni se deben mostrar como una validación aprobada:

| Hallazgo | Evidencia histórica | Estado en TASK047F |
|---|---|---|
| A47-01 | [Quality #44556931530](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44556931530), SHA `181afaf…`: seis fallos responsive (dos aserciones × Chromium/Firefox/WebKit), 320 px contra documento 334 px. | Pendiente y aplazado por decisión del propietario. No se reprodujo en Windows local. El wrap de `.field-heading` publicado en `54bd817` no resolvió el fallo: [Quality #44566635410](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44566635410) volvió a fallar las mismas seis pruebas y midió 334 px. |
| A47-02 | [Quick Start #44556931645](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44556931645), SHA `181afaf…`: Angular no superó health check en Windows runner. El arranque había funcionado en Windows local. | Pendiente y aplazado. No se investigará/corregirá en TASK047F. |
| A47-03 | [Quick Start #44556931645](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44556931645), SHA `181afaf…`: Bash no validó la propiedad del PID en parada/reinicio Linux. | Pendiente y aplazado. No se investigará/corregirá en TASK047F. |

Runs posteriores sobre `54bd817…`: [Quality #44566635410](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44566635410) terminó failure (backend/frontend PASS, Playwright 73 PASS, 20 skips, 6 FAIL); [Quick Start #44566635425](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44566635425) terminó failure (health Angular Windows y comprobación PID Linux). Son evidencias del aplazamiento, no un ciclo de corrección.

Los hallazgos A47-01/02/03 no se consideran resueltos. La decisión expresa del propietario
es priorizar la ejecución local Windows 10. Estos resultados CI no constituyen por sí solos
un incumplimiento del reto original; tampoco equivalen a certificación multiplataforma.
No se alteran los jobs, comandos, aserciones ni matrices que los workflows ejecutan.

## Límites de seguridad

Los workflows verifican calidad básica, no constituyen auditoría integral de seguridad,
SAST/DAST, branch protection, autorización ni preparación para producción. Auditorías npm
dependen de registry/advisories en la fecha del run. Las dependencias Python usan constraints
sin hashes y build isolation no queda plenamente bloqueada.
