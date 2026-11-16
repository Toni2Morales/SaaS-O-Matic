"""Pruebas de los identificadores fiscales españoles."""

import pytest

from saas_o_matic.domain.customers.errors import InvalidTaxId
from saas_o_matic.domain.customers.value_objects import (
    SpanishTaxId,
    TaxIdKind,
    normalize_tax_id,
)


@pytest.mark.parametrize(
    ("raw", "normalized", "kind"),
    [
        ("12345678Z", "12345678Z", TaxIdKind.DNI),
        ("12345678-z", "12345678Z", TaxIdKind.DNI),
        ("X1234567L", "X1234567L", TaxIdKind.NIE),
        ("x-1234567-l", "X1234567L", TaxIdKind.NIE),
        ("Y1234567X", "Y1234567X", TaxIdKind.NIE),
        ("Z1234567R", "Z1234567R", TaxIdKind.NIE),
        ("B12345674", "B12345674", TaxIdKind.CIF),
        ("P1234567D", "P1234567D", TaxIdKind.CIF),
        ("J12345674", "J12345674", TaxIdKind.CIF),
        ("J1234567D", "J1234567D", TaxIdKind.CIF),
        ("K1234567D", "K1234567D", TaxIdKind.CIF),
    ],
)
def test_valid_spanish_tax_ids_are_normalized_and_classified(
    raw: str,
    normalized: str,
    kind: TaxIdKind,
) -> None:
    """Los tres tipos válidos se normalizan y clasifican correctamente."""

    parsed = SpanishTaxId.parse(raw)

    assert parsed.value == normalized
    assert parsed.kind is kind
    assert str(parsed) == normalized


@pytest.mark.parametrize(
    "raw",
    [
        "12345678A",
        "X1234567A",
        "B12345678",
        "P12345674",
        "I1234567D",
        "1234",
        "123456789",
        "ABCDEFGHI",
    ],
)
def test_invalid_spanish_tax_ids_are_rejected(raw: str) -> None:
    """Se rechazan controles incorrectos, prefijos y longitudes inválidas."""

    with pytest.raises(InvalidTaxId):
        SpanishTaxId.parse(raw)


@pytest.mark.parametrize("raw", ["", "   ", "- -"])
def test_empty_tax_ids_are_rejected(raw: str) -> None:
    """Un identificador vacío o compuesto solo por separadores no es válido."""

    with pytest.raises(InvalidTaxId):
        SpanishTaxId.parse(raw)


def test_normalize_tax_id_removes_spaces_and_hyphens() -> None:
    """La normalización elimina espacios y guiones y aplica mayúsculas."""

    assert normalize_tax_id(" 12-345 678-z ") == "12345678Z"
    assert normalize_tax_id("x-1234567-l") == "X1234567L"
