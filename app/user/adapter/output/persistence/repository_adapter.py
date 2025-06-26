from app.user.domain.repository.user import UserRepo
from typing import Dict
from app.user.domain.command import VerifyTokenRequest


class UserRepositoryAdapter:
    def __init__(self, *, user_repo: UserRepo):
        self.user_repo = user_repo
    
    async def verify_token(self, *, command: VerifyTokenRequest):
        return await self.user_repo.verify_token(command=command)
