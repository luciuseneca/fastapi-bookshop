from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

class AuthorizedCustomerREQT(BaseModel):
    type: Literal["access_token"]
    jti: str
    exp: int
    iat: int
    sub: int = Field(..., description="Customer ID")
    role: str | None = None


class ConfirmAuthCustomerREQT(BaseModel):
    session_id: UUID
    otp: str