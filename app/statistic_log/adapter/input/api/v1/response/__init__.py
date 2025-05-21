from pydantic import BaseModel, Field


class StatsticLogResponse(BaseModel):
    status: str = Field(..., description="Status")
    status_code: int = Field(..., description="Status code")
