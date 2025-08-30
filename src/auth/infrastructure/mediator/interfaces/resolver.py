from abc import ABC, abstractmethod

from auth.application.common.handlers import (
    NotificationHandler,
    PipelineBehaviorHandler,
    RequestHandler,
)

type Handler = RequestHandler | NotificationHandler | PipelineBehaviorHandler


class Resolver(ABC):
    @abstractmethod
    async def resolve[TDependency: Handler](
        self, dependency_type: type[TDependency]
    ) -> TDependency: ...
