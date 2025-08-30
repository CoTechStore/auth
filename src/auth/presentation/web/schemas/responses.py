import re
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field
from starlette import status

from auth.application.common.const import errors as application_text
from auth.application.common.dto.user_info_dto import UserInfoDto
from auth.domain.user.const import errors as domain_user_text
from auth.presentation.web.const import errors as presentation_error_text
from auth.presentation.web.const import response as presentation_response_text


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthenticateSuccessfulResponse:
    access_token: str
    expires: int
    user_info: UserInfoDto


class ModelResponse(BaseModel):
    """Общее исключение для моделей."""

    @classmethod
    def generate_response_schema(cls) -> dict:
        model_name = cls.__name__.replace("ResponseSchema", "")
        model_name = "_".join(
            word.lower() for word in re.findall(r"[A-Z][a-z]*", model_name)
        )
        return {
            model_name: {
                "summary": cls.__doc__.strip() if cls.__doc__ else "",
                "value": cls().model_dump(),
            }
        }


def generate_combined_schema[TModel: ModelResponse](
    description: str, *models: type[TModel]
) -> dict[str, Any]:
    """Генерирует схему для комбинированного ответа."""
    examples = {}
    for model in models:
        examples.update(model.generate_response_schema())

    return {
        "description": description,
        "content": {"application/json": {"examples": examples}},
    }


class LoginSuccessfulResponseSchema(ModelResponse):
    status_code: int = Field(default=status.HTTP_200_OK)
    result: AuthenticateSuccessfulResponse


class LogoutSuccessfulResponseSchema(ModelResponse):
    status_code: int = Field(default=status.HTTP_200_OK)
    result: str = Field(default=presentation_response_text.SUCCESS_LOGOUT)


class UnauthorizedInvalidLoginOrPasswordResponseSchema(ModelResponse):
    status_code: int = Field(default=status.HTTP_401_UNAUTHORIZED)
    error: str = Field(default=application_text.INVALID_LOGIN_OR_PASSWORD)


class UnauthorizedResponseSchema(ModelResponse):
    status_code: int = Field(default=status.HTTP_401_UNAUTHORIZED)
    error: str = Field(default=application_text.APPLICATION_FORBIDDEN)


class UnauthenticatedResponseSchema(ModelResponse):
    status_code: int = Field(default=status.HTTP_401_UNAUTHORIZED)
    error: str = Field(default=application_text.UNAUTHENTICATED)


# region ----------------------------------------- 422 -------------------------------
class EmptyLoginResponseSchema(ModelResponse):
    """Ответ при пустом логине."""

    status_code: int = Field(default=status.HTTP_422_UNPROCESSABLE_ENTITY)
    error: str = Field(default=domain_user_text.EMPTY_LOGIN)


class EmptyPasswordResponseSchema(ModelResponse):
    """Ответ при пустом пароле."""

    status_code: int = Field(default=status.HTTP_422_UNPROCESSABLE_ENTITY)
    error: str = Field(default=domain_user_text.EMPTY_PASSWORD)


class TooShortLoginResponseSchema(ModelResponse):
    """Ответ при коротком логине."""

    status_code: int = Field(default=status.HTTP_422_UNPROCESSABLE_ENTITY)
    error: str = Field(default=domain_user_text.TOO_SHORT_LOGIN)


class TooShortPasswordResponseSchema(ModelResponse):
    """Ответ при коротком пароле."""

    status_code: int = Field(default=status.HTTP_422_UNPROCESSABLE_ENTITY)
    error: str = Field(default=domain_user_text.TOO_SHORT_PASSWORD)


class TooLongLoginResponseSchema(ModelResponse):
    """Ответ при длинном логине."""

    status_code: int = Field(default=status.HTTP_422_UNPROCESSABLE_ENTITY)
    error: str = Field(default=domain_user_text.TOO_LONG_LOGIN)


class TooLongPasswordResponseSchema(ModelResponse):
    """Ответ при длинном пароле."""

    status_code: int = Field(default=status.HTTP_422_UNPROCESSABLE_ENTITY)
    error: str = Field(default=domain_user_text.TOO_LONG_PASSWORD)


class WrongLoginFormatResponseSchema(ModelResponse):
    """Ответ при неправильном формате логина."""

    status_code: int = Field(default=status.HTTP_422_UNPROCESSABLE_ENTITY)
    error: str = Field(default=domain_user_text.WRONG_LOGIN_FORMAT)


class WrongPasswordFormatResponseSchema(ModelResponse):
    """Ответ при неправильном формате пароля."""

    status_code: int = Field(default=status.HTTP_422_UNPROCESSABLE_ENTITY)
    error: str = Field(default=domain_user_text.WRONG_PASSWORD_FORMAT)


# endregion ------------------------------------------------------------------------


class ServerErrorResponseSchema(ModelResponse):
    """Схема данных для конфликта организаций."""

    status_code: int = Field(default=status.HTTP_500_INTERNAL_SERVER_ERROR)
    error: str = Field(default=presentation_error_text.ERROR_INTERNAL_SERVER)
