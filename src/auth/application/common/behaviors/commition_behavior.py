from auth.application.common.handlers import HandleNext, PipelineBehaviorHandler
from auth.application.common.markers import Command
from auth.application.ports.transaction_manager import TransactionManager


class CommitionBehaviorHandler[TCommand: Command, TResponse](
    PipelineBehaviorHandler[TCommand, TResponse]
):
    """Поведение фиксации транзакции."""

    def __init__(self, transaction_manager: TransactionManager) -> None:
        self.__transaction_manager = transaction_manager

    async def handle(
        self, request: TCommand, handle_next: HandleNext[TCommand, TResponse]
    ) -> TResponse:
        response = await handle_next(request)
        await self.__transaction_manager.commit()

        return response
