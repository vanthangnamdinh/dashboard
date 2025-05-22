from abc import ABC, abstractmethod
from typing import Dict


class DashboardRepo(ABC):
    @abstractmethod
    async def create_dashboard(self, *, data) -> dict:
        """Save user"""
