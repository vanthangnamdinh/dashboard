from app.user.domain.repository.user import UserRepo
import logging
from app.user.domain.command import VerifyTokenRequest

from fastapi import HTTPException
from core.config import config
import jwt  # PyJWT package

logger = logging.getLogger(__name__)


class UserOutput(UserRepo):
    async def verify_token(self, command: VerifyTokenRequest):
        try:
            payload = jwt.decode(
                command.token,
                config.JWT_PUBLIC_KEY_URL,
                algorithms=[config.JWT_ALGORITHM],
                audience=config.JWT_AUDIENCE,
                issuer=config.JWT_ISSUER,
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            return HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            return HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return HTTPException(status_code=401, detail="Token verification failed")
