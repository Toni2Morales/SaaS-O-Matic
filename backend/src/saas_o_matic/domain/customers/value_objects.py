"""Objetos de valor del dominio de clientes."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import StrEnum

from saas_o_matic.domain.customers.errors import (
    InvalidCountry,
    InvalidLegalName,
    InvalidPlan,
    InvalidTaxId,
)

LEGAL_NAME_MIN_LENGTH = 1
LEGAL_NAME_MAX_LENGTH = 255


class CountryCode(StrEnum):
    """Códigos ISO 3166-1 alfa-2 admitidos por la primera versión."""

    ES = "ES"
    PT = "PT"
    FR = "FR"
    DE = "DE"
    IT = "IT"
    NL = "NL"

    @classmethod
    def parse(cls, raw: str) -> CountryCode:
        """Convierte un código de país y rechaza los no soportados."""

        try:
            return cls(raw)
        except ValueError as exc:
            raise InvalidCountry("País no soportado.") from exc


class PlanCode(StrEnum):
    """Catálogo de planes aprobado para el MVP."""

    STANDARD = "standard"

    @classmethod
    def parse(cls, raw: str) -> PlanCode:
        """Convierte un código de plan y rechaza los no aprobados."""

        try:
            return cls(raw)
        except ValueError as exc:
            raise InvalidPlan("Plan no soportado. El único plan válido es 'standard'.") from exc


def normalize_legal_name(raw: str) -> str:
    """Recorta la razón social y valida su contenido y longitud."""

    normalized = raw.strip()
    if len(normalized) < LEGAL_NAME_MIN_LENGTH:
        raise InvalidLegalName("La razón social no puede estar vacía.")
    if len(normalized) > LEGAL_NAME_MAX_LENGTH:
        raise InvalidLegalName(
            f"La razón social no puede superar los {LEGAL_NAME_MAX_LENGTH} caracteres."
        )
    return normalized


class TaxIdKind(StrEnum):
    """Tipos de identificación fiscal española admitidos."""

    DNI = "DNI"
    NIE = "NIE"
    CIF = "CIF"


_DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"
_CIF_CONTROL_LETTERS = "JABCDEFGHI"
_CIF_DIGIT_ONLY = frozenset("ABEH")
_CIF_LETTER_ONLY = frozenset("KPQS")
_NIE_PREFIXES = {"X": "0", "Y": "1", "Z": "2"}


def normalize_tax_id(raw: str) -> str:
    """Elimina espacios y guiones y convierte el identificador a mayúsculas."""

    return re.sub(r"[\s-]+", "", raw).upper()


@dataclass(frozen=True, slots=True)
class SpanishTaxId:
    """Identificador fiscal español normalizado y validado."""

    value: str
    kind: TaxIdKind

    @classmethod
    def parse(cls, raw: str) -> SpanishTaxId:
        """Normaliza y valida un DNI/NIF, NIE o CIF/NIF de entidad."""

        normalized = normalize_tax_id(raw)
        if not normalized:
            raise InvalidTaxId("El identificador fiscal no puede estar vacío.")
        if len(normalized) != 9:
            raise InvalidTaxId("El identificador fiscal debe tener 9 caracteres.")

        if _is_dni(normalized):
            return cls(value=normalized, kind=TaxIdKind.DNI)
        if _is_nie(normalized):
            return cls(value=normalized, kind=TaxIdKind.NIE)
        if _is_cif(normalized):
            return cls(value=normalized, kind=TaxIdKind.CIF)

        raise InvalidTaxId("El identificador fiscal no es válido.")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class GenericTaxId:
    """Identificador internacional; validación de forma, no fiscal oficial."""

    value: str

    @classmethod
    def parse(cls, raw: str) -> GenericTaxId:
        """Preserva puntuación y rechaza controles antes de normalizar espacios."""

        if any(unicodedata.category(char) in {"Cc", "Cf", "Cs"} for char in raw):
            raise InvalidTaxId("El identificador fiscal no admite caracteres de control.")
        normalized = " ".join(raw.split()).upper()
        if not 1 <= len(normalized) <= 64:
            raise InvalidTaxId("El identificador fiscal debe tener entre 1 y 64 caracteres.")
        return cls(normalized)


TaxId = SpanishTaxId | GenericTaxId


def parse_tax_id(raw: str, country: CountryCode) -> TaxId:
    """Selecciona la validación española o genérica según el país."""

    return SpanishTaxId.parse(raw) if country == CountryCode.ES else GenericTaxId.parse(raw)


def _is_dni(value: str) -> bool:
    if re.fullmatch(r"[0-9]{8}[A-Z]", value) is None:
        return False

    number = int(value[:8])
    return value[8] == _DNI_LETTERS[number % 23]


def _is_nie(value: str) -> bool:
    match = re.fullmatch(r"([XYZ])([0-9]{7})([A-Z])", value)
    if match is None:
        return False

    number = int(_NIE_PREFIXES[match.group(1)] + match.group(2))
    return match.group(3) == _DNI_LETTERS[number % 23]


def _is_cif(value: str) -> bool:
    match = re.fullmatch(r"([A-HJ-NP-SUVW])([0-9]{7})([0-9A-Z])", value)
    if match is None:
        return False

    first_letter = match.group(1)
    digits = match.group(2)
    control = match.group(3)

    even_sum = sum(int(digits[index]) for index in (1, 3, 5))
    odd_sum = sum(sum(divmod(int(digits[index]) * 2, 10)) for index in (0, 2, 4, 6))
    control_digit = (10 - ((even_sum + odd_sum) % 10)) % 10
    control_letter = _CIF_CONTROL_LETTERS[control_digit]

    if first_letter in _CIF_DIGIT_ONLY:
        return control == str(control_digit)
    if first_letter in _CIF_LETTER_ONLY:
        return control == control_letter
    return control in {str(control_digit), control_letter}
