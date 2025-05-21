from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any

class StatisticData(BaseModel):
    url: str = Field(..., description="URL of browser when User sends a message")
    page_title: str = Field(..., description="Page title")
    page_metadata: Dict[str, Any] = Field(..., description="JSON metadata of the page. Such as description, author,...")
    page_keywords: List[str] = Field(..., description="An array of strings representing all text on the page")
    session_history_url: List[str] = Field(..., description="Array of history URLs")
    focus_content_snippet: Dict[str, Any] = Field(..., description="JSON snippet of current focus content.")
    reading_duration_ms: int = Field(..., description="Reading duration in milliseconds")
    cookies: Dict[str, Any] = Field(..., description="JSON cookies")

class StatisticLogRequest(BaseModel):
    user: str = Field(..., description="Id of User")
    message_id: str = Field(..., description="ID of message")
    conversation_id: str = Field(..., description="Id of conversation")
    timestamp_chat: datetime  = Field(..., description="Time of message")
    statistic_data: StatisticData = Field(..., description="statistic_data")
    error_message: str = Field(..., description="Using to store the error response returned by the BE (Backend), if any")

