from dataclasses import dataclass


@dataclass(frozen=True)
class InfrastructureError(Exception):
    message: str


@dataclass(frozen=True)
class HandlerNotFoundError(InfrastructureError): ...
