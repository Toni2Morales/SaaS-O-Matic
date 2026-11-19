# SPEC-008 — Dashboard y gestión comercial de clientes

| Campo | Valor |
| --- | --- |
| Estado | Especificada para implementación local TASK042 |
| Fecha | 2026-11-18 |
| Base | TASK041 en `feature/mvp-frontend` |
| Contratos | OpenAPI de backend en `main`, revisado localmente en TASK042 |
| Stack | Se conserva Angular 22.2.6 y versiones de TASK041 |

## 1. Objetivo y usuarios

Implementar el primer recorrido comercial usable: panel informativo con datos reales,
consulta/búsqueda/paginación de clientes, alta internacional, ficha y su historial
inmutable. Usuarios: equipo comercial interno; interfaz en español.

## 2. Alcance

- Dashboard con total de clientes del `total` backend y una página pequeña (hasta 6)
  de clientes para acceso rápido; la consulta no se presenta como clientes recientes.
- Capacidades del sistema: seis países (ES/PT/FR/DE/IT/NL) y divisas EUR/USD/GBP.
- Listado server-side `GET /customers`, búsqueda por razón social o tax_id, debounce
  300 ms, cancelación de anteriores, paginación limit 10/20/50 y offset.
- Alta `POST /customers`, Reactive Forms estrictos y tipados, los cinco campos
  obligatorios, países y el único plan `standard`; conflicto/validación/transport.
- Ficha `GET /customers/{customer_id}` e historial paginado
  `GET /customers/{customer_id}/simulations` en estados independientes.
- Representación de campos históricos nullable sin coerción a cero ni recálculo.
- Acciones a alta, listado y ruta nueva simulación ligada al cliente. El simulador
  sigue siendo placeholder de TASK043.
- Mejoras acotadas del shell, shared loading/empty/error states, documentación,
  pruebas unitarias, E2E y un flujo real con SQLite temporal.

## 3. Exclusiones y límites de negocio

No simulador, preview, creación/edición/borrado de simulaciones, edición/borrado de
clientes, autenticación, métricas no disponibles, exportación, orden configurable,
catálogo fiscal adicional, validación fiscal oficial fuera de ES, nuevos endpoints,
dependencias, cambios de versiones/lockfile, scripts npm autorizados ni cambios
backend. No hay facturación, MRR, clientes activos o estadísticas globales: la API no
las suministra. No se descargan todos los clientes para agregar datos.

## 4. Flujos funcionales

1. **Dashboard:** solicitar `GET /customers?limit=6&offset=0`; mostrar estado de carga,
   error recuperable, empty real o total y hasta seis empresas de la respuesta. Título
   “Panel comercial”; aclarar que los accesos son una selección del listado ordenado
   por el servidor, no una lista de altas recientes. Acciones Nuevo cliente, Buscar
   clientes y Nueva simulación (esta última conduce a elegir cliente en listado y
   explica que la simulación llegará en TASK043).
2. **Listado:** cargar el primer segmento; filtro reactivo con 300 ms; recortar
   extremos antes de enviar (contrato lo recorta también), ignorar filtro vacío;
   `distinctUntilChanged` y `switchMap`; cada término cambia offset a 0. Result count
   usa `total`, no `items.length`. Sin coincidencias y sin clientes globalmente se
   distinguen. Tabla desktop y cards semánticas mobile; razón social, tax_id, país,
   email, plan y link a ficha.
3. **Paginación:** limit 10/20/50, default API 20; backend limita 100. Desactivar
   anterior/siguiente según offset/total. Al cambiar página mantener búsqueda; al
   cambiar tamaño volver a offset 0. Estado imposible/offset fuera del total vuelve
   a página cero como máximo una vez por respuesta nueva, sin reintentar en bucle.
4. **Alta:** formulario tipado legal_name, tax_id, email, country, plan. Enviar país
   junto con tax_id. ES ayuda que el backend aplica comprobación española; otros países
   indican validación genérica, no oficial. No copiar algoritmos fiscales. Normalizar
   sólo legal_name trim en el frontend; tax_id se envía preservado (normalización es
   del backend). `standard` se envía explícitamente. Submit pendiente bloquea nuevas
   ejecuciones. Sólo response 201 genera confirmación y navegación a ficha.
5. **Alta fallida:** 409 enlaza al error general de duplicidad por país sin borrar
   datos; 422 asocia `errors[].field` sólo si el campo se reconoce y el mensaje tiene
   forma válida, de otro modo mensaje general. Fallos 500/transporte conservan valores
   y muestran mensaje seguro. En error de transporte ambiguo, explicar que la creación
   podría haberse realizado y ofrecer ir a listado; no retry automático.
6. **Ficha:** UUID malformado detectado antes de HTTP; cliente e historial se cargan
   por separado, cancelar solicitudes previas al cambio de `customerId`; 404 no es
   ficha vacía. Detalles reales, fecha de creación, link al listado y nueva simulación.
