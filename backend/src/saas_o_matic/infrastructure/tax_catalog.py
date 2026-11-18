"""Única tabla fiscal versionada; fuentes verificadas el 17/11/2026."""

from datetime import date
from decimal import Decimal

from saas_o_matic.domain.customers.value_objects import CountryCode
from saas_o_matic.domain.simulations.calculation import TaxCatalog, TaxRule

VERSION = "general-vat-2026-11-17-v1"


def configured_tax_catalog() -> TaxCatalog:
    """Configuración explícita sustituible por inyección, no servicio fiscal externo."""

    entries = (
        (
            CountryCode.ES,
            "0.21",
            "https://sede.agenciatributaria.gob.es/Sede/iva/calculo-iva-repercutido-clientes/tipos-impositivos-iva.html",
            "Península y Baleares",
        ),
        (
            CountryCode.PT,
            "0.23",
            "https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/civa_rep/Pages/iva18.aspx",
            "Portugal continental",
        ),
        (
            CountryCode.FR,
            "0.20",
            "https://www.economie.gouv.fr/particuliers/tva-taux-quotidien",
            "Francia metropolitana",
        ),
        (
            CountryCode.DE,
            "0.19",
            "https://www.gesetze-im-internet.de/ustg_1980/__12.html",
            "Ámbito general IVA alemán",
        ),
        (
            CountryCode.IT,
            "0.22",
            "https://www.fiscooggi.it/portale/-/iva-agevolata-oppure-ordinaria-decide-la-classificazione-doganale",
            "Ámbito general IVA italiano",
        ),
        (
            CountryCode.NL,
            "0.21",
            "https://www.belastingdienst.nl/wps/wcm/connect/bldcontenten/belastingdienst/business/vat/vat_in_the_netherlands/calculating_vat/vat_tariffs",
            "Países Bajos europeos",
        ),
    )
    return TaxCatalog(
        tuple(
            TaxRule(country, Decimal(rate), source, VERSION, date(2026, 11, 17), territory)
            for country, rate, source, territory in entries
        )
    )
