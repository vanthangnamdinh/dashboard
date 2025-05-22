from abc import ABC, abstractmethod
from app.dashboard.domain.command import (
    WidgetData,
    GetDashboardList,
    GetDashboard,
    CreateNewWidget,
    UpdateWidget,
    NewMessage,
)
from app.dashboard.domain.entity.dashboard import Dashboard, Widget, Message
from typing import Dict


class DashboardUseCase(ABC):
    @abstractmethod
    async def create_dashboard(self, *, command: WidgetData) -> dict:
        """Create log"""

    @abstractmethod
    async def get_dashboards(self, *, command: GetDashboardList) -> dict:
        """Get log"""

    @abstractmethod
    async def get_dashboard(self, *, command: GetDashboard) -> dict:
        """Get log"""

    @abstractmethod
    async def create_widget(self, *, command: CreateNewWidget) -> dict:
        """Update log"""

    @abstractmethod
    async def update_widget(self, *, command: UpdateWidget) -> dict:
        """Update log"""

    @abstractmethod
    async def create_message(self, *, command: NewMessage) -> dict:
        """Update log"""
