from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any

# This file is part of the FastAPI project.
# Input for api save widget


class WidgetData(BaseModel):
    dashboard_id: str = Field(..., description="Id of Dashboard")
    dashboard_name: str = Field(..., description="Name of Dashboard", max_length=200)
    end_user_id: str = Field(..., description="Id of End User")
    widget_id: str = Field(..., description="Id of Widget")
    parent_message_id: str = Field(..., description="Id of Parent Message")
    conversation_id: str = Field(..., description="Id of Conversation")
    width: int = Field(..., description="Width of Widget")
    height: int = Field(..., description="Height of Widget")
    x: int = Field(..., description="X position of Widget")
    y: int = Field(..., description="Y position of Widget")
    created_at: datetime = Field(..., description="Creation time of Widget")

class GetDashboard(BaseModel):
    dashboard_id: str = Field(..., description="Id of Dashboard")

class GetDashboardList(BaseModel):
    conversation_id: str = Field(..., description="Id of Conversation")

class CreateNewWidget(BaseModel):
    dashboard_id: str = Field(..., description="Id of Dashboard")
    widget_id: str = Field(..., description="Id of Widget")
    parent_message_id: str = Field(..., description="Id of Parent Message")
    width: int = Field(..., description="Width of Widget")
    height: int = Field(..., description="Height of Widget")
    x: int = Field(..., description="X position of Widget")
    y: int = Field(..., description="Y position of Widget")
    messageId: str = Field(..., description="Id of Message")


class UpdateWidget(BaseModel):
    widget_id: str = Field(..., description="Id of Widget")
    width: int = Field(..., description="Width of Widget")
    height: int = Field(..., description="Height of Widget")
    x: int = Field(..., description="X position of Widget")
    y: int = Field(..., description="Y position of Widget")


class NewMessage(BaseModel):
    widget_id: str = Field(..., description="Id of Widget")
    messageId: str = Field(..., description="Id of Message")
    parent_message_id: str = Field(..., description="Id of Parent Message")
    type: str = Field(..., description="Type of Message")
