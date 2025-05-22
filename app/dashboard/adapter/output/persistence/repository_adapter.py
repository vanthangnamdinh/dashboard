from app.dashboard.domain.repository.dashboard import DashboardRepo


class DashboardRepositoryAdapter:
    def __init__(self, *, dashboard_repo: DashboardRepo):
        self.dashboard_repo = dashboard_repo

    async def create_dashboard(self, *, data) -> None:
        await self.dashboard_repo.create_dashboard(data=data)
