from dataclasses import asdict
from typing import Final

from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from auth.application.common.application_error import AppErrorType, ApplicationError
from auth.domain.shared.domain_error import DomainError, DomainErrorType
from auth.infrastructure.errors import InfrastructureError
from auth.presentation.web.schemas.base import ErrorResponse

STATUS_MAP: Final[dict[AppErrorType | DomainErrorType, int]] = {
    AppErrorType.UNAUTHORIZED: HTTP_401_UNAUTHORIZED,
    AppErrorType.FORBIDDEN: HTTP_403_FORBIDDEN,
    AppErrorType.NOT_FOUND: HTTP_404_NOT_FOUND,
    DomainErrorType.VALIDATION: HTTP_422_UNPROCESSABLE_ENTITY,
    DomainErrorType.FORBIDDEN: HTTP_403_FORBIDDEN,
    AppErrorType.VALIDATION: HTTP_422_UNPROCESSABLE_ENTITY,
    AppErrorType.CONFLICT: HTTP_409_CONFLICT,
}


def application_error_handler(_: Request, exception: ApplicationError) -> Response:
    """Обработчик прикладных исключений."""
    status_code = STATUS_MAP[exception.type]
    error_response = ErrorResponse(status_code, exception.message)
    return JSONResponse(status_code=status_code, content=asdict(error_response))


def domain_error_handler(_: Request, exception: DomainError) -> Response:
    """Обработчик доменных исключений."""
    status_code = STATUS_MAP[exception.type]
    error_response = ErrorResponse(status_code, exception.message)
    return JSONResponse(status_code=status_code, content=asdict(error_response))


def internal_error_handler(
    _: Request, exception: InfrastructureError | Exception
) -> Response:
    """Обработчик инфраструктурных исключений."""
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    message = exception.message if hasattr(exception, "message") else str(exception)
    error_response = ErrorResponse(status_code, message)
    return JSONResponse(status_code=status_code, content=asdict(error_response))
