from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any, Optional


# This file is part of the FastAPI project.
# Input for api save widget


class WidgetData(BaseModel):
    dashboard_id: str = Field(..., description="Id of Dashboard")
    dashboard_name: str = Field(..., description="Name of Dashboard")
    widget_id: str = Field(..., description="Id of Widget")
    end_user_id: str = Field(..., description="Id of End User")
    width: int = Field(..., description="Width of Widget")
    conversation_id: str = Field(..., description="Id of Conversation")
    parent_message_id: Optional[str] = Field(None, description="Id of Parent message")
    height: int = Field(..., description="Height of Widget")
    x: int = Field(..., description="X position of Widget")
    y: int = Field(..., description="Y position of Widget")
