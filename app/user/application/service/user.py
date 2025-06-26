from app.user.adapter.output.persistence.repository_adapter import (
    UserRepositoryAdapter,
)
from app.user.domain.command import VerifyTokenRequest
from app.user.domain.usecase.user import UserUseCase
from core.db import Transactional
from core.helpers.token import TokenHelper
from typing import Dict


class UserService(UserUseCase):
    def __init__(self, *, repository: UserRepositoryAdapter):
        self.repository = repository

    async def verify_token(self, *, command: VerifyTokenRequest) -> dict:
        return await self.repository.verify_token(command=command)
