from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.container import Container
from app.dashboard.adapter.input.api.v1.response import CustomResponse
from app.dashboard.domain.command import (
    WidgetData,
    GetDashboard,
    GetDashboardList,
    CreateNewWidget,
    UpdateWidget,
    NewMessage,
    DeleteWidget,
    UpdateNameDashboard,
)
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
    data = await usecase.create_dashboard(command=command)
    print("Dashboard created successfully")
    print(type(data))
    return {"data": data, "status_code": 0, "status": "Success"}


@dashboard_router.put(
    "/update-dashboard-name/{dashboard_id}",
    tags=["Dashboard"],
    summary="Update dashboard name",
    description="Update dashboard name",
    response_description="Update dashboard name",
    response_model=CustomResponse,
)
@inject
async def update_dashboard_name(
    dashboard_id: str,
    request: UpdateNameDashboard,
    usecase: DashboardUseCase = Depends(Provide[Container.dashboard_service]),
):
    command = UpdateNameDashboard(**request.model_dump())
    data = await usecase.update_dashboard_name(
        dashboard_id=dashboard_id, command=command
    )
    return {"data": data, "status_code": 0, "status": "Success"}


@dashboard_router.get(
    "/dashboard",
    tags=["Dashboard"],
    summary="Get dashboard",
    description="Get dashboard",
    response_description="Get dashboard",
    response_model=CustomResponse,
)
@inject
async def get_dashboard(
    dashboard_id: str = Query(..., description="Dashboard ID"),
    usecase: DashboardUseCase = Depends(Provide[Container.dashboard_service]),
):
    command = GetDashboard(dashboard_id=dashboard_id)
    data = await usecase.get_dashboard(command=command)
    return {"data": data, "status_code": 0, "status": "Success"}


@dashboard_router.get(
    "/dashboard-list",
    tags=["Dashboard"],
    summary="Get dashboard list",
    description="Get dashboard list",
    response_description="Get dashboard list",
    response_model=CustomResponse,
)
@inject
async def get_dashboard_list(
    conversation_id: str = Query(..., description="Conversation ID"),
    usecase: DashboardUseCase = Depends(Provide[Container.dashboard_service]),
):
    command = GetDashboardList(conversation_id=conversation_id)
    data = await usecase.get_dashboards(command=command)
    return {"data": data, "status_code": 0, "status": "Success"}


@dashboard_router.post(
    "/widget",
    tags=["Dashboard"],
    summary="Create new widget",
    description="Create new widget",
    response_description="Create new widget",
    response_model=CustomResponse,
)
@inject
async def create_new_widget(
    request: WidgetData,
    usecase: DashboardUseCase = Depends(Provide[Container.dashboard_service]),
):
    command = WidgetData(**request.model_dump())
    data = await usecase.create_widget(command=command)
    return {"data": data, "status_code": 0, "status": "Success"}


@dashboard_router.post(
    "/update-widget",
    tags=["Dashboard"],
    summary="Update widget",
    description="Update widget",
    response_description="Update widget",
    response_model=CustomResponse,
)
@inject
async def update_widget(
    request: UpdateWidget,
    usecase: DashboardUseCase = Depends(Provide[Container.dashboard_service]),
):
    command = UpdateWidget(**request.model_dump())
    data = await usecase.update_widget(command=command)
    return {"data": data, "status_code": 0, "status": "Success"}


@dashboard_router.delete(
    "/delete-widget",
    tags=["Dashboard"],
    summary="Delete widget",
    description="Delete widget",
    response_description="Delete widget",
    response_model=CustomResponse,
)
@inject
async def delete_widget(
    widget_id: str = Query(..., description="Widget ID"),
    usecase: DashboardUseCase = Depends(Provide[Container.dashboard_service]),
):
    data = await usecase.delete_widget(widget_id=widget_id)
    return {"data": data, "status_code": 0, "status": "Success"}


@dashboard_router.post(
    "/new-message",
    tags=["Dashboard"],
    summary="Create new message",
    description="Create new message",
    response_description="Create new message",
    response_model=CustomResponse,
)
@inject
async def create_new_message(
    request: NewMessage,
    usecase: DashboardUseCase = Depends(Provide[Container.dashboard_service]),
):
    command = NewMessage(**request.model_dump())
    data = await usecase.create_message(command=command)
    return {"data": data, "status_code": 0, "status": "Success"}
