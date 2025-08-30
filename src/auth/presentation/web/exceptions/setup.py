from typing import TYPE_CHECKING, cast

from fastapi import FastAPI

from auth.application.common.application_error import ApplicationError
from auth.domain.shared.domain_error import DomainError
from auth.infrastructure.errors import InfrastructureError
from auth.presentation.web.exceptions.handlers import (
    application_error_handler,
    domain_error_handler,
    internal_error_handler,
)

if TYPE_CHECKING:
    from starlette.types import HTTPExceptionHandler


def setup_application_error_handler(application: FastAPI) -> None:
    """Регистрация обработчиков исключений прикладного уровня для FastAPI."""
    application.add_exception_handler(
        ApplicationError, cast("HTTPExceptionHandler", application_error_handler)
    )


def setup_domain_error_handler(application: FastAPI) -> None:
    """Регистрация обработчиков исключений предметного (доменного) уровня для FastAPI."""
    application.add_exception_handler(
        DomainError, cast("HTTPExceptionHandler", domain_error_handler)
    )


def setup_internal_error_handler(application: FastAPI) -> None:
    """
    Регистрация обработчиков исключений инфраструктурного и
    базового уровня для FastAPI.
    """
    application.add_exception_handler(
        InfrastructureError, cast("HTTPExceptionHandler", internal_error_handler)
    )
    application.add_exception_handler(
        Exception, cast("HTTPExceptionHandler", internal_error_handler)
    )
