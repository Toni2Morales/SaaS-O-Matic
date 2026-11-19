# Plan — SPEC-010

## Principios

- Rama existente `feature/mvp-frontend`; sin cambios Git de publicación.
- Hashes iniciales antes de editar; preservar archivos protegidos.
- Primero reproducir; luego corregir sólo causas confirmadas y autorizadas.
- Cero cambios en dependencias, contratos y cálculos backend.
- Capturas de navegador real y datos sintéticos, fuera del repositorio.

## Fases

1. **Baseline y análisis:** verificar refs/working tree, hashes, scripts/dependencias,
   reports/screenshots TASK043 y SPEC-007–009; materializar SPEC-010/plan/tasks antes del
   código. Reproducir V43-01 mirando el fixture y confirmar con servicio real.
2. **Pruebas de regresión:** añadir casos 15/16 que verifican parámetro, response, estado y
   historial; explorar foco/scroll/skip link en captura viewport y full-page; identificar
   transiciones de estado y layouts móvil.
3. **Integridad/concurrencia:** auditar formulario, request fingerprints y generación de
   preview, cancelación, guardado único y errores; ajustar componentes sólo ante defecto
   reproducido. Hacer estados mutuamente claros.
4. **UX y accesibilidad:** resumen móvil no obstructivo si es verificable; pista/labels del
   slider, mensajes de validación, bandas condicionales, textos comerciales, navegación,
   estados vacíos, títulos y páginas de clientes/historial.
5. **E2E real:** FastAPI real + SQLite temporal/migraciones 0001–0004 y clientes sintéticos.
   Comprobar España 15/16 y Portugal; preview no inserta, guardado de una sola fila, historia
   y reload. FX externo se intenta aparte.
6. **Instalación y regresión:** npm ci --ignore-scripts en carpeta aislada; quality scripts;
   suites deterministas y Playwright; backend pytest/Ruff/mypy/pip check en `.venv`. npm
   audits; hashes/cambios/links/secrets/artifacts.
7. **Evidencia y cierre:** 21 capturas con procedencia real/interceptada identificada, informe
   TASK044, updates vigentes y aceptación individual. Mantener índice vacío y detenerse.

## Hipótesis iniciales

V43-01 probablemente se relaciona con fixture de evidencia que devuelve importes fijos para
un rango de usuarios; esto no concluye que el producto esté libre de carrera. No se aceptará
como causa hasta comparar cuerpo real, respuesta backend y DB en 15/16.

V43-02 podría ser efecto del skip link enfocado o de `position: sticky` durante captura
full-page. La causa debe verificarse con el foco activo, scroll y screenshot viewport; no se
elimina ninguna funcionalidad de accesibilidad.

V43-03–07 y UX-01–10 son objetivos visuales/funcionales, no causas confirmadas. Se documenta
para cada uno reproducción y decisión.

## Archivos previstos

- `frontend/src/app/features/simulations/simulation-page.ts` y sus pruebas/E2E.
- `frontend/src/app/core/layout/app-shell.ts`, `.html`, `.scss` sólo si la investigación de
  foco/topbar lo requiere; `frontend/src/styles.scss` únicamente vía tokens públicos.
- Componentes de cliente/historial/dashboard y sus tests, sólo para UX autorizado.
- `frontend/e2e/` para integración/determinismo y capturas opt-in.
- Documentación vigente y `ai-workspace/01-tasks/TASK044-*`.
- Sin backend, migraciones, dependencias, package manifests/lock, LICENSE ni informes
  TASK001–TASK043P.

## Validación

Las comprobaciones ya reportadas por TASK043P son baseline, no resultado TASK044. Cualquier
instalación omitida/no disponible, servicio externo fallido, navegador no cubierto o auditoría
no ejecutada se informará de forma separada.
