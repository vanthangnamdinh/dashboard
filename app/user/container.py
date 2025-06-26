from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.user.adapter.output.persistence.repository_adapter import (
    UserRepositoryAdapter,
)
from app.user.adapter.output.persistence.sqlalchemy.user import (
    UserOutput,
)
from app.user.application.service.user import UserService

from core.db import session


class UserContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app"])
    user_repo = Singleton(UserOutput, session=session)
    user_repository_adapter = Factory(
        UserRepositoryAdapter,
        repository=user_repo,
    )
    statistic_service = Factory(
        UserService, repository=user_repository_adapter
    )
