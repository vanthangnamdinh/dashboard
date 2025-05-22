from abc import ABC, abstractmethod


class DashboardRepo(ABC):
    @abstractmethod
    async def create_dashboard(self, *, data) -> None:
        """Save user"""
