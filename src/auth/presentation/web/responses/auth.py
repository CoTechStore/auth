from typing import Any, Final

from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from auth.presentation.web.schemas import responses as response

LOGIN_RESPONSES: Final[dict[int | str, dict[str, Any]] | None] = {
    HTTP_200_OK: {"model": response.LoginSuccessfulResponseSchema},
    HTTP_401_UNAUTHORIZED: {
        "model": response.UnauthorizedInvalidLoginOrPasswordResponseSchema
    },
    HTTP_422_UNPROCESSABLE_ENTITY: response.generate_combined_schema(
        "Validation Error",
        response.EmptyLoginResponseSchema,
        response.EmptyPasswordResponseSchema,
        response.TooShortLoginResponseSchema,
        response.TooShortPasswordResponseSchema,
        response.TooLongLoginResponseSchema,
        response.TooLongPasswordResponseSchema,
        response.WrongLoginFormatResponseSchema,
        response.WrongPasswordFormatResponseSchema,
    ),
    HTTP_500_INTERNAL_SERVER_ERROR: {"model": response.ServerErrorResponseSchema},
}

LOGOUT_RESPONSES: Final[dict[int | str, dict[str, Any]] | None] = {
    HTTP_200_OK: {"model": response.LogoutSuccessfulResponseSchema},
    HTTP_401_UNAUTHORIZED: {"model": response.UnauthenticatedResponseSchema},
    HTTP_500_INTERNAL_SERVER_ERROR: {"model": response.ServerErrorResponseSchema},
}
