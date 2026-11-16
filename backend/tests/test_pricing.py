"""Pruebas del motor de precios progresivos por usuarios."""

from __future__ import annotations

import inspect
from dataclasses import FrozenInstanceError
from decimal import Decimal, localcontext
from itertools import pairwise
from typing import Any, cast

import pytest

from saas_o_matic.domain.pricing import (
    APPROVED_USER_PRICING_SCHEDULE,
    InvalidPricingSchedule,
    InvalidUserCount,
    PricingBand,
    PricingSchedule,
    calculate_user_subtotal,
)


@pytest.mark.parametrize(
    ("user_count", "expected"),
    [
        (1, Decimal("10.00")),
        (10, Decimal("100.00")),
        (11, Decimal("108.00")),
        (50, Decimal("420.00")),
        (51, Decimal("425.00")),
        (100, Decimal("670.00")),
    ],
)
def test_calculate_user_subtotal_acceptance_examples(
    user_count: int,
    expected: Decimal,
) -> None:
    """Los seis ejemplos aprobados producen exactamente el subtotal esperado."""

    assert calculate_user_subtotal(user_count) == expected


@pytest.mark.parametrize(
    ("user_count", "expected"),
    [
        (9, Decimal("90.00")),
        (10, Decimal("100.00")),
        (11, Decimal("108.00")),
        (49, Decimal("412.00")),
        (50, Decimal("420.00")),
        (51, Decimal("425.00")),
        (52, Decimal("430.00")),
        (100, Decimal("670.00")),
        (101, Decimal("675.00")),
        (1000, Decimal("5170.00")),
    ],
)
def test_calculate_user_subtotal_band_boundaries(
    user_count: int,
    expected: Decimal,
) -> None:
    """Los límites de tramo solo cobran las unidades de cada tramo."""

    assert calculate_user_subtotal(user_count) == expected


def test_calculate_user_subtotal_returns_decimal() -> None:
    """El resultado es Decimal y no un float."""

    result = calculate_user_subtotal(11)

    assert isinstance(result, Decimal)
    assert not isinstance(result, float)


def test_calculate_user_subtotal_is_monotonic() -> None:
    """Añadir usuarios nunca reduce el subtotal."""

    counts = [1, 9, 10, 11, 49, 50, 51, 52, 100, 101, 1000]
    subtotals = [calculate_user_subtotal(count) for count in counts]

    assert subtotals == sorted(subtotals)
    assert all(left < right for left, right in pairwise(subtotals))


def test_calculate_user_subtotal_band_increments() -> None:
    """Cruzar un tramo aplica únicamente el precio del usuario adicional."""

    assert calculate_user_subtotal(11) - calculate_user_subtotal(10) == Decimal("8.00")
    assert calculate_user_subtotal(51) - calculate_user_subtotal(50) == Decimal("5.00")
    assert calculate_user_subtotal(1001) - calculate_user_subtotal(1000) == Decimal("5.00")


def test_calculate_user_subtotal_supports_large_counts_exactly() -> None:
    """No hay máximo comercial y el cálculo conserva la exactitud."""

    result = calculate_user_subtotal(10**30)
    expected = Decimal(5 * 10**30 + 170)

    assert result == expected


def test_calculate_user_subtotal_supports_counts_beyond_int_str_limit() -> None:
    """La precisión no depende de convertir el entero completo a cadena decimal."""

    user_count = 10**4300
    expected = Decimal(5 * user_count + 170)

    try:
        result = calculate_user_subtotal(user_count)
    except ValueError as exc:
        pytest.fail(f"El cálculo no debe depender de int→str: {exc}")

    assert isinstance(result, Decimal)
    assert result == expected


def test_calculate_user_subtotal_isolates_decimal_context() -> None:
    """Una precisión externa baja no altera el resultado ni el contexto del llamador."""

    with localcontext() as context:
        context.prec = 2

        result = calculate_user_subtotal(100)

        assert result == Decimal("670.00")
        assert context.prec == 2


def test_calculate_user_subtotal_has_no_plan_parameter() -> None:
    """El cálculo no recibe el plan ni depende del catálogo."""

    assert tuple(inspect.signature(calculate_user_subtotal).parameters) == ("user_count",)


@pytest.mark.parametrize(
    "user_count",
    [
        0,
        -1,
        -100,
        1.0,
        1.5,
        float("inf"),
        float("nan"),
        Decimal("1"),
        Decimal("1.0"),
        "1",
        "",
        None,
        True,
        False,
        object(),
        [1],
        (1,),
    ],
)
def test_calculate_user_subtotal_rejects_invalid_counts(user_count: object) -> None:
    """Solo se aceptan enteros positivos, sin coerciones ni truncamientos."""

    with pytest.raises(InvalidUserCount) as error:
        calculate_user_subtotal(cast(Any, user_count))

    assert error.value.value is user_count


