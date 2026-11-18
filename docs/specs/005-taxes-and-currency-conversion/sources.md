# Fuentes oficiales — consulta 2026-11-17

## IVA

[Comisión Europea / Your Europe](https://europa.eu/youreurope/business/taxation/vat/vat-rules-rates/index_en.htm):
tabla de tipos generales ES21/PT23/FR20/DE19/IT22/NL21; página «Last checked 13/07/2026».
Contraste nacional efectivo:

| País | Fuente consultada | Tipo | Ámbito simplificado | Entrada en vigor |
| --- | --- | --- | --- | --- |
| ES | [AEAT](https://sede.agenciatributaria.gob.es/Sede/iva/calculo-iva-repercutido-clientes/tipos-impositivos-iva.html), actualizada 13/10/2026 | 21% | Península/Baleares, no Canarias/Ceuta/Melilla | No verificada en esta página; NULL |
| PT | [AT, CIVA art.18](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/civa_rep/Pages/iva18.aspx), apartado 1.c; distingue regiones autónomas | 23% | Portugal continental, no Madeira/Azores | Cita Lei 55-A/2010; no inferir fecha efectiva, NULL |
| FR | [Ministère de l'Économie](https://www.economie.gouv.fr/particuliers/tva-taux-quotidien), 11/12/2025 | 20% | Francia metropolitana; sin regímenes territoriales especiales | No verificada; NULL |
| DE | [UStG §12.1, Ministerio de Justicia](https://www.gesetze-im-internet.de/ustg_1980/__12.html) | 19% | Ámbito general alemán, no territorios excluidos | No verificada; NULL |
| IT | [FiscoOggi, Agenzia delle Entrate](https://www.fiscooggi.it/portale/-/iva-agevolata-oppure-ordinaria-decide-la-classificazione-doganale), 11/11/2026: «aliquota ordinaria del 22 per cento» | 22% | Ámbito general italiano, sin territorios especiales | No verificada; NULL |
| NL | [Belastingdienst VAT tariffs](https://www.belastingdienst.nl/wps/wcm/connect/bldcontenten/belastingdienst/business/vat/vat_in_the_netherlands/calculating_vat/vat_tariffs) y [portal gubernamental, publicado por Belastingdienst](https://business.gov.nl/finance-and-taxes/vat/vat-rates-and-exemptions/) | 21% | Países Bajos europeos, sin territorios especiales | No verificada; NULL |

No confundir fecha de publicación/consulta con entrada en vigor. La aplicación no
recibe región ni situación fiscal: aplica siempre el general del país como simplificación
aprobada, sin exenciones, reducidos, inversión del sujeto pasivo ni tratamiento B2B real.
La fecha verificada es una observación puntual, no mantenimiento fiscal automático.

Incidencias reales: buscador web no disponible; varias rutas antiguas de impots.gouv.fr,
agenziaentrate.gov.it y Belastingdienst devolvieron 404. Se siguieron fuentes oficiales
alternativas/enlaces publicados. No se tomaron esas rutas fallidas como evidencia.

## Frankfurter

[Documentación](https://frankfurter.dev/) y [licencia/términos](https://frankfurter.dev/license/).
API v2 actual; v1 deprecada pero disponible. Sin clave/cuenta, uso comercial gratuito,
almacenamiento y caché permitidos; límites antiabuso sin cuotas diarias/mensuales.
Software/docs MIT. Datos de referencia sin garantía, revisables o ausentes; respetar
condiciones de fuentes subyacentes. No se encontró obligación general de atribución
específica para el feed mezclado; se conserva y muestra source=frankfurter por trazabilidad.

Endpoint elegido `/v2/rate/EUR/USD` (GBP análogo), JSON objeto con date/base/quote/rate.
Ejemplo real de consulta: `{"date":"2026-11-17","base":"EUR","quote":"USD","rate":1.1014}`.
Endpoint conjunto consultado devolvió GBP .8339 y USD 1.1014 con fecha 2026-11-17.
Son observaciones de la consulta, no tasas fijas de la aplicación.
EUR/USD/GBP disponibles y convención EUR→destino verificada. Feed mezclado entre
fuentes; referencias una o varias veces al día, no mercado continuo. Fines de semana,
festivos y revisiones posibles. No usar como asesoramiento fiscal ni liquidación real.
