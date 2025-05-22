from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, composite, relationship
from datetime import datetime, UTC
from core.config import config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Tạo engine cho PostgreSQL
engine = create_async_engine(config.POSTGRES_URL, echo=True)

# Tạo session factory
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

from core.db import Base
from core.db.mixins import TimestampMixin


# This file is part of the FastAPI project.
# Input for api save widget

from pydantic_settings import BaseSettings


class Dashboard(Base, TimestampMixin):
    __tablename__ = "dashboard"

    id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    end_user_id: Mapped[str] = mapped_column(nullable=False)
    conversation_id: Mapped[str] = mapped_column(nullable=False)
    parent_message_id: Mapped[str] = mapped_column(nullable=True)
    isDeleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    widgets = relationship(
        "Widget", back_populates="dashboard", cascade="all, delete-orphan"
    )


class Widget(Base, TimestampMixin):
    __tablename__ = "widget"

    id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    dashboard_id: Mapped[str] = mapped_column(
        String, ForeignKey("dashboard.id", ondelete="CASCADE"), nullable=False
    )
    width: Mapped[int] = mapped_column(nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    x: Mapped[int] = mapped_column(nullable=False)
    y: Mapped[int] = mapped_column(nullable=False)
    isDeleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    dashboard = relationship("Dashboard", back_populates="widgets")
    messages = relationship(
        "Message", back_populates="widget", cascade="all, delete-orphan"
    )


class Message(Base, TimestampMixin):
    __tablename__ = "message"

    id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    widget_id: Mapped[str] = mapped_column(
        String, ForeignKey("widget.id", ondelete="CASCADE"), nullable=False
    )
    parent_message_id: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[str] = mapped_column(nullable=False)
    isDeleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    widget = relationship("Widget", back_populates="messages")
