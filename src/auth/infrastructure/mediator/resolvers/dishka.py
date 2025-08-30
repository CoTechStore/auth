from typing import cast

from dishka import AsyncContainer

from auth.infrastructure.mediator.interfaces.resolver import Handler, Resolver


class DishkaResolver(Resolver):
    """Класс, отвечающий за получения зависимостей."""

    def __init__(self, container: AsyncContainer) -> None:
        self.__container = container

    async def resolve[TDependency: Handler](
        self, dependency_type: type[TDependency]
    ) -> TDependency:
        return cast(TDependency, await self.__container.get(dependency_type))