7. **Historial:** page size 10/20; `limit` máximo soportado 100; columnas principales
   de fecha, consumos, subtotal EUR, total/impuestos y display currency/convertido.
   Campos nulos “No registrado”/“No disponible” según dato. Empty y error son
   independientes del detalle de cliente. Snapshot sin datos no se recalcula.

## 5. Contrato HTTP verificado

Consultado el OpenAPI generado desde `backend/src` el 2026-11-18:

- `GET /customers?search&limit=20&offset=0` → `CustomerPageResponse` con
  `items,total,limit,offset`; `search` opcional, trim, máximo 255; limit 1..100;
  offset ≥0. Búsqueda Unicode parcial/literal sobre legal_name OR tax_id, backend
  casefold sin quitar acentos ni normalizar NFC. Orden legal_name casefold ASC y UUID
  ASC. No ordering query param.
- `POST /customers` body estricto por forma con required `legal_name` 1..255,
  `tax_id`, `email`, `country`, `plan`; respuesta `201 CustomerResponse` con UUID,
  `created_at` UTC; `409`, `422`, `500` ProblemDetails.
- `GET /customers/{customer_id}` → `200 CustomerResponse`, `404`, `422`, `500`
  ProblemDetails. UUID en path.
- `GET /customers/{customer_id}/simulations?limit=20&offset=0` →
  `200 SimulationHistoryPageResponse`, `404`, `422`, `500`. Orden created_at DESC/id
  DESC. Page total real.
- ProblemDetails reales: `type,title,status,detail` requeridos, `instance: string|null`
  y `errors: ProblemFieldError[]|null` opcionales.

Países `ES|PT|FR|DE|IT|NL`; plan literal `standard`; divisa `EUR|USD|GBP`; periodo
`monthly`. `created_at` cliente y simulación guardada son date-time UTC strings.
Fecha de referencia fiscal/FX es date-only; fecha obtenida es date-time. Importes y
tasas son cadenas exactas. En historial los consumos y snapshots fiscales/FX pueden
ser null. `created_at` historia también nullable en OpenAPI actual. Prefijo de
navegador `/api` lo elimina el proxy; backend recibe rutas sin prefijo.

## 6. Validación del formulario

- `legal_name`: required tras trim; longitud trimmed 1–255; preservar espacios
  interiores; backend autoridad.
- `tax_id`: required; no quitar puntuación/espacios en cliente. Backend normaliza ES
  (espacios/guiones y mayúsculas), valida DNI/NIE/CIF; para no-ES rechaza categorías
  Unicode Cc/Cf/Cs, recorta/colapsa espacios, upper, longitud 1–64 sin validador
  nacional oficial.
- `email`: required y verificación sintáctica Angular básica, backend EmailStr manda.
- `country`: `CountryCode` enum requerido.
- `plan`: requerido y enviado explícito `standard`.
- Tocar submit/blur para mostrar los errores; labels, ayuda, aria-describedby y
  mensajes con `role=alert`/aria-live adecuados. Conservar valores ante todos los
  errores HTTP.

## 7. Estado y concurrencia

El estado se queda por página/componente en Signals; los servicios feature data access
son wrappers HTTP sin estado global. Los stream de listado convierten control de
búsqueda y page state a consultas `switchMap`; cada respuesta/error pertenece sólo al
último query activo; `finalize`/estado por query no debe apagar el loading de una
petición nueva. `takeUntilDestroyed` para subscriptions. Errores se capturan dentro de
cada operación y permiten un query posterior. El alta no tiene retry/optimistic update.
Detalle e historial usan stream por ID y `switchMap`; un error de historial no altera
estado detalle.

## 8. Dinero, fechas y datos históricos

- La forma del valor económico permanece como cadena exacta en modelos y servicios.
  No usar `Number`, `parseFloat`, Math ni efectuar operación. Utilidad de visualización
  puede agrupar dígitos con `BigInt` y renderizar la fracción recibida sin redondeo ni
  truncado. Locale `es-ES`; símbolo/código EUR/USD/GBP explícito. Regex decimal
  inválida → “No disponible”; cero decimal exacto → importe cero. Null queda como dato
  no registrado, no cero.
- Tipo de cambio conserva todos sus dígitos; sólo presentación localiza separador,
  sin limitar precisión. No reinterpretar snapshots.
- Fecha date-time `created_at`: `Intl.DateTimeFormat('es-ES')` en zona local del
  navegador, decisión de display; fuente UTC del API no cambia. Date-only se parsea
  por componentes y presenta sin pasarlo a Date UTC/local que desplace el día.
  Null/valor malformado: “No disponible”.