def test_approved_schedule_contains_the_approved_bands() -> None:
    """La tabla aprobada conserva los tres tramos y sus precios."""

    bands = APPROVED_USER_PRICING_SCHEDULE.bands

    assert len(bands) == 3
    assert bands[0].lower_bound == 1
    assert bands[0].upper_bound == 10
    assert bands[0].price_per_user_eur == Decimal("10.00")
    assert bands[1].lower_bound == 11
    assert bands[1].upper_bound == 50
    assert bands[1].price_per_user_eur == Decimal("8.00")
    assert bands[2].lower_bound == 51
    assert bands[2].upper_bound is None
    assert bands[2].price_per_user_eur == Decimal("5.00")


def test_valid_schedule_is_accepted() -> None:
    """Una tabla contigua con último tramo abierto es válida."""

    schedule = PricingSchedule(
        bands=(
            PricingBand(1, 10, Decimal("10.00")),
            PricingBand(11, None, Decimal("8.00")),
        )
    )

    assert schedule.bands[0].upper_bound == 10
    assert schedule.bands[1].upper_bound is None


@pytest.mark.parametrize(
    "bands",
    [
        (),
        (PricingBand(2, 10, Decimal("10.00")), PricingBand(11, None, Decimal("8.00"))),
        (PricingBand(1, 10, Decimal("10.00")), PricingBand(12, None, Decimal("8.00"))),
        (PricingBand(1, 10, Decimal("10.00")), PricingBand(10, None, Decimal("8.00"))),
        (PricingBand(1, None, Decimal("10.00")), PricingBand(11, None, Decimal("8.00"))),
        (PricingBand(1, 10, Decimal("10.00")), PricingBand(11, 50, Decimal("8.00"))),
    ],
)
def test_invalid_schedule_is_rejected(bands: tuple[PricingBand, ...]) -> None:
    """La tabla rechaza huecos, solapamientos, inicio incorrecto y cierre incorrecto."""

    with pytest.raises(InvalidPricingSchedule):
        PricingSchedule(bands=bands)


def test_schedule_rejects_non_tuple_bands() -> None:
    """La tabla exige una tupla inmutable."""

    with pytest.raises(InvalidPricingSchedule):
        PricingSchedule(bands=cast(Any, [PricingBand(1, None, Decimal("10.00"))]))


def test_schedule_rejects_non_band_items() -> None:
    """La tabla solo admite instancias de PricingBand."""

    with pytest.raises(InvalidPricingSchedule):
        PricingSchedule(bands=cast(Any, (PricingBand(1, None, Decimal("10.00")), "x")))


@pytest.mark.parametrize(
    "band_args",
    [
        (0, 10, Decimal("10.00")),
        (-1, 10, Decimal("10.00")),
        (cast(Any, True), 10, Decimal("10.00")),
        (cast(Any, 1.0), 10, Decimal("10.00")),
        (cast(Any, Decimal("1")), 10, Decimal("10.00")),
        (1, 0, Decimal("10.00")),
        (1, cast(Any, True), Decimal("10.00")),
        (1, cast(Any, 10.0), Decimal("10.00")),
        (1, 10, Decimal("0")),
        (1, 10, Decimal("-1")),
        (1, 10, Decimal("NaN")),
        (1, 10, Decimal("Infinity")),
        (1, 10, cast(Any, 10.0)),
        (1, 10, cast(Any, 10)),
        (1, 10, cast(Any, "10")),
    ],
)
def test_invalid_band_is_rejected(band_args: tuple[object, object, object]) -> None:
    """Cada tramo valida límites, tipos y precio positivo finito."""

    lower_bound, upper_bound, price = band_args

    with pytest.raises(InvalidPricingSchedule):
        PricingBand(
            lower_bound=cast(Any, lower_bound),
            upper_bound=cast(Any, upper_bound),
            price_per_user_eur=cast(Any, price),
        )


def test_pricing_band_is_immutable() -> None:
    """Un tramo no puede modificarse después de construirse."""

    band = PricingBand(1, 10, Decimal("10.00"))

    with pytest.raises(FrozenInstanceError):
        cast(Any, band).lower_bound = 2


def test_pricing_schedule_is_immutable() -> None:
    """La tabla y su tupla de tramos no pueden modificarse."""

    schedule = PricingSchedule(bands=(PricingBand(1, None, Decimal("10.00")),))

    with pytest.raises(FrozenInstanceError):
        cast(Any, schedule).bands = ()

    with pytest.raises(TypeError):
        cast(Any, schedule.bands)[0] = PricingBand(1, 10, Decimal("10.00"))
