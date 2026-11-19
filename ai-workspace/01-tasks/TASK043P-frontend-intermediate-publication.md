# TASK043P — Preparación de publicación intermedia del frontend

| Campo                  | Valor                                                                                         |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| Fecha                  | 2026-11-18                                                                                    |
| Reanudación autorizada | 2026-11-19                                                                                    |
| Estado                 | Documentación subsanada; 90 rutas staged selectivamente y revisadas; commit y push pendientes |
| Rama                   | `feature/mvp-frontend`                                                                        |
| Base / HEAD inicial    | `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`                                                    |
| `origin/main` inicial  | `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`                                                    |
| `main` local inicial   | `8371f9f608ce6e06984cc501d8240e1b7edf34d5`                                                    |
| Autorización           | Instrucción TASK043P del propietario; commit único y push de la rama autorizados              |
| Alcance                | Respaldo local/publicado del trabajo acumulado TASK041–TASK043; sin PR ni merge               |

## 1. Objetivo y límites

Preparar la publicación intermedia del frontend Angular en la rama de trabajo,
preservando el historial y la separación respecto a `main`. La autorización permite
revisar, validar, hacer staging selectivo, crear un commit y publicar esa rama. No
autoriza Pull Request, merge, cambios funcionales, aprobación de scripts de instalación
ni TASK044.

Este documento registra preparación, interrupción y reanudación. No anticipa hashes ni
resultados del commit o push, que todavía no se han ejecutado.

## 2. Estado inicial comprobado

- `git fetch origin` se ejecutó; `HEAD` y `origin/main` coinciden con el hash base
  esperado `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`.
- Rama: `feature/mvp-frontend`; `main` local: `8371f9f608ce6e06984cc501d8240e1b7edf34d5`.
- `origin/feature/mvp-frontend` no existe todavía; `origin/main` sí existe y no diverge.
- Índice inicialmente vacío. Candidatos previos: 89 (9 rutas modificadas frente a la
  base y 80 sin seguimiento aptas para publicar). El DOCX no se cuenta y permanece sin
  seguimiento.
- Identidad Git: nombre configurado `Antonio Morales`; el correo configurado coincide
  con el formato público GitHub noreply. No se reproduce la dirección en este documento.
- El remoto `origin` apunta a `https://github.com/Toni2Morales/SaaS-O-Matic.git`.

## 3. Inventario y correspondencia

El manifiesto [TASK043-initial-hashes.json](TASK043-initial-hashes.json) enumera los 81
candidatos acumulados al inicio de TASK043, de los cuales 19 cambiaron desde esa
captura. TASK043 añadió ocho rutas, enumeradas aquí; junto con los 81 iniciales
constituyen 89 candidatos previos a este registro:

1. `ai-workspace/01-tasks/TASK043-initial-hashes.json`
2. `ai-workspace/01-tasks/TASK043-interactive-subscription-simulator.md`
3. `docs/specs/009-interactive-subscription-simulator/plan.md`
4. `docs/specs/009-interactive-subscription-simulator/spec.md`
5. `docs/specs/009-interactive-subscription-simulator/tasks.md`
6. `frontend/e2e/simulator.spec.ts`
7. `frontend/e2e/visual-evidence.spec.ts`
8. `frontend/src/app/features/simulations/data-access/simulations-api.service.ts`

Este documento es la única ruta nueva de TASK043P. Inventario autorizado resultante:
**90 rutas** = 89 anteriores + este informe. Se conservan todos los cambios acumulados
de TASK041/TASK042. Los informes históricos `TASK001`–`TASK042` no se modificaron.

Las nueve rutas versionadas modificadas frente a `main` son `.gitignore`, `README.md`,
`ai-workspace/00-project-context/architectural-evolution.md`, `ai-workspace/README.md`,
`backend/README.md`, `docs/adr/0001-technology-stack.md`,
`docs/planning/mvp-roadmap.md`, `docs/requirements/functional-requirements.md` y
`docs/requirements/requirements-traceability.md`. Las restantes rutas publicables son
los archivos de tareas, especificaciones y frontend listados en los manifiestos y en
el inventario Git inspeccionado.

El `git status` también presenta `Prueba Devs con IA.docx` como archivo sin seguimiento.
Su hash SHA-256 coincide con el capturado; no se abrió, modificó ni se incluirá en
staging. `TASKS.zip` está excluido mediante `.git/info/exclude`. `.env`, `.venv`,
`node_modules`, `dist`, cachés, resultados Playwright y bases de datos están cubiertos
por los archivos de exclusión y no aparecen como candidatos.

## 3.1 Interrupción y subsanación documental autorizada

La revisión del 2026-11-18 se detuvo antes del commit al detectar estados actuales obsoletos:
`README.md` aún describía el simulador como pendiente en secciones posteriores al
resumen TASK043; requisitos y matriz conservaban FR-09–FR-12 como pendientes/parciales;
la roadmap mantenía el estado TASK043 como pendiente. El propietario autorizó corregir
exclusivamente los cuatro documentos vigentes de la lista complementaria y este informe.

