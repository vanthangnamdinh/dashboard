from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.container import Container
from app.user.adapter.input.api.v1.response import CustomResponse
from app.user.domain.command import VerifyTokenRequest
from app.user.domain.usecase.user import UserUseCase
from core.fastapi.dependencies import PermissionDependency

user_router = APIRouter()


@user_router.post(
    "/verify-token",
    tags=["User"],
    summary="Verify token",
    description="Verify token",
    response_description="Verify token",
    response_model=CustomResponse,
)
@inject
async def verify_token(
    request: VerifyTokenRequest,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    command = VerifyTokenRequest(**request.model_dump())
    data = await usecase.verify_token(command=command)
    return {"data": data, "status_code": 0, "status": "Success"}


