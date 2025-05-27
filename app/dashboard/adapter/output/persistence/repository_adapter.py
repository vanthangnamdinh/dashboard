from app.dashboard.domain.repository.dashboard import DashboardRepo
from typing import Dict


class DashboardRepositoryAdapter:
    def __init__(self, *, dashboard_repo: DashboardRepo):
        self.dashboard_repo = dashboard_repo

    async def create_dashboard(self, *, data) -> dict:
        return await self.dashboard_repo.create_dashboard(data=data)

    async def update_dashboard_name(self, *, dashboard_id, data) -> dict:
        return await self.dashboard_repo.update_dashboard_name(
            dashboard_id=dashboard_id, data=data
        )

    async def get_dashboards(self, *, data) -> dict:
        return await self.dashboard_repo.get_dashboards(data=data)

    async def get_dashboard(self, *, data) -> dict:
        return await self.dashboard_repo.get_dashboard(data=data)

    async def create_widget(self, *, data) -> dict:
        return await self.dashboard_repo.create_widget(data=data)

    async def update_widget(self, *, data) -> dict:
        return await self.dashboard_repo.update_widget(data=data)

    async def delete_widget(self, *, widget_id) -> dict:
        return await self.dashboard_repo.delete_widget(widget_id=widget_id)

    async def create_message(self, *, data) -> dict:
        return await self.dashboard_repo.create_message(data=data)
