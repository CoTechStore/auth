from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, cast

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from auth.bootstrap.config import AppConfig, get_config
from auth.bootstrap.di.containers.web import web_container
from auth.infrastructure.logging import get_logger_config
from auth.infrastructure.persistence.sqlalchemy.tables.setup import setup_mappings
from auth.presentation.web.controllers.auth import AUTH_ROUTER
from auth.presentation.web.controllers.healthcheck import HEALTHCHECK_ROUTER
from auth.presentation.web.exceptions.setup import (
    setup_application_error_handler,
    setup_domain_error_handler,
    setup_internal_error_handler,
)

if TYPE_CHECKING:
    from dishka import AsyncContainer


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Зависимости приложения."""
    setup_mappings()
    container = cast("AsyncContainer", application.state.dishka_container)
    yield
    await container.close()


def custom_openapi(application: FastAPI) -> dict[str, Any]:
    """Swagger configuration."""
    if application.openapi_schema:
        return application.openapi_schema
    openapi_schema = get_openapi(
        title="Auth",
        version="1.0",
        summary="Модуль для авторизации и аутентификации.",
        routes=application.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    application.openapi_schema = openapi_schema
    return application.openapi_schema


def setup_app(config: AppConfig) -> FastAPI:
    """Сборка приложения."""
    application = FastAPI(
        lifespan=lifespan,
        openapi_url=config.openapi_url,
        swagger_ui_init_oauth={
            "clientId": config.client_id,
            "clientSecret": config.client_secret,
        },
        docs_url="/auth/docs",
        swagger_ui_parameters={
            "displayRequestDuration": True,
            "persistAuthorization": True,
        },
    )
    application.openapi = lambda: custom_openapi(application)  # type: ignore[method-assign]
    return application


def setup_middlewares(application: FastAPI, config: AppConfig) -> None:
    """Регистрация middlewares для FastAPI."""
    origins = ["*"] if config.debug else config.cors_origins
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_exception_handlers(application: FastAPI) -> None:
    """Регистрация обработчиков исключений для FastAPI."""
    setup_application_error_handler(application=application)
    setup_domain_error_handler(application=application)
    setup_internal_error_handler(application=application)


def setup_routers(application: FastAPI) -> None:
    """Регистрация маршрутов для FastAPI."""
    application.include_router(HEALTHCHECK_ROUTER)
    application.include_router(AUTH_ROUTER)


def app_factory() -> FastAPI:
    """Точка старта приложения."""
    config = get_config()
    logger_config = get_logger_config(config.app_config)
    container = web_container(config.postgres_config, config.auth_config, logger_config)
    application = setup_app(config.app_config)
    setup_middlewares(application, config.app_config)
    setup_routers(application)
    setup_exception_handlers(application)
    setup_dishka(container=container, app=application)
    return application
