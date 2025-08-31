from dataclasses import dataclass

from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from auth.presentation.web.schemas.base import SuccessfulResponse

HEALTHCHECK_ROUTER = APIRouter(tags=["Healthcheck"])


@dataclass(frozen=True)
class Healthcheck:
    status: str


@HEALTHCHECK_ROUTER.get(
    "/healthcheck",
    responses={HTTP_200_OK: {"model": SuccessfulResponse[Healthcheck]}},
    status_code=HTTP_200_OK,
)
def healthcheck() -> SuccessfulResponse[Healthcheck]:
    return SuccessfulResponse(status_code=HTTP_200_OK, result=Healthcheck("OK"))
