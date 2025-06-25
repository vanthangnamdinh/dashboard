import httpx
import jwt
from sqlalchemy import select
from app.user.domain.repository.user import UserRepository
from app.user.domain.entity.user import User
from core.db import session
from core.config import config

class UserSQLAlchemyRepository(UserRepository):
    async def decode_jwt(self, token: str) -> dict:
        async with httpx.AsyncClient() as client:
            jwks_resp = await client.get(config.JWT_PUBLIC_KEY_URL)
            jwks = jwks_resp.json()
        
        # Giải mã JWT RS256
        unverified_header = jwt.get_unverified_header(token)
        key = next((k for k in jwks["keys"] if k["kid"] == unverified_header["kid"]), None)
        if not key:
            raise Exception("Public key for JWT not found")
        
        claims = jwt.decode(
            token, 
            key, 
            algorithms=[unverified_header["alg"]], 
            audience=config.JWT_AUDIENCE,
            issuer=config.JWT_ISSUER
        )
        
        return {
            "sub": claims["sub"],
            "email": claims.get("email", ""),
            "name": claims.get("name", ""),
        }

    async def save_user(self, user_info: dict) -> bool:
        async with session() as s:
            stmt = select(User).where(User.sub == user_info["sub"])
            result = await s.execute(stmt)
            user = result.scalar_one_or_none()
            
            if user:
                return False  # User đã tồn tại
            
            user = User(
                sub=user_info["sub"],
                email=user_info["email"]
            )
            s.add(user)
            await s.commit()
            return True  # User mới 