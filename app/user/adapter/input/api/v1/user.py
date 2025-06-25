from fastapi import APIRouter, Depends
from app.user.application.dto import CheckUserJWTRequestDTO, CheckUserJWTResponseDTO
from app.user.domain.usecase.user import UserUseCase
from dependency_injector.wiring import Provide, inject
from app.container import Container

router = APIRouter()

@router.post("/check", response_model=CheckUserJWTResponseDTO, tags=["User"])
@inject
async def check_user_jwt(
    request: CheckUserJWTRequestDTO,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    return await usecase.check_user_jwt(request) 