- Tres generaciones representativas de historial se prueban: antes de consumos/snapshot,
  con consumos pero snapshot fiscal/FX nulo, y con snapshot completo. `0` cuenta como
  cero; null como “No registrado”/“No disponible”; nunca sustituir por total calculado,
  tasa actual, EUR asumido o snapshot reconstruido.

## 9. Estados compartidos y visuales

Reutilizar componentes standalone tipados para carga (`role=status`, mensaje), vacío
(título/explicación/acción opcional) y error (`role=alert`, mensaje seguro, reintento
explícito opcional). Distinguir error detalle/historial, listado vacío/sin coincidencias,
404 y fallo de servicio. Mantener tokens Material TASK041. Shell: iconos SVG inline
propios aria-hidden para Inicio/Clientes, indicador activo, botón de cierre visible
en drawer, gestión de foco/teclado y cierre al navegar; sin dependencias iconográficas.

## 10. Responsive y accesibilidad

Anchos de prueba 320, 360, 390, 768, 1280, 1440. Cards mobile o tabla con overflow
interno etiquetado, nunca overflow del viewport. Razón social, tax_id y email largos
rompen de forma segura. Paginación operable por teclado y aria-label. Drawer móvil
Escape, botón de cierre, restauración de foco y nombres accesibles. Formularios
labels persistentes, required text, ayuda/errores vinculados, foco a resumen/heading
tras fallo si aporta contexto. Estados anunciables, foco visible, contraste revisado,
reduced-motion. WCAG 2.2 AA objetivo, sin afirmar conformidad auditada.

## 11. Pruebas y evidencias

- Unitarias HTTP mockeado: métodos/URLs/params/body/responses/errors.
- Dashboard/listado: datos total vs items, load/error/empty, debounce 300ms,
  distinct, switchMap/cancelación, búsqueda trim, paginación, offset reset, response
  obsoleta no sobreescribe estado, cambio total sin loop.
- Alta: validaciones, seis países, standard explícito, request trim de nombre pero
  tax_id intacto, pending/doble submit, 201 y navegación; 409/422/500/transporte
  mantienen campos y no muestran éxito/retry.
- Ficha/history: UUID inválido, existente/404, cambio ID, error independiente, empty,
  paginación, tres generaciones y nullable.
- Utilidades monetarias exactas, divisas, cero/null/malformado y fecha UTC/date-only.
- E2E Chromium: backend real con DB temporal completa (alta ES e internacional, buscar,
  ficha, historial vacío, reload persistencia); los otros casos pueden interceptar
  respuestas y se etiquetan explícitamente. Historial con snapshots debe usar API
  permitida en base temporal y mostrar tipo FX sintético EUR para no necesitar red.
- E2E 409/422, error/empty, página, keyboard/mobile, validación y acceso simulador.
- Backend suite referencia 579 en `backend/.venv`; scripts npm del stack sin cambiar.

## 12. Seguridad/riesgos

- TASK041 reportó 21 avisos high por una única advisory transitiva que se propagaba
  a muchas herramientas. GitHub retiró GHSA-fc5q-39xc-vjpf / CVE-2026-112366 el
  2026-11-18; auditoría actual limpia. No modificar lock/deps. Revisar nuevamente en
  TASK045 y si advisories reaparecen.
- npm mantiene scripts opcionales no aprobados. La suite actual build/test pasa con
  scripts bloqueados; no aprobar sin decisión específica.
- Registro datos fiscales/email es PII: sólo datos sintéticos, no logging de request,
  sin persistir evidencias con clientes reales.
- No añadir ninguna dependencia, nueva ruta backend o calculador.

## 13. Criterios de aceptación

1. Dashboard obtiene total y hasta seis clientes del backend, muestra capacidades
   reales y no métricas no servidas.
2. Acciones principales navegan correctamente y nueva simulación aclara prerequisito.
3. Listado expone datos reales, búsqueda y pagina en servidor, preserva Unicode,
   parámetros literales, responde con estados load/empty/error.
4. Debounce/cancelación impiden que petición obsoleta altere UI.
5. Alta tipada, los cinco campos y seis países, plan explícito standard, ayuda fiscal
   correcta, validación, submit único y navegación sólo después de 201.
6. 409/422/server/transport comprensibles y preservan formulario; no retry automático.
7. Ficha y su historial usan endpoints separados; 404 no aparece como ficha vacía.
8. Historial paginado muestra nulos como desconocidos; dinero no se convierte ni
   recalcula; date-only no cambia el día.
9. Drawer incluye botón de cierre y foco/teclado accesible.
10. Unitarias y E2E relevantes pasan; al menos un flujo navegador→FastAPI→SQLite
    temporal de alta/búsqueda/ficha/historial/reload funciona.
11. Build/lint/format/typecheck pasan; backend 579 pass; hash-protection e índice
    limpio; no cambios npm deps, backend ni publicación.
12. TASK042 registra audit, evidencias sintéticas, screenshots temporales y limitaciones.
13. TASK043 no se inicia.
