class UserRepository:
    async def decode_jwt(self, token: str) -> dict:
        """Decode JWT RS256 lấy thông tin user"""
        raise NotImplementedError

    async def save_user(self, user_info: dict) -> bool:
        """Lưu user vào DB, trả về True nếu là user mới"""
        raise NotImplementedError 