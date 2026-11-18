"""Parámetros paginados HTTP compartidos."""

from pydantic import BaseModel, Field

from saas_o_matic.application.pagination import DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT


class PageParameters(BaseModel):
    limit: int = Field(default=DEFAULT_PAGE_LIMIT, ge=1, le=MAX_PAGE_LIMIT)
    offset: int = Field(default=0, ge=0)
