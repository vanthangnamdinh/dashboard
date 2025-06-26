from abc import ABC, abstractmethod
from typing import Dict


class UserRepo(ABC):
    @abstractmethod
    async def verify_token(self, *, data) -> dict:
        """Save user"""

    