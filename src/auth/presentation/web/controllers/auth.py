from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from starlette.responses import Response

from auth.domain.user.value_objects import UserId
from auth.application.operations.commands import LogoutCommand, RegisterCommand
from auth.application.operations.commands.login import LoginCommand
from auth.presentation.sender import Sender as Mediator
from auth.presentation.web.const import response as text
from auth.presentation.web.const.response import REFRESH
from auth.presentation.web.responses import auth as auth_response
from auth.presentation.web.schemas.base import SuccessfulResponse

AUTH_ROUTER = APIRouter(prefix="/api/v1/auth", tags=["Auth"], route_class=DishkaRoute)


@AUTH_ROUTER.post(
    path="/register",
    summary="Registration new user.",
    responses=auth_response.REGISTER_RESPONSES,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    command: RegisterCommand,
    *,
    mediator: FromDishka[Mediator],
) -> SuccessfulResponse[UserId]:
    result = await mediator.send(command)

    return SuccessfulResponse(status_code=status.HTTP_201_CREATED, result=result)


@AUTH_ROUTER.post(
    path="/login",
    summary="Login to your account.",
    responses=auth_response.LOGIN_RESPONSES,
    status_code=status.HTTP_200_OK,
)
async def login(
    credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())],
    *,
    mediator: FromDishka[Mediator],
) -> Response:
    command = LoginCommand(credentials.username, credentials.password)
    result = await mediator.send(command)

    response = Response(status_code=status.HTTP_200_OK, content=result.user_id)
    response.set_cookie(
        key=REFRESH,
        value=str(result.session_id),
        expires=result.expires_at,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return response


@AUTH_ROUTER.post(
    path="/logout",
    summary="Logout of the account.",
    responses=auth_response.LOGOUT_RESPONSES,
    status_code=status.HTTP_200_OK,
)
async def logout(mediator: FromDishka[Mediator]) -> Response:
    command = LogoutCommand()
    await mediator.send(command)

    response = Response(status_code=status.HTTP_200_OK, content=text.SUCCESS_LOGOUT)
    response.delete_cookie(
        key=REFRESH,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return response
