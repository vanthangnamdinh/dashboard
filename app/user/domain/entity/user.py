from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sub: Mapped[str] = mapped_column(unique=True, nullable=False)  # JWT subject
    email: Mapped[str] = mapped_column(nullable=False) 