Cambios efectuados, sin alterar alcance funcional ni decisiones históricas:

- `README.md`: estado y stack frontend, tabla funcional, API/UI, puesta en marcha, nota
  de `npm ci` pendiente, resultados TASK043 y enlaces SPEC-009/TASK043/TASK043P.
- `docs/requirements/functional-requirements.md`: FR-09–FR-12 y filas relacionadas
  reflejan la implementación/validación local; se añade TASK043 a evidencias e historial;
  se mantienen pendientes instalación limpia, auditoría, publicación y despliegue.
- `docs/requirements/requirements-traceability.md`: versión/delta TASK043, estados CH/FR
  y evidencias; se preservan las tablas marcadas explícitamente como contextos históricos.
- `docs/planning/mvp-roadmap.md`: versión/estado vigentes, resultado R8, TASK043/TASK043P
  en la tabla de ejecución y TASK044–TASK047 pendientes.
- `ai-workspace/01-tasks/TASK043P-frontend-intermediate-publication.md`: este motivo,
  subsanaciones y estado de staging.

No se modificaron código funcional, pruebas, configuración, dependencias ni otros
documentos. Antes de editar se guardó externamente SHA-256 del blob staged inicial de los
cinco documentos autorizados y de los otros 85. La comparación posterior a renovar el
staging confirma que sólo cambiaron los hashes de esos cinco documentos; los otros 85
permanecen idénticos.

## 4. Protección, exclusiones y análisis dirigido

- Los 162 archivos protegidos de `TASK043-initial-hashes.json` mantienen sus hashes:
  archivos históricos, código/tests/migraciones backend, `backend/requirements.lock`,
  `LICENSE` y versiones de los manifiestos npm protegidas por la captura.
- Sin cambios TASK043 en `backend/src`, `backend/tests`, `backend/migrations`,
  `backend/requirements.lock`, `frontend/package.json` o `frontend/package-lock.json`.
- Los 89 candidatos previos se revisaron por correspondencia con TASK041–TASK043; los
  informes de esas tareas, SPEC-007–009 y manifiestos conservan el detalle de alcance.
- Los literales de correo corresponden a fixtures sintéticos del repositorio
  (`example.com`, `.test` y `ejemplo.es`); no se halló correo de cliente real. El escaneo
  dirigido no halló tokens, claves privadas, credenciales ni rutas absolutas personales
  en candidatos textuales.
- No hay candidatos `node_modules`, `.venv`, `dist`, test-results, capturas, logs,
  archivos SQLite ni otros artefactos generados.
- `git diff --check` pasa; no se encontraron enlaces Markdown relativos rotos.
- Prettier del informe TASK043P pasa. `prettier --check` en los cuatro documentos raíz
  corregidos advierte formato no conforme; la misma comprobación también advertía en sus
  blobs staged previos a la subsanación. Prettier no está configurado como script de
  formato de documentación raíz; se preservó el estilo existente y `git diff --check`
  verifica las modificaciones.
- El DOCX original no se incluye. Para staging se usará una lista exacta de rutas, no
  una operación global; el que siga sin estar ignorado por Git no implica inclusión.

Estos escaneos son dirigidos y no constituyen auditoría SAST/DAST, revisión legal ni
garantía absoluta de ausencia de datos sensibles.

## 5. Validaciones ejecutadas

### Frontend

Con el árbol de dependencias existente; no se ejecutó `npm ci` ni se alteraron paquetes:

| Comprobación                       | Resultado                                          |
| ---------------------------------- | -------------------------------------------------- |
| `npm run typecheck`                | PASS                                               |
| `npm run lint`                     | PASS; todos los archivos                           |
| `npm run format:check`             | PASS                                               |
| `npm test`                         | PASS; 37 pruebas / 11 archivos                     |
| `npm run e2e` determinista         | PASS; 17 pasaron, 2 opt-in omitidas explícitamente |
| Playwright captura visual opt-in   | PASS; 1 prueba ejecutada aparte                    |
| Playwright integración real opt-in | PASS; 1 prueba ejecutada aparte                    |
| `npm run build`                    | PASS; build de producción                          |
| `npm audit`                        | PASS; 0 vulnerabilidades                           |
| `npm audit --omit=dev`             | PASS; 0 vulnerabilidades                           |

`npm install-scripts ls`, ejecutado desde `frontend/`, identifica cuatro scripts no
autorizados: `@parcel/watcher@2.6.0`, `esbuild@0.28.2`, `lmdb@3.5.6` y
`msgpackr-extract@3.0.7`. No se aprobó ninguno. Conforme a esta autorización, `npm ci`
no se ejecutó; una instalación limpia reproducible queda pendiente de una autorización
que permita evaluar esos scripts.

### Backend

Usando exclusivamente `backend/.venv`:

