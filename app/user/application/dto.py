from pydantic import BaseModel, Field

class CheckUserJWTRequestDTO(BaseModel):
    token: str = Field(..., description="JWT token (RS256)")

class CheckUserJWTResponseDTO(BaseModel):
    user_id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    is_new: bool = Field(..., description="Is this a new user?") 