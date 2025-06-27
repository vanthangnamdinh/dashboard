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
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal server error",
                        "message": str(e),
                    },
                )

    async def update_dashboard_name(self, *, dashboard_id, data) -> dict:
        async with async_session() as session:
            try:
                stmt = select(Dashboard).where(
                    (Dashboard.id == dashboard_id) & (Dashboard.isDeleted == False)
                )
                result = await session.execute(stmt)
                dashboard = result.scalar_one_or_none()

                if dashboard:
                    dashboard.name = data.dashboard_name
                    session.add(dashboard)
                    await session.commit()
                    await session.refresh(dashboard)
                    return {
                        "dashboard_id": dashboard.id,
                        "dashboard_name": dashboard.name,
                        "updated_at": dashboard.updated_at,
                    }
                else:
                    logger.error(f"Dashboard with ID {dashboard_id} not found.")
                    raise HTTPException(
                        status_code=404,
                        detail={
                            "error": "Dashboard not found",
                        },
                    )

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Failed to update dashboard name: {e}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal server error",
                        "message": str(e),
                    },
                )

    async def get_dashboards(self, *, data) -> dict:
        async with async_session() as session:
            try:
                stmt = select(Dashboard).where(
                    (Dashboard.conversation_id == data.conversation_id)
                    & (Dashboard.isDeleted == False)
                )
                result = await session.execute(stmt)
                dashboards = result.scalars().all()

                for dashboard in dashboards:
                    stmt_widgets = select(Widget).where(
                        (Widget.dashboard_id == dashboard.id)
                        & (Widget.isDeleted == False)
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
                            "parent_message_id": dashboard.parent_message_id,
                            "created_at": dashboard.created_at,
                            "updated_at": dashboard.updated_at,
                        }
                        for dashboard in dashboards
                    ],
                }

            except SQLAlchemyError as e:
                logger.error(f"Failed to get dashboards: {e}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal server error",
                        "message": str(e),
                    },
                )

    async def get_dashboard(self, *, data) -> dict:
        async with async_session() as session:
            try:
                stmt = select(Dashboard).where(
                    (Dashboard.id == data.dashboard_id) & (Dashboard.isDeleted == False)
                )
                result = await session.execute(stmt)
                dashboard = result.scalar_one_or_none()
                if not dashboard:
                    logger.error(f"Dashboard with ID {data.dashboard_id} not found.")
                    return {"error": "Dashboard not found"}
                stmt_widgets = select(Widget).where(
                    (Widget.dashboard_id == dashboard.id) & (Widget.isDeleted == False)
                )
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
                        (Message.widget_id == widget.id) & (Message.isDeleted == False)
                    )
                    message_result = await session.execute(stmt_messages)
                    messages = message_result.unique().scalars().all()
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
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal server error",
                        "message": str(e),
                    },
                )
            except HTTPException as e:
                logger.error(f"HTTP error: {e.detail}")
                raise HTTPException(
                    status_code=e.status_code,
                    detail={
                        "error": e.detail,
                        "message": str(e),
                    },
                )

    async def create_widget(self, *, data) -> dict:
        async with async_session() as session:
            try:
                dashboard = await session.get(Dashboard, data.dashboard_id)
                if not dashboard:
                    dashboard = Dashboard(
                        id=data.dashboard_id,
                        name=data.dashboard_name,
                        end_user_id=data.end_user_id,
                        conversation_id=data.conversation_id,
                        parent_message_id=data.parent_message_id,
                    )
                    session.add(dashboard)
                widget = await session.get(Widget, data.widget_id)
                if not widget:
                    logger.info(f"Creating new widget with ID {data.widget_id}")
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
                    id=data.message_id,
                    widget_id=data.widget_id,
                    parent_message_id=data.parent_message_id,
                    type=data.type,
                )
                dashboard.updated_at = datetime.now()
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
                    "updated_at": dashboard.updated_at,
                }

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Failed to create widget: {e}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal server error",
                        "message": str(e),
                    },
                )
            except HTTPException as e:
                logger.error(f"HTTP error: {e.detail}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal server error",
                        "message": str(e),
                    },
                )

    async def update_widget(self, *, data) -> dict:
        async with async_session() as session:
            try:
                stmt = select(Widget).where(
                    (Widget.id == data.widget_id) & (Widget.isDeleted == False)
                )
                result = await session.execute(stmt)
                widget = result.scalar_one_or_none()

                if widget:
                    widget.width = data.width
                    widget.height = data.height
                    widget.x = data.x
                    widget.y = data.y

                    session.add(widget)
                    dashboard = await session.get(Dashboard, widget.dashboard_id)
                    if dashboard:
                        dashboard.updated_at = datetime.now()
                        session.add(dashboard)
                    else:
                        logger.error(
                            f"Dashboard with ID {widget.dashboard_id} not found."
                        )
                    await session.commit()
                    await session.refresh(widget)
                    return {
                        "widget_id": widget.id,
                        "dashboard_id": widget.dashboard_id,
                        "width": widget.width,
                        "height": widget.height,
                        "x": widget.x,
                        "y": widget.y,
                        "updated_at": dashboard.updated_at if dashboard else None,
                    }
                else:
                    logger.error(f"Widget with ID {data.widget_id} not found.")
                    raise HTTPException(
                        status_code=500,
                        detail={
                            "error": "Widget not found",
                            "message": str(e),
                        },
                    )

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Failed to update widget: {e}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal server error",
                        "message": str(e),
                    },
                )
            except HTTPException as e:
                logger.error(f"HTTP error: {e.detail}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal server error",
                        "message": str(e),
                    },
                )

    async def delete_widget(self, *, widget_id) -> dict:
        async with async_session() as session:
            try:
                stmt = select(Widget).where(
                    (Widget.id == widget_id) & (Widget.isDeleted == False)
                )
                result = await session.execute(stmt)
                widget = result.scalar_one_or_none()

                if widget:
                    widget.isDeleted = True
                    widget.deleted_at = datetime.now()
                    session.add(widget)
                    dashboard = await session.get(Dashboard, widget.dashboard_id)
                    if dashboard:
                        dashboard.updated_at = datetime.now()
                        session.add(dashboard)

                    await session.commit()
                    return {
                        "widget_id": widget.id,
                        "dashboard_id": widget.dashboard_id,
                        "isDeleted": widget.isDeleted,
                        "deleted_at": widget.deleted_at,
                        "updated_at": dashboard.updated_at if dashboard else None,
                    }
                else:
                    logger.error(f"Widget with ID {widget_id} not found.")
                    raise HTTPException(
                        status_code=500,
                        detail={
                            "error": "Widget not found",
                            "message": f"Widget with ID {widget_id} not found.",
                        },
                    )

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Failed to delete widget: {e}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal server error",
                        "message": str(e),
                    },
                )
            except HTTPException as e:
                logger.error(f"HTTP error: {e.detail}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal server error",
                        "message": str(e),
                    },
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
                widget = await session.get(Widget, data.widget_id)
                if not widget:
                    logger.error(f"Widget with ID {data.widget_id} not found.")
                    return JSONResponse(
                        status_code=404,
                        content={"error": "Widget not found"},
                    )
                widget.updated_at = datetime.now()
                session.add(widget)
                dashboard = await session.get(Dashboard, widget.dashboard_id)
                if dashboard:
                    dashboard.updated_at = datetime.now()
                    session.add(dashboard)
                else:
                    logger.error(f"Dashboard with ID {widget.dashboard_id} not found.")

                await session.commit()
                await session.refresh(message)
                return message

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Failed to create message: {e}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal server error",
                        "message": str(e),
                    },
                )
            except HTTPException as e:
                logger.error(f"HTTP error: {e.detail}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal server error",
                        "message": str(e),
                    },
                )
