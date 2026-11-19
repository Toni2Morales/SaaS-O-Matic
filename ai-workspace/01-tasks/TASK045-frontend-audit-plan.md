# TASK045 — Plan de auditoría técnica independiente del frontend

| Campo               | Valor                                                                                                                             |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Fecha               | 2026-11-19                                                                                                                        |
| Rama / HEAD inicial | `feature/mvp-frontend`, `8cd664262ed908e101b19a7de715560e344105ca`                                                                |
| Tipo                | Auditoría independiente, sin implementación ni cambios funcionales                                                                |
| Integridad          | [Manifiesto SHA-256](TASK045-initial-hashes.json), generado antes de las comprobaciones técnicas                                  |
| Restricciones       | Sin staging/commit/push, instalaciones con scripts, herramientas nuevas, modificación de pruebas/código o proceso del propietario |

## Objetivo y método

Contrastar el frontend TASK041–044 y su integración con los requisitos originales resumidos
por el propietario. Recoger evidencia reproducible y separar hechos observados, inferencias,
riesgos, limitaciones y preferencias. El documento original privado no se abre ni se hashea.

La inspección incluye revisión estática de arquitectura y contratos; suites oficiales sin
modificarlas; pruebas independientes temporales fuera del repositorio; integración local
contra SQLite aislada; exploración visual y de teclado; comprobación de dependencias y de
integridad del árbol al final. Las pruebas automatizadas son evidencia acotada, no prueba de
ausencia de defectos.

## Secuencia

1. **Preflight y hashes:** repositorio, rama, refs, índice, archivos, runtimes, navegadores,
   puertos/procesos. Se registra el manifiesto inicial antes de pruebas.
2. **Trazabilidad:** resumir cada requisito del reto con FR/SPEC/módulo, prueba/evidencia,
   estado independiente y riesgo de interpretación, especialmente FX intermediado.
3. **Arquitectura Angular:** componentes, estado, servicios, validación, ciclo de vida,
   errores, tipado, dependencias, tamaño/acoplamiento y rutas.
4. **Oráculo económico:** comprobar las trece cotas de pricing y seis impuestos; seguir
   conversión Decimal/rounding, snapshots y autoridad económica backend.
5. **Concurrencia:** inspeccionar código y ejecutar escenarios adversos temporales para
   preview, guardado y búsqueda (latencias invertidas, cambios, error/reintento, navegación).
6. **Integración real:** crear solo datos sintéticos en DB temporal; aplicar migraciones;
   probar clientes, búsqueda, preview sin escritura, persistencia/recarga/reinicio, límites,
   monedas y errores. No tocar el servicio ni la DB preexistentes de puerto 8000.
7. **Formularios y V44:** rangos, datos inválidos, errores, siete observaciones visuales y
   capturas estables fuera del repo.
8. **Responsive/accesibilidad/browser:** viewports 320–1440, teclado/DOM/reflow/estados;
   usar únicamente navegadores ya instalados.
9. **Seguridad y supply chain:** revisión estática inocua; cadena y scripts de cuatro
   paquetes npm sin ejecutarlos; audit solo si la conectividad permite; instalación temporal
   únicamente con `--ignore-scripts` si aporta evidencia y sin modificar el checkout.
10. **Calidad/mantenibilidad/rúbrica:** suites oficiales, pruebas y cobertura disponibles,
    build/bundle, deuda A39 y puntuación orientativa de la rúbrica.
11. **Cierre:** informe con hallazgos A45, límites, pruebas reproducibles, criterios CA01–45;
    rehash de los 263 archivos iniciales y verificación de Git. Solo permanecen los tres
    documentos TASK045 autorizados dentro del repositorio.

## Reglas de decisión

- Priorizar defectos reproducibles y riesgo observable; no fabricar hallazgos para cubrir
  una lista de categorías.
- No convertir una recomendación arquitectónica en defecto sin impacto o requisito.
- No afirmar tiempo real de mercado: distinguir interacción UI, referencia publicada y TTL.
- Un resultado externo puntual no demuestra disponibilidad ni fallo persistente del proveedor.
- No declarar conformidad WCAG con revisión parcial ni compatibilidad con navegadores no
  ejecutados.
- No ejecutar scripts npm bloqueados ni inferir seguridad total a partir de `npm audit`.
- Si las pruebas requieren intervenir sobre un proceso o datos ajenos, omitirlas y registrar
  la limitación.
- No escribir código, pruebas o configuración de producto; no realizar operaciones Git
  prohibidas.

## Línea base preliminar registrada

- `HEAD` y `origin/feature/mvp-frontend`: `8cd664262ed908e101b19a7de715560e344105ca`.
- `origin/main`: `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`.
- `main` local: `8371f9f608ce6e06984cc501d8240e1b7edf34d5`.
- Índice vacío; ningún tracked modificado; DOCX privado sin seguimiento y excluido.
- Python 3.13.17, Node 24.22.0, npm 11.19.1, Angular CLI 22.2.6,
  TypeScript 6.0.3. Puerto 8000 ocupado por proceso preexistente; no se intervendrá.
- Pendiente tras registrar el plan: inspección de paquetes, disponibilidad real de los
  navegadores, herramientas de coverage/a11y, ejecución de suites y puertos temporales.
