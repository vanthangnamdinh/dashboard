from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, composite

from core.db import Base
from core.db.mixins import TimestampMixin


class StatisticLog(Base, TimestampMixin):
    __tablename__ = "statistic_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)