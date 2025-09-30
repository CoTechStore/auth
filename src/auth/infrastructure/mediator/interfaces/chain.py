from abc import ABC, abstractmethod
from collections.abc import Iterable

from auth.application.common.handlers import (
    HandleNext,
    PipelineBehaviorHandler,
    RequestHandler,
)
from auth.domain.shared.domain_event import EventHandler


class Chain(ABC):
    @abstractmethod
    def build_pipeline_behaviors(
        self,
        handler: RequestHandler | EventHandler,
        behaviors: Iterable[PipelineBehaviorHandler],
    ) -> HandleNext: ...
