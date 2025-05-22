from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.container import Container
from app.dashboard.adapter.input.api.v1.request import WidgetData
from app.dashboard.adapter.input.api.v1.response import CustomResponse
from app.dashboard.domain.command import WidgetData
from app.dashboard.domain.usecase.dashboard import DashboardUseCase 
from core.fastapi.dependencies import PermissionDependency

dashboard_router = APIRouter()



@dashboard_router.post(
    "/new-dashboard",
    tags=["Dashboard"],
    summary="Create new dashboard",
    description="Create new dashboard",
    response_description="Create new dashboard",
    response_model=CustomResponse,
)
@inject
async def create_new_dashboard(
    request: WidgetData,
    usecase: DashboardUseCase = Depends(Provide[Container.dashboard_service]),
):
    command = WidgetData(**request.model_dump())
    await usecase.create_dashboard(command=command)
    return {"status_code": 0, "status": "Success"}
    
