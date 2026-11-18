# SPEC-005 — Impuestos y conversión de divisas

> TASK038: CalculateSimulation comparte validación/cliente/pricing/MonthlyEstimator
> entre preview y guardado, sin cambiar impuestos/FX ni catálogo. Historial lee solo
> snapshots, incluidos NULL antiguos; preview no escribe ni añade id/created_at.
> Contratos de lectura y frontend en [SPEC-006](../006-customer-queries-and-preview/spec.md).

Estado: implementada localmente e integrada en la suite TASK039B de 579 pruebas;
auditada en TASK039 y corregida en TASK039B; sin publicación ni revisión humana
externa.
Fuentes: instrucción del propietario, [requisitos](../../requirements/functional-requirements.md),
ADR 0001/0002 y [fuentes verificadas](sources.md). Consulta: 2026-11-17.

## Reglas y decisiones

Q-05/Q-22: catálogo versionado configurable por inyección, único en infraestructura:
ES .21, PT .23, FR .20, DE .19, IT .22, NL .21, contrastados oficialmente.
Cada regla contiene país, fracción Decimal, fuente, versión, fecha de consulta,
ámbito y fecha inicial solo si está verificada (NULL si no). Sin tasa por defecto;
catálogo debe cubrir exactamente los seis países. Estimación comercial simplificada:
sin exenciones, reducidos, inversión del sujeto pasivo, regímenes B2B ni territorios
especiales (ES península/Baleares; PT continental; FR metropolitana; DE/IT/NL
ámbito general IVA, sin territorios excluidos). No facturación ni asesoría fiscal.

Base = subtotal del motor existente. Impuesto = base × tasa, ROUND_HALF_UP a .01.
Total EUR = base + impuesto. Consumos y standard no generan cargos.
Q-16: convertir el total EUR con impuestos; persistir también resultado convertido.
Q-08: importes con dos decimales; tasas como texto exacto con precisión original.
Q-17/SIM-P14: snapshot fiscal y FX inmutable, fuente/fecha de consulta/versión,
fecha efectiva conocida y publicación FX cuando aplica. No recalcular históricos.

Q-06/Q-07/Q-23: único proveedor Frankfurter v2, endpoint
`https://api.frankfurter.dev/v2/rate/EUR/{USD|GBP}`. Tipos de referencia mezclados,
no cotizaciones continuas ni tipos oficiales de una sola institución. Convención:
1 EUR = X destino. Conversión = total EUR × tasa, ROUND_HALF_UP a .01.
EUR es identidad 1, source identity, reference_date NULL, sin llamada externa.
USD/GBP requieren tasa finita positiva, base y destino coincidentes y fecha válida
no futura. JSON con parse_float/parse_int Decimal; rechazar constantes no finitas.

Límites técnicos de plausibilidad, no comerciales: `0.000001 <= tasa <= 1000000`
y máximo 32 dígitos significativos. EUR/USD y EUR/GBP se mueven alrededor de
0,8–1,2; los límites dejan seis órdenes de magnitud de holgura y una precisión muy
superior a la publicada por el proveedor. La respuesta externa sigue limitada a
64 KiB. Una tasa fuera de rango se rechaza antes de la caché y se traduce al
mecanismo externo existente (`503 application/problem+json`); no se redondea para
hacerla válida, no se cachea y no se convierte en un `500`. Los snapshots históricos
fuera de rango se consideran datos corruptos y siguen la política controlada de
A39-05, sin ocultación ni reparación automática.

## Contrato definitivo

POST /simulations mantiene customer_id, user_count, storage_gb y api_calls_per_month
obligatorios. display_currency admite EUR/USD/GBP, EUR si se omite. Forbid permanece:
no tasas/país alternativo/importes ni periodicidad del usuario.
Respuesta 201 conserva todos los campos anteriores y añade:

- tax_country, tax_rate, tax_source, tax_catalog_version, tax_territory;
- tax_verified_on (fecha de consulta), tax_effective_from (fecha o NULL);
- tax_amount_eur, total_eur, display_currency, exchange_rate, converted_total;
- exchange_rate_date (fecha de referencia o NULL identidad), exchange_rate_obtained_at
  (UTC), exchange_rate_source (frankfurter/identity).

Cantidades y tasas siempre cadenas, fechas ISO. 404 cliente ausente, 422 inválido,
503 proveedor sin tasa válida; 500 configuración/error interno. problem+json; sin Location.
El contrato TASK036 sigue siendo válido: EUR por defecto. No rutas públicas nuevas.

## Arquitectura y cálculo reutilizable

Dominio puro: reglas, catálogo validado, quote y cálculo monetario inmutables.
Aplicación: MonthlyEstimator reutilizable por preview futuro; puerto estructural
ExchangeRateProvider definido en aplicación, sin que infraestructura lo importe.
Infraestructura implementa la firma usando tipos de dominio, urllib y caché.
HTTPX es solo dev: no usarlo como dependencia de ejecución ni añadir paquetes.
Bootstrap compone catálogo y una instancia compartida del adaptador/caché por proceso.
urllib cierra cada respuesta mediante context manager; no cliente persistente que cerrar.
Consultar país del cliente mediante puerto; finalizar transacción de lectura antes de
red externa. Calcular todo antes de insertar; FK y rollback se conservan.

## Caché y errores

Memoria por par EUR/destino, TTL 86400 segundos monotónicos desde respuesta válida.
Timeout 5 s; lock sencillo evita consultas duplicadas concurrentes dentro del proceso.
No guardar errores, no servir expirados ni usar respaldo. Fecha de referencia anterior
por festivo/fin de semana no implica caché vencida; TTL usa obtención, no publicación.
Fechas publicación, obtención y creación persistidas; expiración solo operativa.
Sin reintentos automáticos ni SLA; cachés independientes por proceso, se pierden al reiniciar.
Errores HTTP/red/timeout/JSON/esquema: 503 sin detalles internos ni registros parciales.
Límite de lectura externa 64 KiB; validación estricta de monedas, tasa y fecha.

## Persistencia y migración

Nueva 0004, sin tocar 0001–0003. Añadir `calculation_snapshot` TEXT nullable:
JSON versionado de todos los campos anteriores, con dinero/tasas como cadenas,
fechas ISO y NULL solo para fechas desconocidas. Es un snapshot autocontenido,
no un documento recibido del proveedor ni campos REAL. Evita duplicar columnas
y permite reconstruir el cálculo con el subtotal existente. Validar al reconstruir.
Históricos: snapshot NULL y todos sus datos intactos; no backfill fiscal/FX.
Nuevas simulaciones por aplicación siempre snapshot completo. Downgrade preflight
bloquea si existe algún snapshot, antes de DDL; ciclo con históricos NULL permitido.

## Precisión y aceptación

Contextos locales explícitos, precisión calculada y traps controlados sin mutar al
llamador. Redondear solo impuesto/conversión; subtotal y total exactos. Resolver
H-03 acotadamente aislando traps del motor de precios, conservando enormes.
H-01 sigue probado; H-06/H-07 residuales documentados.
Probar tablas fiscales, fracciones de céntimo, FX/errores/caché con dobles, EUR offline,
contrato, TEXT físico/nueva sesión, metadatos e historia, migraciones/downgrade.
Suite independiente de Internet; smoke real separado. Sin TASK038 ni publicación.
