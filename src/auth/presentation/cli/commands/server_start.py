from signal import SIGINT, signal

from click import argument, option
from dishka import FromDishka
from dishka.integrations.click import inject
from uvicorn import Server as UvicornServer


@argument("path", default=None, required=False)
@option("-h", "--host", default=None, help="Хост для запуска приложения")
@option("-p", "--port", default=None, help="Порт для запуска приложения")
@inject
def start_uvicorn(
    path: str | None,
    host: str | None,
    port: int | None,
    *,
    uvicorn_server: FromDishka[UvicornServer],
) -> None:
    """
    Запуск приложения на FastAPI
    Команда: core start-uvicorn.
    """
    if path is not None:
        uvicorn_server.config.app = path

    if host is not None:
        uvicorn_server.config.host = host

    if port is not None:
        uvicorn_server.config.port = port

    signal(
        SIGINT, lambda signum, frame: uvicorn_server.handle_exit(sig=signum, frame=frame)
    )

    uvicorn_server.run()
