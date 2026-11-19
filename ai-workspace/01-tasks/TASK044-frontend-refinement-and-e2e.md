# TASK044 — Refinamiento del frontend, accesibilidad, responsive e integración E2E

| Campo          | Valor                                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------------------ |
| Fecha          | 2026-11-19                                                                                             |
| Rama / base    | `feature/mvp-frontend`, `84b087af352c1082880417ce10f7c2ede9b7108e`                                     |
| Estado         | Implementado y validado localmente con observaciones; revisión del propietario pendiente; sin publicar |
| Especificación | [SPEC-010](../../docs/specs/010-frontend-refinement-and-e2e/spec.md), plan y tareas                    |
| Alcance        | Frontend, pruebas y documentación vigente. Sin cambios de backend, contratos ni dependencias.          |

## 1. Resumen y estado Git

La tarea refinó simulador, foco/navegación, etiquetas, errores de campo, ficha, historial,
estados vacíos y responsive. Se añadieron regresiones E2E para carreras, invalidación,
guardado único, respuesta definitiva diferente y V43-01. FastAPI siguió siendo la autoridad
económica. La tarea **no está cerrada como entrega**: quedan observaciones de cobertura y
comprobaciones visuales/accesibilidad descritas abajo.

Inicial: `feature/mvp-frontend`; HEAD y `origin/feature/mvp-frontend` iguales a
`84b087af352c1082880417ce10f7c2ede9b7108e`; `origin/main` en
`23cc43b486d20f7995a2cf29375e3f724f3c7c3f`; `main` local en
`8371f9f608ce6e06984cc501d8240e1b7edf34d5`; índice vacío, ningún tracked modificado,
DOCX del reto no seguido. `git fetch origin` no reveló divergencias.

Final: misma rama/HEAD y referencias; índice vacío. Cambios locales no publicados y
`Prueba Devs con IA.docx` sigue excluido/no seguido. No se ejecutaron staging, commit,
push, PR, merge, rebase, cherry-pick, reset, clean ni stash. TASK045 no se inició.

## 2. Baseline, SPEC y diagnóstico

- Manifiesto inicial: [TASK044-initial-hashes.json](TASK044-initial-hashes.json), 256 archivos
  tracked, 168 protegidos; SHA-256 del DOCX guardado sin abrirlo.
- SPEC-010/plan/tareas se escribieron antes de las correcciones funcionales.
- Baseline observado: frontend 37 Vitest, Playwright 17 pass y 2 opt-in; typecheck/lint/
  Prettier/build correctos. Backend Ruff, formato, mypy, pip check y 579 Pytest correctos.
- V43-01: fixture visual de TASK043 calculaba importes de 15 usuarios aunque la UI enviaba 16. Se corrigió para que sólo use referencias explícitas, sin inventar respuestas por
  defecto. Integración real mostró que el producto envía 16, recibe y persiste 148.00 EUR,
  IVA 31.08, total 179.08; 15 envía/recibe/persiste 140.00, 29.40 y 169.40. No se confirmó
  defecto de producto en estos escenarios.
- V43-02: diagnóstico de viewport encontró skip link no enfocado inicialmente, scroll 0
  y topbar normal; la anomalía se reprodujo en `fullPage`. Se preservó el enlace y se añadió
  foco explícito al `main` al activarlo por teclado. No se atribuye todo artefacto de captura
  a un defecto del usuario final.

## 3. Implementación y observaciones UX/V43

- Concurrencia: debounce/cancelación, respuesta tardía, invalidez inmediata, doble envío,
  POST ambiguo sin retry y diferencia preview/201 cubiertos por Playwright. Se reinicia el
  formulario/estado al cambiar de cliente. No se cambió backend.
- Móvil: resumen mensual compacto disponible en viewport estrecho. Se eligió **no sticky**
  tras comprobar visualmente que el elemento sticky cubría contenido al desplazarse. Sin
  importe cuando el formulario está inválido/estimación obsoleta.
- Slider: nombre/valor accesibles, rango visual 0–1.000 y explicación del rango manual hasta
  1.000.000; el valor manual no se clampa.
- Validación: errores específicos requerido/entero/mínimo/máximo, bandas no mostradas si
  usuarios inválido y sin preview adicional en formulario inválido.
- Navegación: foco del título tras cambio de ruta, skip link conservado con activación
  explícita, foco de apertura/cierre de menú probado; scroll-margin para cabecera.
- Textos/consistencia: desduplicación de títulos visibles, búsqueda con etiqueta breve y
  nombre accesible completo, historial «cálculo original», resumen de llamadas sin coste,
  mejor affordance a ficha y SVG de estado vacío.

Estados de hallazgos:

