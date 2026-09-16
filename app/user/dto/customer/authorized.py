from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class CustomerAuthorizedDTO:
    type: Literal["access_token"]
    jti: str
    exp: int
    iat: int
    sub: int
    role: str | None = None