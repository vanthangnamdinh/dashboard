from pydantic import BaseModel, Field


class CustomResponse(BaseModel):
    data: dict = Field(..., description="Response data")
    status: str = Field(..., description="Status")
    status_code: int = Field(..., description="Status code")
