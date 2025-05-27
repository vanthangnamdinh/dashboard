from abc import ABC, abstractmethod
from typing import Dict


class DashboardRepo(ABC):
    @abstractmethod
    async def create_dashboard(self, *, data) -> dict:
        """Save user"""

    @abstractmethod
    async def update_dashboard_name(self, *, dashboard_id, data) -> dict:
        """Update dashboard name"""

    @abstractmethod
    async def get_dashboard(self, *, data) -> Dict:
        """Get dashboard by ID"""

    @abstractmethod
    async def get_dashboards(self, *, data) -> Dict:
        """Get all dashboards for a conversation"""

    @abstractmethod
    async def create_widget(self, *, data) -> dict:
        """Create a new widget in a dashboard"""

    @abstractmethod
    async def update_widget(self, *, data) -> dict:
        """Update an existing widget in a dashboard"""

    @abstractmethod
    async def delete_widget(self, *, widget_id) -> dict:
        """Delete a widget from a dashboard"""

    @abstractmethod
    async def create_message(self, *, data) -> dict:
        """Create a new message in a widget"""
