"""Tabla de tramos aprobada para el cálculo de precios por usuarios."""

from __future__ import annotations

from decimal import Decimal
from typing import Final

from saas_o_matic.domain.pricing.value_objects import PricingBand, PricingSchedule

APPROVED_USER_PRICING_SCHEDULE: Final[PricingSchedule] = PricingSchedule(
    bands=(
        PricingBand(lower_bound=1, upper_bound=10, price_per_user_eur=Decimal("10.00")),
        PricingBand(lower_bound=11, upper_bound=50, price_per_user_eur=Decimal("8.00")),
        PricingBand(lower_bound=51, upper_bound=None, price_per_user_eur=Decimal("5.00")),
    )
)
