from app.user.application.dto import CheckUserJWTRequestDTO, CheckUserJWTResponseDTO
from app.user.domain.repository.user import UserRepository

class UserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def check_user_jwt(self, request: CheckUserJWTRequestDTO) -> CheckUserJWTResponseDTO:
        user_info = await self.user_repository.decode_jwt(request.token)
        is_new = await self.user_repository.save_user(user_info)
        return CheckUserJWTResponseDTO(
            user_id=user_info["sub"],
            email=user_info["email"],
            is_new=is_new,
        ) 