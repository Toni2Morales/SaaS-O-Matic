"""Límites técnicos comunes de las consultas, sin dependencias de framework."""

DEFAULT_PAGE_LIMIT = 20
MAX_PAGE_LIMIT = 100
MAX_SEARCH_LENGTH = 255


class InvalidQueryData(ValueError):
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(message)


def validate_pagination(limit: int, offset: int) -> None:
    if type(limit) is not int or not 1 <= limit <= MAX_PAGE_LIMIT:
        raise InvalidQueryData("limit", f"Debe ser un entero entre 1 y {MAX_PAGE_LIMIT}.")
    if type(offset) is not int or offset < 0:
        raise InvalidQueryData("offset", "Debe ser un entero no negativo.")
