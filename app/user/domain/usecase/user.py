from abc import ABC, abstractmethod
from app.user.domain.command import VerifyTokenRequest
from typing import Dict


class UserUseCase(ABC):
    @abstractmethod
    async def verify_user(self, *, command: VerifyTokenRequest) -> dict:
        """Create log"""
