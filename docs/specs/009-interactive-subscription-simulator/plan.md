# Plan — SPEC-009

## Enfoque

Implementación local y en incrementos pequeños sobre `feature/mvp-frontend`. Mantener
sin cambios backend, pruebas/migraciones backend, dependencias, lockfiles y registros
TASK001–TASK042. Conservar índice vacío y no publicar.

## Fases

1. **Contratos y especificación:** manifiesto de hashes; contrastar OpenAPI real,
   modelos, estilos, rutas y pruebas existentes; crear SPEC-009/plan/tasks antes del
   código (completado antes de iniciar fase 2).
2. **Acceso a datos y modelos:** añadir métodos tipados de preview y creación al
   `ApiClient` y servicio de simulaciones; pruebas HTTP exactas. Ampliar tipos solo si
   están probados por OpenAPI.
3. **Estado y formulario:** construir feature standalone con carga validada de cliente,
   Reactive Form estricta, límites y sincronización manual/slider sin clamp. Diseñar
   flujo RxJS de invalidación inmediata, debounce, deduplicación, cancelación y control
   de generación.
4. **Presentación y persistencia:** estados diferenciados, resultado exacto, error FX y
   reintento; POST explícito congelando formulario, respuesta 201 autoritativa y refresco
   del historial. Integrar entradas desde ficha/historial/dashboard y focos accesibles.
5. **Diseño:** paleta Material vía API pública; resultado en dos columnas y móvil;
   revisión de interacciones y foco programático.
6. **Pruebas y ejecución real:** ampliar Vitest/Playwright, mantener las previas, probar
   dimensiones requeridas, integración Angular–FastAPI–SQLite temporal, caso ES,
   internacional y cero, y FX externo si disponible. Capturas reales fuera del repo.
7. **Regresión y trazabilidad:** npm ci sin cambios de manifests, typecheck/lint/format,
   Vitest/E2E/build/audits, 579 Pytest, diff/checks/hashes/secretos/enlaces/index;
   actualizar documentación vigente e informe TASK043 con evidencia real y evaluación
   individual de aceptación.

## Decisiones de implementación

- Estado de interfaz local a la página con Signals; no servicio de estado global.
- Solicitudes de preview únicamente por `/api/simulations/preview` y guardado por
  `/api/simulations`; los parámetros enviados provienen del formulario validado.
- Cuatro controles numéricos con valor interno tolerante a edición y serialización solo
  si es entero finito y dentro de rango. Sin cálculos monetarios del navegador.
- Slider se deshabilita en valores manuales fuera de 0..1.000 y muestra explicación;
  no modifica el valor de usuario.
- Actualización del historial mediante mecanismo público ya usado por la feature o
  navegación/recarga de su consulta; no insertar datos optimistas.
- Ningún cambio de backend, manifiesto, lock, nueva tecnología o proceso Git de
  publicación.

## Validación por fase

Cada fase ejecuta pruebas cercanas al cambio. Validación final informa comandos y
resultados numéricos reales; se declara “no ejecutada” cualquier comprobación bloqueada.
Capturas son navegador real y datos sintéticos, guardadas en carpeta temporal aprobada.
