from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.dashboard.application.service.dashboard import DashboardService
from app.dashboard.adapter.output.persistence.repository_adapter import DashboardRepositoryAdapter
from app.dashboard.adapter.output.persistence.sqlalchemy.dashboard import DashboardOutput

from app.user.application.service.user import UserService
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserOutput

class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    dashboard_repo = Singleton(DashboardOutput)
    dashboard_repo_adapter = Factory(DashboardRepositoryAdapter, dashboard_repo=dashboard_repo)
    dashboard_service = Factory(DashboardService, repository=dashboard_repo_adapter)

    # Add other services and repositories as needed
    user_repo = Singleton(UserOutput)
    user_repo_adapter = Factory(UserRepositoryAdapter, user_repo=user_repo)
    user_service = Factory(UserService, repository=user_repo_adapter)
