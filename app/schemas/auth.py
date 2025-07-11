from pydantic import BaseModel, EmailStr

from app.schemas.user import OwnerOut, ClinicOut

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class UserLoginResponse(BaseModel):
    success: bool
    token: str
    user: OwnerOut | ClinicOut