from app.dashboard.domain.repository.dashboard import DashboardRepo
from app.dashboard.domain.entity.dashboard import Dashboard, Widget
import logging
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.dashboard.domain.entity.dashboard import async_session

logger = logging.getLogger(__name__)


class DashboardOutput(DashboardRepo):
    async def create_dashboard(self, *, data) -> None:
        async with async_session() as session:
            try:
                dashboard = Dashboard(
                    id=data.dashboard_id,
                    name=data.dashboard_name,
                    end_user_id=data.end_user_id,
                    conversation_id=data.conversation_id,
                    parent_message_id=data.parent_message_id,
                )
                session.add(dashboard)

                widget = Widget(
                    id=data.widget_id,
                    dashboard_id=dashboard.id,
                    width=data.width,
                    height=data.height,
                    x=data.x,
                    y=data.y,
                )
                session.add(widget)

                await session.commit()
                await session.refresh(dashboard)
                await session.refresh(widget)

                return dashboard

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Failed to create dashboard: {e}")
                return None
