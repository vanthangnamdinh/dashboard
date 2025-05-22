from app.dashboard.domain.repository.dashboard import DashboardRepo
from app.dashboard.domain.entity.dashboard import Dashboard, Widget, Message
import logging
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlalchemy import select
from app.dashboard.domain.entity.dashboard import async_session
from fastapi import HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class DashboardOutput(DashboardRepo):
    async def create_dashboard(self, *, data) -> dict:
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
                return {
                    "dashboard_id": dashboard.id,
                    "widget_id": widget.id,
                    "parent_message_id": dashboard.parent_message_id,
                    "conversation_id": dashboard.conversation_id,
                    "end_user_id": dashboard.end_user_id,
                    "updated_at": dashboard.updated_at,
                }

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Failed to create dashboard: {e}")
                return {"error": str(e)}

    async def get_dashboards(self, *, data) -> dict:
        async with async_session() as session:
            try:
                stmt = select(Dashboard).where(
                    Dashboard.conversation_id == data.conversation_id,
                )
                result = await session.execute(stmt)
                dashboards = result.scalars().all()

                for dashboard in dashboards:
                    stmt_widgets = select(Widget).where(
                        Widget.dashboard_id == dashboard.id
                    )
                    widget_result = await session.execute(stmt_widgets)
                    widgets = widget_result.scalars().all()
                    dashboard.count_widget = len(widgets)

                return {
                    "dashboards": [
                        {
                            "dashboard_id": dashboard.id,
                            "dashboard_name": dashboard.name,
                            "count_widget": dashboard.count_widget,
                            "updated_at": dashboard.updated_at,
                        }
                        for dashboard in dashboards
                    ],
                }

            except SQLAlchemyError as e:
                logger.error(f"Failed to get dashboards: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)},
                )

    async def get_dashboard(self, *, data) -> dict:
        async with async_session() as session:
            try:
                stmt = select(Dashboard).where(Dashboard.id == data.dashboard_id)
                result = await session.execute(stmt)
                dashboard = result.scalar_one_or_none()
                if not dashboard:
                    logger.error(f"Dashboard with ID {data.dashboard_id} not found.")
                    return {"error": "Dashboard not found"}
                await session.commit()
                stmt_widgets = select(Widget).where(Widget.dashboard_id == dashboard.id)
                widget_result = await session.execute(stmt_widgets)
                widgets = widget_result.scalars().all()
                dashboard_data = {
                    "dashboard_id": dashboard.id,
                    "dashboard_name": dashboard.name,
                    "updated_at": dashboard.updated_at,
                    "widgets": [],
                }
                # Fetch messages for each widget
                for widget in widgets:
                    stmt_messages = select(Message).where(
                        Message.widget_id == widget.id
                    )
                    message_result = await session.execute(stmt_messages)
                    messages = message_result.scalars().all()
                    dashboard_data["widgets"].append(
                        {
                            "widget_id": widget.id,
                            "width": widget.width,
                            "height": widget.height,
                            "x": widget.x,
                            "y": widget.y,
                            "messages": [
                                {
                                    "message_id": message.id,
                                    "parent_message_id": message.parent_message_id,
                                    "type": message.type,
                                    "created_at": message.created_at,
                                }
                                for message in messages
                            ],
                        }
                    )

                return {
                    "dashboard_id": dashboard_data["dashboard_id"],
                    "dashboard_name": dashboard_data["dashboard_name"],
                    "updated_at": dashboard_data["updated_at"],
                    "widgets": dashboard_data["widgets"],
                }

            except SQLAlchemyError as e:
                logger.error(f"Failed to get dashboard: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)},
                )
            except HTTPException as e:
                logger.error(f"HTTP error: {e.detail}")
                return JSONResponse(
                    status_code=e.status_code,
                    content={"error": e.detail},
                )

    async def create_widget(self, *, data) -> dict:
        async with async_session() as session:
            try:
                widget = Widget(
                    id=data.widget_id,
                    dashboard_id=data.dashboard_id,
                    width=data.width,
                    height=data.height,
                    x=data.x,
                    y=data.y,
                )
                session.add(widget)
                message = Message(
                    id=data.messageId,
                    widget_id=widget.id,
                    parent_message_id=data.parent_message_id,
                )
                session.add(message)
                await session.commit()
                await session.refresh(widget)
                await session.refresh(message)
                logger.info(f"Widget created with ID {widget.id}")
                return {
                    "widget_id": widget.id,
                    "dashboard_id": widget.dashboard_id,
                    "width": widget.width,
                    "height": widget.height,
                    "x": widget.x,
                    "y": widget.y,
                }

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Failed to create widget: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)},
                )
            except HTTPException as e:
                logger.error(f"HTTP error: {e.detail}")
                return JSONResponse(
                    status_code=e.status_code,
                    content={"error": e.detail},
                )

    async def update_widget(self, *, data) -> dict:
        async with async_session() as session:
            try:
                stmt = select(Widget).where(Widget.id == data.widget_id)
                result = await session.execute(stmt)
                widget = result.scalar_one_or_none()

                if widget:
                    widget.width = data.width
                    widget.height = data.height
                    widget.x = data.x
                    widget.y = data.y
                    await session.commit()
                    await session.refresh(widget)
                    return widget
                else:
                    logger.error(f"Widget with ID {data.widget_id} not found.")
                    return JSONResponse(
                        status_code=404,
                        content={"error": "Widget not found"},
                    )

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Failed to update widget: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)},
                )
            except HTTPException as e:
                logger.error(f"HTTP error: {e.detail}")
                return JSONResponse(
                    status_code=e.status_code,
                    content={"error": e.detail},
                )

    async def create_message(self, *, data) -> dict:
        async with async_session() as session:
            try:
                message = Message(
                    id=data.messageId,
                    widget_id=data.widget_id,
                    parent_message_id=data.parent_message_id,
                    type=data.type,
                    created_at=datetime.now(),
                )
                session.add(message)
                await session.commit()
                await session.refresh(message)
                return message

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Failed to create message: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)},
                )
            except HTTPException as e:
                logger.error(f"HTTP error: {e.detail}")
                return JSONResponse(
                    status_code=e.status_code,
                    content={"error": e.detail},
                )
