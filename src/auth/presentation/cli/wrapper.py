import asyncio
from collections.abc import AsyncIterator, Callable, Coroutine
from functools import wraps
from typing import Any, cast, overload


@overload
def async_command[**Param, R](
    func: Callable[Param, Coroutine[Any, Any, R]],
) -> Callable[Param, R]: ...


@overload
def async_command[**Param, R](
    func: Callable[Param, AsyncIterator[R]],
) -> Callable[Param, R]: ...


def async_command[**Param, R](
    func: Callable[Param, Coroutine[Any, Any, R]] | Callable[Param, AsyncIterator[R]],
) -> Callable[Param, R]:
    @wraps(func)
    def runner(*args: Param.args, **kwargs: Param.kwargs) -> R:
        if asyncio.iscoroutinefunction(func):
            # Для обычных async функций
            return cast(R, asyncio.run(func(*args, **kwargs)))

        # Для async генераторов
        async def run_async_gen() -> R:
            result: R = None  # type: ignore
            async for item in func(*args, **kwargs):  # type: ignore
                result = item
            return result

        return asyncio.run(run_async_gen())

    return runner
