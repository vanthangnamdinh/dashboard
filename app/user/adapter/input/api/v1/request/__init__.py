from pydantic import BaseModel, Field

# This file is part of the FastAPI project.
# Input for api save widget


class VerifyTokenRequest(BaseModel):
    token: str = Field(..., description="Token to verify")
    provider: str = Field(..., description="Provider to verify")
   