| Hallazgo                       | Estado final               | Evidencia / observación                                                                               |
| ------------------------------ | -------------------------- | ----------------------------------------------------------------------------------------------------- |
| UX-01 títulos duplicados       | RESUELTO                   | Inspección visual y H1 único en simulador; historial simplificado.                                    |
| UX-02 ayuda móvil              | CUMPLIDO CON OBSERVACIONES | Resumen móvil revisado; no auditoría en todos los campos/zooms.                                       |
| UX-03 paginación recortada     | NO REPRODUCIDO             | Se añadieron reglas flex-wrap en historial; sin captura específica de paginación larga.               |
| UX-04 espacio icono/texto      | CUMPLIDO CON OBSERVACIONES | SVG vacío y affordance; revisión visual no exhaustiva de cada icono.                                  |
| UX-05 cromática                | NO APLICA                  | Paleta TASK043 preservada; no se declara nueva unificación.                                           |
| UX-06 acceso a ficha           | RESUELTO                   | Enlace «Abrir ficha» explícito y E2E.                                                                 |
| UX-07 etiqueta buscador        | RESUELTO                   | Etiqueta compacta y `aria-label` completo.                                                            |
| UX-08 iconografía vacía        | RESUELTO                   | Icono SVG contextual, decorativo para AT.                                                             |
| UX-09 terminología técnica     | CUMPLIDO CON OBSERVACIONES | Terminología visible seleccionada revisada; no auditoría lingüística exhaustiva de todos los estados. |
| UX-10 contador historial móvil | CUMPLIDO CON OBSERVACIONES | Contador tipo chip y paginación flexible; validación a tamaños de layout.                             |
| V43-01                         | RESUELTO                   | Causa fue fixture visual; integración real 15/16 concordante.                                         |
| V43-02                         | CUMPLIDO CON OBSERVACIONES | Skip link funcional, keyboard E2E; diferencia full-page/viewport registrada.                          |
| V43-03                         | RESUELTO                   | Resumen mensual compacto no sticky; captura móvil.                                                    |
| V43-04                         | RESUELTO                   | Límites y rango manual visibles; teclado E2E.                                                         |
| V43-05                         | RESUELTO                   | Errores específicos, inválidos sin bandas/requests.                                                   |
| V43-06                         | CUMPLIDO CON OBSERVACIONES | Casos críticos automatizados; no se certifica exhaustivez de todas las carreras.                      |
| V43-07                         | RESUELTO                   | Textos e iconografía acotados; sin rediseño.                                                          |

## 4. Integración real, FX y evidencias

FastAPI se ejecutó desde `backend/.venv`, Alembic aplicó 0001–0004 a SQLite temporal y
Playwright/Angular usaron proxy same-origin en un puerto temporal. La prueba real pasó:

- Dashboard/listado, alta ES sintética, fiscal inválido y duplicado, Portugal, búsqueda,
  ficha e historial vacío.
- ES 15: preview HTTP 200, ningún registro antes del guardado, POST HTTP 201 con body
  `user_count=15`, resultado 140.00/29.40/169.40; historial y reload conservan el registro.
- ES 16: preview HTTP 200, ningún registro antes del guardado, POST HTTP 201 con body
  `user_count=16`, resultado 148.00/31.08/179.08; historial y reload conservan el registro.
- Cero usuarios y Portugal comprobados. No se usa el motor económico en Angular.
- FX puntual vía FastAPI, 2026-11-19: USD HTTP 200, tasa `1.0997`, `186.29`; GBP HTTP 200,
  tasa `0.83348`, `141.19`. Es consulta puntual, no disponibilidad garantizada.
- Se detuvieron los uvicorn de TASK044 en puertos 8001–8004 y se retiraron las DB de
  integración de cada ejecución completada. El fichero `real-integration.sqlite3` creado
  en el intento inicial permanece bloqueado por un proceso uvicorn preexistente que ocupa
  el puerto 8000; no se atribuyó ni se detuvo ese proceso, y no fue el backend usado para
  validar. Queda pendiente retirar ese fichero temporal cuando el propietario confirme
  que puede detener el proceso que lo mantiene abierto.

21 PNG de navegador real quedaron fuera del repositorio en la carpeta temporal TASK044:

`TASK044-dashboard-desktop.png`, `TASK044-dashboard-mobile.png`,
`TASK044-clientes-desktop.png`, `TASK044-clientes-mobile.png`,
`TASK044-registro-desktop.png`, `TASK044-registro-mobile.png`,
`TASK044-ficha-historial-desktop.png`, `TASK044-ficha-historial-mobile.png`,
`TASK044-simulador-desktop.png`, `TASK044-simulador-mobile.png`,
`TASK044-simulador-mobile-resumen.png`, `TASK044-simulador-15-usuarios.png`,
`TASK044-simulador-16-usuarios.png`, `TASK044-simulador-usd.png`,
`TASK044-simulador-gbp.png`, `TASK044-simulador-validacion.png`,
`TASK044-simulador-error-fx.png`, `TASK044-simulacion-guardada.png`,
`TASK044-historial-persistido.png`, `TASK044-menu-mobile.png`,
`TASK044-foco-teclado.png`.

