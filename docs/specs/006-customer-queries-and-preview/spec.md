# SPEC-006 — Consultas de clientes, historial y previsualización

| Campo | Valor |
| --- | --- |
| Estado | Implementada localmente, 579 pruebas superadas; auditada en TASK039 y corregida en TASK039B; sin publicación ni revisión humana externa |
| Base | feature/mvp-backend, HEAD b3c5ca81d23d279b478ed466757bada031aa1e1e |
| Fuente | Instrucción TASK038 del propietario; requisitos y SPEC-004/005 |

## Decisiones consolidadas

Q-09/Q-24/SIM-P10: historial inmutable a través de la API; no edición ni borrado.
Q-24/SIM-P11: listado, detalle e historial públicos paginados. Q-25: preview sin
persistencia, mismo cálculo y referencias que guardado. No nuevo GET individual
de simulación ni Location; se mantienen contratos de creación. P-01/P-05 pendientes.
Los placeholders de rutas se llaman `customer_id`, coherentes con los DTO UUID;
la URI real es la solicitada (/{id}), no cambia su significado.

## GET /customers

Parámetros: search opcional, recortado; longitud máxima 255 caracteres después de
recortar; vacío equivale a ningún filtro. limit entero 1..100 (20), offset entero
no negativo (0). Query parameters con conversión habitual de enteros HTTP; sin
coerciones nuevas en cuerpos de simulación. Extras de query se ignoran según la
política normal de FastAPI, no se amplía forbid fuera de los cuerpos aprobados.

Búsqueda parcial `legal_name OR tax_id`. Función SQLite por conexión aplica Python
`str.casefold()` a columnas y patrón. LIKE parametrizado, con escape explícito de
barra inversa, `%` y `_`: el usuario no introduce comodines. No SQL concatenado.
No quitar acentos, normalizar Unicode NFC/NFKC ni hacer búsqueda difusa. É/é y
Ü/ü coinciden; casefold permite expansiones como ß/ss. No colación lingüística ni
reglas de idioma; formas compuestas/descompuestas distintas pueden no coincidir.
Orden: nombre casefold ascendente mediante colación binaria SQLite, después UUID
ascendente. No depende del orden de inserción; no es un orden alfabético por idioma.

200: {items:[CustomerResponse], total, limit, offset}. Cada cliente incluye los
campos existentes y created_at UTC. total se calcula antes de LIMIT/OFFSET. Sin
coincidencias: items [], total0; offset fuera de rango: [] con total correcto,
incluso offsets muy grandes (se evita enlazarlos a SQLite si exceden total).
422 problem+json para parámetros inválidos; 500 inesperado.

## GET /customers/{customer_id}

UUID válido obligatorio: 200 con CustomerResponse existente, 404 desconocido,
422 UUID inválido, 500 inesperado. Sin historial embebido ni estadísticas inventadas.

## GET /customers/{customer_id}/simulations

Misma paginación limit/offset. Validar parámetros, verificar cliente primero, luego
COUNT y página filtrados por customer_id. Orden created_at DESC, id DESC estable.
200: {items:[HistoricalSimulationResponse],total,limit,offset}. Cliente existente
sin datos: página vacía; cliente ausente404; UUID/parámetros inválidos422.

Elementos: id, customer_id, user_count, storage_gb, api_calls_per_month, billing_period,
user_subtotal_eur, created_at y todos los metadatos fiscales/FX de SPEC-005.
Consumos históricos y cada dato fiscal/FX pueden ser NULL. Subtotal nunca se
presenta como total con IVA; divisa histórica desconocida NULL, no EUR por defecto.
Reconstruir exclusivamente snapshot persistido: sin catálogo actual ni Frankfurter.
Las validaciones existentes de integridad del snapshot no sustituyen sus valores
ni vuelven a calcularlos con reglas/referencias actuales. Fechas recuperadas UTC.
Sin endpoints de edición/borrado; no se añade protección append-only a SQL directo.

## POST /simulations/preview

Mismo SimulationCreateRequest de creación: cuatro campos obligatorios, rangos e
integers estrictos TASK036, EUR por defecto, EUR/USD/GBP, forbid y mensual servidor.
200 con los campos de la respuesta creada salvo id y created_at persistidos. Incluye
fuentes, consulta/vigencia fiscal y referencia/obtención FX; no Location.
404/422/503/500 problem+json como guardado. EUR identidad de SPEC-005 intacta.
No INSERT/UPDATE/DELETE ni métodos de persistencia de simulaciones. Puede leer
cliente y modificar caché en memoria. Repetir preview no aumenta historial.

## Arquitectura y consultas

Puertos de lectura segregados en dominio, implementados por repositorios actuales.
Aplicación orquesta listado/detalle/historial y DTO; SQLAlchemy filtra, ordena,
cuenta y pagina. UDF de casefold registrada en create_sqlite_engine, sin alterar
esquema ni índices; ninguna migración necesaria ni modificación de 0001–0004.
Count/página implican como máximo dos SELECT; historial añade existencia de cliente.
Sin N+1 ni carga de tabla completa en aplicación. LIKE parcial/UDF puede requerir
escaneos SQLite: limitación de rendimiento aceptada, sin índices especulativos.
Offset no es snapshot estable ante escrituras concurrentes; no se añaden cursores
ni aislamiento nuevo. Sesiones de lectura sin autoflush para no provocar escrituras.

Extraer servicio de aplicación CalculateSimulation con validaciones, obtención del
país, pricing y MonthlyEstimator. CreateSimulation persiste el resultado; PreviewSimulation
solo lo transforma. Ambos reciben el mismo estimador/catálogo/proveedor/caché desde
bootstrap. No duplicar fórmulas ni confiar en importes del frontend. Una referencia
FX diferente entre preview y guardado puede cambiar resultado; no bloqueo de precio,
tokens ni reservas. No se promete igualdad de timestamps, solo de datos comerciales
cuando las referencias son idénticas.

## Pruebas y aceptación

Baseline411 preservado; probar búsqueda Unicode/acentos/literales/inyección, páginas
vacías/totales/orden/desempates, detalle y aislamiento entre clientes. Históricos de
tres generaciones, NULL y snapshots exactos sin catálogo/FX. Preview países/divisas/
límites/errores/caché/paridad y denegación SQLite de escrituras, sin Internet.
Flujo completo alta→búsqueda→detalle→preview→historial vacío→guardado→historial.
OpenAPI: parámetros/rangos/esquemas, nullability, cadenas monetarias y problem+json.
Revisión estática de capas, Ruff/mypy/pip/lock, enlaces, whitespace, huellas e índice.
No frontend ni publicación. TASK039 auditó el backend y TASK039B aplicó las
correcciones autorizadas; la revisión es metodológica, no humana externa.

## Guía para Angular (sin implementar UI)

Buscar y seleccionar cliente; cargar detalle e historial paginado. Cambios del
slider/formulario disparan preview con debounce (por ejemplo 250–400 ms), distinción
de entradas repetidas y cancelación/descartado de respuestas obsoletas con switchMap
o secuencia de petición. Cancelar en cliente no garantiza cancelar el trabajo del
servidor. Mostrar carga/error/503 y datos nulos como desconocidos, no cero. Guardar
explícitamente con POST /simulations y refrescar historial. No enviar los importes
del preview ni tratarlo como una cotización bloqueada. No generar cliente TypeScript.
