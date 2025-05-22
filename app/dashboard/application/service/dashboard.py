from app.dashboard.adapter.output.persistence.repository_adapter import (
    DashboardRepositoryAdapter,
)
from app.dashboard.domain.command import (
    WidgetData,
    GetDashboardList,
    GetDashboard,
    CreateNewWidget,
    UpdateWidget,
    NewMessage,
)
from app.dashboard.domain.usecase.dashboard import DashboardUseCase
from core.db import Transactional
from core.helpers.token import TokenHelper
from typing import Dict


class DashboardService(DashboardUseCase):
    def __init__(self, *, repository: DashboardRepositoryAdapter):
        self.repository = repository

    async def create_dashboard(self, *, command: WidgetData) -> dict:
        return await self.repository.create_dashboard(data=command)

    async def get_dashboards(self, *, command: GetDashboardList) -> dict:
        return await self.repository.get_dashboards(data=command)

    async def get_dashboard(self, *, command: GetDashboard) -> dict:
        return await self.repository.get_dashboard(data=command)

    async def create_widget(self, *, command: CreateNewWidget) -> dict:
        return await self.repository.create_widget(data=command)

    async def update_widget(self, *, command: UpdateWidget) -> dict:
        return await self.repository.update_widget(data=command)

    async def create_message(self, *, command: NewMessage) -> dict:
        return await self.repository.create_message(data=command)
