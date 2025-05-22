from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.statistic_log.application.service.statistic import StatisticService
from app.statistic_log.adapter.output.persistence.repository_adapter import StatisticRepositoryAdapter
from app.statistic_log.adapter.output.persistence.sqlalchemy.statistic import StatistisLogRepo

from app.dashboard.application.service.dashboard import DashboardService
from app.dashboard.adapter.output.persistence.repository_adapter import DashboardRepositoryAdapter
from app.dashboard.adapter.output.persistence.sqlalchemy.dashboard import DashboardOutput

from core.db import session
class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    statistic_log_repo = Singleton(StatistisLogRepo)
    statistic_repo_adapter = Factory(StatisticRepositoryAdapter, statistic_repo=statistic_log_repo)
    statistic_service = Factory(StatisticService, repository=statistic_repo_adapter)

    dashboard_repo = Singleton(DashboardOutput, session=session)
    dashboard_repo = Singleton(DashboardOutput)
    dashboard_repo_adapter = Factory(DashboardRepositoryAdapter, dashboard_repo=dashboard_repo)
    dashboard_service = Factory(DashboardService, repository=dashboard_repo_adapter)
