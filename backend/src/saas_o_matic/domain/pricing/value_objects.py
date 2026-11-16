"""Objetos de valor del dominio de precios."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from saas_o_matic.domain.pricing.errors import InvalidPricingSchedule


def _is_int(value: object) -> bool:
    """Comprueba que un valor sea un entero y no un booleano."""

    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(frozen=True, slots=True)
class PricingBand:
    """Tramo inmutable de usuarios con un precio unitario en EUR."""

    lower_bound: int
    upper_bound: int | None
    price_per_user_eur: Decimal

    def __post_init__(self) -> None:
        """Valida los límites y el precio del tramo."""

        if not _is_int(self.lower_bound) or self.lower_bound < 1:
            raise InvalidPricingSchedule(
                "El límite inferior debe ser un entero mayor o igual que 1."
            )

        if self.upper_bound is not None:
            if not _is_int(self.upper_bound):
                raise InvalidPricingSchedule("El límite superior debe ser un entero o None.")
            if self.upper_bound < self.lower_bound:
                raise InvalidPricingSchedule(
                    "El límite superior no puede ser menor que el límite inferior."
                )

        if not isinstance(self.price_per_user_eur, Decimal):
            raise InvalidPricingSchedule("El precio por usuario debe ser un Decimal.")
        if not self.price_per_user_eur.is_finite() or self.price_per_user_eur <= 0:
            raise InvalidPricingSchedule(
                "El precio por usuario debe ser un Decimal finito y positivo."
            )


@dataclass(frozen=True, slots=True)
class PricingSchedule:
    """Tabla inmutable y contigua de tramos progresivos."""

    bands: tuple[PricingBand, ...]

    def __post_init__(self) -> None:
        """Valida que los tramos cubran todos los usuarios sin huecos ni solapamientos."""

        if not isinstance(self.bands, tuple):
            raise InvalidPricingSchedule("Los tramos deben ser una tupla inmutable.")
        if not self.bands:
            raise InvalidPricingSchedule("La tabla de tramos no puede estar vacía.")
        if not all(isinstance(band, PricingBand) for band in self.bands):
            raise InvalidPricingSchedule("Todos los tramos deben ser PricingBand.")

        expected_lower = 1
        last_index = len(self.bands) - 1

        for index, band in enumerate(self.bands):
            if band.lower_bound != expected_lower:
                raise InvalidPricingSchedule(
                    "Los tramos deben ser contiguos, sin huecos ni solapamientos, y empezar en 1."
                )

            if band.upper_bound is None:
                if index != last_index:
                    raise InvalidPricingSchedule("Solo el último tramo puede estar abierto.")
                return

            expected_lower = band.upper_bound + 1

        raise InvalidPricingSchedule("El último tramo debe estar abierto.")
