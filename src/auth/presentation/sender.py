from abc import ABC, abstractmethod

from auth.application.common.markers import BaseRequest


class Sender(ABC):
    @abstractmethod
    async def send[TResponse](self, request: BaseRequest[TResponse]) -> TResponse: ...
