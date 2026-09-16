from app.user.exception.jwt.invalid import JwtInvalidFormatERR
import jwt
from app.user.dto.customer.authorized import CustomerAuthorizedDTO
from app.core.config.base import get_settings
from app.user.service.infrastructure.jwt.keys import load_public_key

settings = get_settings()

def jwt_decode(token: str) -> CustomerAuthorizedDTO:
    if "." not in token:
        raise JwtInvalidFormatERR()
    
    jwt_token_payload = jwt.decode(
        token,
        load_public_key(),
        algorithms=[settings.jwt.algorithm],
    )
    
    return CustomerAuthorizedDTO(**jwt_token_payload)