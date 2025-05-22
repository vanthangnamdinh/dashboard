from app.dashboard.adapter.output.persistence.repository_adapter import DashboardRepositoryAdapter
from app.dashboard.domain.command import WidgetData
from app.dashboard.domain.usecase.dashboard import DashboardUseCase
from core.db import Transactional
from core.helpers.token import TokenHelper


class DashboardService(DashboardUseCase):
    def __init__(self, *, repository: DashboardRepositoryAdapter):
        self.repository = repository

    async def create_dashboard(self, *, command: WidgetData) -> None:
        await self.repository.create_dashboard(data=command)