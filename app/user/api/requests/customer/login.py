import re
from pydantic import BaseModel, field_validator
from app.user.exception.customer.invalid_creds import CustomerInvalidEmailERR, CustomerInvalidPasswordERR

class CustomerLoginREQT(BaseModel):
    email: str
    password: str
    
    @field_validator('email')
    @classmethod
    def check_email(cls, email: str) -> str:
        local_part = email.split('@')[0]
        
        if 3 <= len(local_part) <= 50:
            return email.lower()
        raise CustomerInvalidEmailERR()
    
    @field_validator("password")
    @classmethod
    def check_password(cls, password: str) -> str:
        password_regex = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,70}$'
        
        if re.match(password_regex, password):
            return password
        raise CustomerInvalidPasswordERR()