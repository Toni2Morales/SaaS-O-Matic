# Plan TASK042 — Dashboard y gestión comercial de clientes

| Campo | Valor |
| --- | --- |
| Base | rama `feature/mvp-frontend`, HEAD `23cc43b486d20f7995a2cf29375e3f724f3c7c3f` |
| Especificación | [spec.md](spec.md) |
| Estado | Especificación preparada antes del código funcional |

## Fases

1. Verificar rama/HEAD/main/remote, índice, conteos y capturar hashes iniciales en
   `ai-workspace/01-tasks/TASK042-initial-hashes.json`.
2. Revalidar TASK041 (`npm test`, `npm run e2e`, build/lint/typecheck/format, backend
   579 tests); releer stack/specs/contratos.
3. Evaluar audit completo y prod-only, `npm ls/explain`, advisory oficial, exposición
   y scripts de instalación. Sin tocar deps/lock/scripts allowlist.
4. Finalizar SPEC-008, plan y checklist antes de implementar UI/servicios.
5. Crear data access de clientes/history sobre HttpClient actual; tests de URL/method/
   query/body/typed responses, problemas.
6. Crear shared states y componentes visuales de dashboard/listado; señales locales,
   streams cancelables y paginación server-side.
7. Crear formularios con `NonNullableFormBuilder`, validators y server error mapping;
   proteger submit doble, integrar rutas.
8. Crear ficha/history con carga independiente, formato exacto de valores y fechas,
   pagination y generación antigua.
9. Mejorar shell sólo con iconos SVG inline, close mobile y gestión de foco.
10. Añadir pruebas unitarias de carreras/formatos/form, E2E test doubles etiquetados y
    escenario API real con SQLite temporal incluyendo snapshots históricos si es posible.
11. Ejecutar todas las verificaciones, inspección screenshots desktop/mobile/empty/error,
    comparar manifest hashes, actualizar docs vigentes y registro.
12. Confirmar sólo acumulado local sin staging/commit/push/PR/merge; TASK043 no iniciar.

## Decisiones de diseño ya delimitadas

- Dashboard lista `limit=6` y comunica que no representa “recientes”. Total desde
  `response.total`.
- Listado limit 20 inicial; permite 10/20/50, `offset`; query params URL para search/
  limit/offset si se implementa sin duplicar estado.
- Form envía `legal_name.trim()`, preserva tax_id original; errores `ProblemDetails`
  mapear sólo a controles conocidos.
- Valores monetarios sólo se formatean con utilidades decimales string + BigInt para
  grouping, nunca Number. Null no equivale a cero.
- Timestamp renderizado en zona local; fecha calendar-only se maneja por componentes.
- Errores de HTTP y estados compartidos no almacenan estado de feature global.
- Simulación desde el dashboard va al listado con explicación; ficha enlaza a la ruta
  del placeholder contextual de TASK043.
- Dependencias y package manifests de TASK041 quedan byte-identical.

## Riesgos

- Backend presenta errores field extension opcional; robustecer validación del shape.
- Formularios tax_id tienen reglas diferentes por país, mantener explicación veraz.
- Debounce/switchMap/finalize y paginación total cambiante generan race conditions.
- `Intl`/BigInt debe preservar decimal original, incluso para cadenas no válidas o
  significativas; probar en navegadores actuales.
- Drawer existente es custom CSS; mejorar sin importar CDK unused dependency.
- Seed de historial para E2E sólo mediante API real en temp DB, no editar SQLite.
- El advisory histórico cambió estado durante la ventana de tarea; registrar fecha y
  fuentes oficiales sin poner allowlist.
