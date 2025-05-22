from abc import ABC, abstractmethod
from app.dashboard.domain.command import WidgetData


class DashboardUseCase(ABC):
    @abstractmethod
    async def create_dashboard(self, *, command: WidgetData) -> None:
        """Create log"""