13 capturas de alta/listado/ficha/simulador/guardado/historial/menú/foco se generaron con
FastAPI+SQLite real; 8 capturas de dashboard, simulador general/divisas/validación/error FX
usan APIs determinísticamente interceptadas y fixture explícita. No son mockups.

## 5. Instalación, dependencias, cobertura y build

- `npm ci --ignore-scripts` en copia limpia final: 402 paquetes, 0 vulnerabilidades en el
  informe de instalación. Typecheck, lint, Prettier, Vitest 37/37, build (395.14 kB) y
  Playwright 20 PASS/3 opt-in skips pasaron en esa copia final. Esta fue instalación sin
  scripts, **no** instalación normal.
- Scripts no autorizados; no se ejecutaron: `@parcel/watcher@2.6.0` (`install:
node scripts/build-from-source.js`, addon nativo/build fallback, opcional); `esbuild@0.28.2`
  (`postinstall: node install.js`, selección/verificación del binario opcional por plataforma);
  `lmdb@3.5.6` (`install: node-gyp-build-optional-packages`, addon nativo y paquetes
  opcionales); `msgpackr-extract@3.0.7` (mismo instalador opcional nativo, transitivo por
  `lmdb -> msgpackr`). Son herramientas/dependencias transitivas de compilación/cache,
  no dependencias runtime de negocio. Se recomienda mantener bloqueada la ejecución
  indiscriminada y aprobar scripts concretos sólo tras revisión independiente de origen,
  artefactos y necesidad.
- `npm audit` y `npm audit --omit=dev`: 0 issues reportados. No equivalen a SAST/CVE audit.
- Coverage: no hay provider de Vitest instalado en dependencias raíz; no se midió y no se
  instaló provider.
- Build producción final: initial 395.14 kB raw (99.11 kB transfer estimado), chunks lazy,
  sin advertencias reportadas. Baseline TASK044 inicial 394.68 kB raw: delta +0.46 kB;
  TASK042 histórico 394.56 kB. El incremento es inferior a 1 kB.

## 6. Validación final ejecutada

- Frontend: typecheck PASS; ESLint PASS; Prettier PASS; Vitest 37/37 PASS (11 archivos);
  Playwright general 20 PASS, integración real opt-in 1 PASS, visual opt-in 1 PASS;
  corrida general omite explícitamente integración y dos capturas opt-in (3 skips).
- Build producción PASS; bundle anotado arriba. npm audit completos y producción: 0.
- Backend: Pytest 579/579 PASS; Ruff check PASS; Ruff format 90 archivos PASS; mypy 83
  archivos PASS; pip check PASS. Backend no modificado.
- `git diff --check`: PASS tras implementar código; se vuelve a comprobar tras esta
  documentación. Cobertura, ejes Firefox/WebKit, zoom real del SO y auditoría automatizada WCAG
  no ejecutados; no se declara WCAG AA.
- Prettier del frontend pasa. El `--check` dirigido a Markdown de documentación avisó de
  seis archivos (README raíz, `ai-workspace` README/contexto, requisitos y roadmap); cuatro
  ya figuraban con advertencias preexistentes en TASK043P. No se reformatearon documentos
  históricos de forma indiscriminada; SPEC-010 y el informe TASK044 sí se formatearon.

## 7. Riesgos/pendientes

La suite unitaria Vitest sigue en 37; el incremento de regresiones fue principalmente E2E.
Algunos hallazgos responsive/terminológicos se comprobaron por ruta pero no con una matriz
visual exhaustiva por cada tamaño/zoom/estado. Las capturas interceptadas no prueban backend;
la prueba real cubre los escenarios descritos, no todas las divisas en guardado real.
No se implementó observabilidad backend A39-07 ni se ejecutó cambio backend; no se confirmó
una necesidad que autorice tal cambio. A39-08 sigue deuda baja. Sin CI, despliegue, auditoría
independiente ni certificación WCAG. Publicación incremental recomendada sólo después de
revisión técnica/visual del propietario y autorización expresa.

## 8. Criterios de aceptación (40)

`CUMPLIDO` sólo refleja evidencia ejecutada. `CUMPLIDO CON OBSERVACIONES` expresa cobertura
parcial o limitación; `NO CUMPLIDO` requiere trabajo/decisión pendiente.

