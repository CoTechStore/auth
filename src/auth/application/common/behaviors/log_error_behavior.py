from typing import ClassVar

from auth.application.common.application_error import ApplicationError
from auth.application.common.handlers import HandleNext, PipelineBehaviorHandler
from auth.application.common.markers import BaseRequest
from auth.application.ports import IdentityProvider, Logger
from auth.domain.shared.domain_error import DomainError


class LogErrorBehaviorHandler[TRequest: BaseRequest, TResponse](
    PipelineBehaviorHandler[TRequest, TResponse]
):
    __status_code: ClassVar[dict[str, int]] = {
        "UNAUTHORIZED": 401,
        "FORBIDDEN": 403,
        "NOT_FOUND": 404,
        "VALIDATION": 422,
        "CONFLICT": 409,
    }

    def __init__(
        self,
        identity_provider: IdentityProvider,
        logger: Logger,
    ) -> None:
        self.__identity_provider = identity_provider
        self.__logger = logger

    async def handle(
        self,
        request: TRequest,
        handle_next: HandleNext[TRequest, TResponse],
    ) -> TResponse:
        try:
            response = await handle_next(request)
        except (ApplicationError, DomainError, Exception) as error:
            user_id = self.__identity_provider.current_user_id()

            if isinstance(error, (ApplicationError, DomainError)):
                type_error = error.type.name
                await self.__logger.aexception(
                    event=request.__class__.__name__,
                    current_user_id=str(user_id) if user_id else None,
                    status_code=self.__status_code[type_error],
                    error_type=type_error,
                    message=error.message,
                )
            else:
                await self.__logger.aexception(
                    event=request.__class__.__name__,
                    current_user_id=str(user_id) if user_id else None,
                    status_code=500,
                    error_type="InternalError",
                    message=str(error),
                )

            raise
        else:
            return response