| Comprobación        | Resultado                                |
| ------------------- | ---------------------------------------- |
| Ruff check          | PASS; todos los checks                   |
| Ruff format --check | PASS; 90 archivos formateados            |
| mypy                | PASS; 83 archivos fuente                 |
| pip check           | PASS; requisitos instalados consistentes |
| Pytest              | PASS; 579 pruebas                        |

### Integración real Angular–FastAPI–SQLite

Se aplicaron Alembic 0001–0004 sobre SQLite temporal y se inició FastAPI desde
`backend/.venv`. Playwright con Chromium ejecutó **1 escenario integrado, pasado**, con
clientes sintéticos:

- Cliente ES, alta/búsqueda/ficha y parámetros de referencia: subtotal `140.00` EUR,
  impuesto `29.40`, total `169.40`.
- Dos cambios de preview no aumentaron el historial; tras el guardado explícito, el
  historial presentó exactamente un registro antes de cualquier creación adicional de
  la prueba; la consulta persistió tras recargar.
- Se validó cero usuarios y cliente PT (total `172.20` EUR con tasa fiscal retornada
  por FastAPI).
- Consultas puntuales externas, fuera de la suite determinista: USD HTTP 200, tasa
  `1.0998`, total convertido `186.31`; GBP HTTP 200, tasa `0.83348`, total `141.19`.
  Referencia devuelta: `2026-11-18`; no se describen como tipos en vivo garantizados.
- Se detuvieron servicios y se eliminaron DB, logs y PID temporales creados para esta
  validación. Las capturas existentes permanecen fuera del repositorio.

## 6. Hallazgos visuales pendientes para TASK044

Veredicto facilitado por el arquitecto: **APTA CON OBSERVACIONES**. Se registran sin
corregir, clasificar como defectos confirmados ni alterar el código durante TASK043P:

- **V43-01 — Alta:** posible inconsistencia entre 16 usuarios mostrados y resultado
  guardado correspondiente a 15. Para 16 usuarios en España, subtotal esperado
  `148.00` EUR, impuesto `31.08`, total `179.08`. Determinar en TASK044 si es fixture,
  carrera de estados o defecto funcional real. No se modifica ni se declara resuelto.
- **V43-02 — Media:** desplazamiento anómalo de cabecera y aparición del enlace de
  accesibilidad en varias capturas; investigar sin eliminar accesibilidad.
- **V43-03 — Media:** mejorar visibilidad de estimación al editar en móvil.
- **V43-04 — Media:** mejorar pista y referencias del slider, diferenciando rangos.
- **V43-05 — Media:** mensajes de validación específicos junto a campos y ocultar
  reparto por tramos para cantidades inválidas.
- **V43-06 — Media:** estados inequívocos de carga, error FX, preview obsoleta y
  resultado guardado.
- **V43-07 — Baja:** separación iconos/texto, quitar títulos/botones redundantes y
  traducir términos técnicos innecesarios.

La existencia de un hallazgo no confirma por sí sola un defecto de código. TASK043P no
los corrige ni sustituye la aprobación final del frontend.

## 7. Riesgos y limitaciones

- La instalación limpia no se verificó porque `npm ci` está prohibido en este encargo;
  los cuatro scripts siguen sin aprobación.
- Los dos escenarios opt-in se reportan por separado: la integración real depende del
  servidor/SQLite temporal, y la evidencia visual determinista se ejecuta al indicar
  `TASK043_SCREENSHOT_DIR`.
- La conversión FX externa es una observación puntual; depende del proveedor y no es
  una suite determinista ni cotización de mercado en directo.
- Auditoría formal WCAG, SAST/DAST, CI y despliegue siguen pendientes.
- Los hallazgos V43-01–07 siguen abiertos; V43-01 requiere diferenciar fixture/carrera
  de defecto real.

## 9. Estrategia y operaciones Git autorizadas

**Staging selectivo ejecutado y revisado.** El índice contiene exactamente las 90 rutas
autorizadas; `Prueba Devs con IA.docx` sigue fuera. Se renovó el staging únicamente para
los cuatro documentos corregidos y este informe mediante los paths explícitos autorizados.
`git diff --cached --check`, inventario, revisión staged y escaneos dirigidos pasan.
El commit y push aún no se han ejecutado.

1. Crear un único commit, sin amend, con mensaje exacto:
   `feat: implement SaaS-O-Matic MVP frontend`.
2. Verificar hash, padre, mensaje y rutas del commit.
3. La rama remota `feature/mvp-frontend` no existía en la comprobación previa. Si sigue
   ausente y no hay divergencia, publicar con
   `git push -u origin feature/mvp-frontend`; si aparece o diverge inesperadamente,
   detenerse y pedir instrucciones. Nunca usar force.
4. Verificar hash remoto, árbol/índice local, `main` local y `origin/main`.

Autorizado específicamente por el propietario: staging selectivo de esos 90 archivos,
un commit con el mensaje indicado y push de `feature/mvp-frontend`. No están autorizados
PR, merge, rebase, cherry-pick, reset, clean, stash, amend, force-push, cambios en
`main`, correcciones V43 ni tareas posteriores.
