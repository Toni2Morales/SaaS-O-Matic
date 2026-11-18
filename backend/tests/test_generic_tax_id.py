"""Validación internacional genérica sin algoritmos fiscales oficiales."""

import pytest

from saas_o_matic.domain.customers.errors import InvalidTaxId
from saas_o_matic.domain.customers.value_objects import GenericTaxId


@pytest.mark.parametrize(
    ("raw", "expected"),
    [(" a ", "A"), ("x" * 64, "X" * 64), (" é-1 /\u00a0  a. ", "É-1 / A.")],
)
def test_generic_normalization_preserves_significant_characters(raw: str, expected: str) -> None:
    assert GenericTaxId.parse(raw).value == expected


@pytest.mark.parametrize("raw", ["", "  ", "x" * 65, "a\t", "a\n", "a\x7f", "a\u200e", "a\ud800"])
def test_generic_invalid_values(raw: str) -> None:
    with pytest.raises(InvalidTaxId):
        GenericTaxId.parse(raw)
