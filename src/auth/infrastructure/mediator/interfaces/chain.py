from abc import ABC, abstractmethod
from collections.abc import Iterable

from auth.application.common.handlers import (
    HandleNext,
    NotificationHandler,
    PipelineBehaviorHandler,
    RequestHandler,
)


class Chain(ABC):
    @abstractmethod
    def build_pipeline_behaviors(
        self,
        handler: RequestHandler | NotificationHandler,
        behaviors: Iterable[PipelineBehaviorHandler],
    ) -> HandleNext: ...