|  CA | Estado                     | Motivo breve                                                                    |
| --: | -------------------------- | ------------------------------------------------------------------------------- |
|  01 | CUMPLIDO                   | Refs, rama, fetch y árbol inicial comprobados.                                  |
|  02 | CUMPLIDO                   | Baseline real de frontend/backend registrado.                                   |
|  03 | CUMPLIDO                   | SPEC/plan/tasks antes de correcciones funcionales.                              |
|  04 | CUMPLIDO                   | Fixture contrastado con API/UI/SQLite reales.                                   |
|  05 | CUMPLIDO                   | 15/16 preview, 201 y persistencia concordantes.                                 |
|  06 | CUMPLIDO CON OBSERVACIONES | Respuesta obsoleta e invalidez en E2E; no exhaustivez de todos los tiempos.     |
|  07 | CUMPLIDO                   | Doble submit bloqueado; una creación; fallo ambiguo sin retry.                  |
|  08 | CUMPLIDO CON OBSERVACIONES | Estados críticos y UI revisados; cobertura total de rutas pendiente.            |
|  09 | CUMPLIDO                   | 503 FX conserva controles y permite retry/EUR; suites deterministas.            |
|  10 | CUMPLIDO CON OBSERVACIONES | Foco de navegación y captura examinados; no auditoría cross-browser.            |
|  11 | CUMPLIDO                   | Skip link permanece y mueve foco al main; E2E teclado.                          |
|  12 | CUMPLIDO                   | Resumen móvil visible y no sticky/obstructivo.                                  |
|  13 | CUMPLIDO                   | Slider y valores manuales diferenciados y probados.                             |
|  14 | CUMPLIDO                   | Errores de requerido, entero y rango asociados; bandas ocultas.                 |
|  15 | CUMPLIDO CON OBSERVACIONES | UX-01–10 evaluados; UX-03/05 no se declaran defectos nuevos.                    |
|  16 | CUMPLIDO CON OBSERVACIONES | V43-01–07 evaluados con estados explícitos.                                     |
|  17 | CUMPLIDO                   | Paleta y estructura existentes preservadas.                                     |
|  18 | CUMPLIDO CON OBSERVACIONES | Textos visibles seleccionados refinados, revisión no exhaustiva.                |
|  19 | CUMPLIDO CON OBSERVACIONES | Estados funcionales clave probados; no todas las variantes visuales.            |
|  20 | CUMPLIDO CON OBSERVACIONES | Viewports automatizados clave; no todos los estados en cada viewport.           |
|  21 | CUMPLIDO CON OBSERVACIONES | Teclado/menu/skip/slider; no inspección completa con lector de pantalla.        |
|  22 | CUMPLIDO CON OBSERVACIONES | Revisión manual y señales automatizadas; sin axe/contraste completo.            |
|  23 | CUMPLIDO CON OBSERVACIONES | `npm ci --ignore-scripts` limpio; no instalación estándar.                      |
|  24 | CUMPLIDO CON OBSERVACIONES | Cuatro scripts/paquetes y finalidades analizados; no ejecutados.                |
|  25 | CUMPLIDO                   | Manifiestos/lockfiles no modificados.                                           |
|  26 | CUMPLIDO CON OBSERVACIONES | E2E ampliado; Vitest sigue en 37, no se añadió suite unitaria crítica integral. |
|  27 | CUMPLIDO                   | 20 E2E normales pasan; capturas opt-in pasan dedicadas.                         |
|  28 | CUMPLIDO                   | Angular/FastAPI/SQLite reales, migraciones y flujo ES/PT.                       |
|  29 | CUMPLIDO                   | Conteo DB/historial no cambia en preview antes de guardar.                      |
|  30 | CUMPLIDO                   | HTTP 201, IDs, valores y persistencia tras reload comprobados.                  |
|  31 | CUMPLIDO CON OBSERVACIONES | EUR/USD/GBP puntuales; no guardado real separado por cada divisa.               |
|  32 | CUMPLIDO                   | Build, chunks y delta bundle medidos.                                           |
|  33 | CUMPLIDO                   | 579 Pytest, Ruff, formato, mypy y pip check.                                    |
|  34 | CUMPLIDO                   | npm audit y omit-dev, ambos 0.                                                  |
|  35 | CUMPLIDO CON OBSERVACIONES | 21 PNG fuera del repo; varias capturas interceptadas y un grupo real.           |
|  36 | CUMPLIDO CON OBSERVACIONES | SPEC/report/índices/README actualizados; reconciliación final aún en revisión.  |
|  37 | CUMPLIDO CON OBSERVACIONES | Protección/hash se verificará al cierre; backend, LICENSE y locks intactos.     |
|  38 | CUMPLIDO                   | No hay cambios backend/deps/contratos ni acciones fuera del alcance.            |
|  39 | CUMPLIDO                   | Índice vacío; sin operaciones de publicación.                                   |
|  40 | CUMPLIDO                   | TASK045 no iniciada.                                                            |
