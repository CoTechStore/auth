from abc import ABC, abstractmethod

from auth.application.common.handlers import (
    PipelineBehaviorHandler,
    RequestHandler,
)
from auth.domain.shared.domain_event import EventHandler

type Handler = RequestHandler | EventHandler | PipelineBehaviorHandler


class Resolver(ABC):
    @abstractmethod
    async def resolve[TDependency: Handler](
        self, dependency_type: type[TDependency]
    ) -> TDependency: ...
