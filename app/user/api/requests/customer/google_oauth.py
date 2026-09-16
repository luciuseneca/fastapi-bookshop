from pydantic import BaseModel, EmailStr

class CustomerOauthREQT(BaseModel):
    email: EmailStr
    oauth_id: str
    username: str