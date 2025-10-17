from dataclasses import dataclass


@dataclass(frozen=True)
class BaseRequest[TResponse]: ...


@dataclass(frozen=True)
class Command[TResponse](BaseRequest[TResponse]): ...


@dataclass(frozen=True)
class Query[TResponse](BaseRequest[TResponse]): ...
