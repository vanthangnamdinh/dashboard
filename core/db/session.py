from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from enum import Enum
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from core.config import config

session_context: ContextVar[str] = ContextVar("session_context")


class SessionType(Enum):
    READ = "read"
    WRITE = "write"

engine = create_async_engine(config.POSTGRES_URL, echo=True)
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
@asynccontextmanager
async def get_session(session_type: SessionType = SessionType.WRITE) -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        if session_type == SessionType.READ:
            session.info["read_only"] = True
        else:
            session.info["read_only"] = False
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
            
def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)



class Base(DeclarativeBase):
    ...