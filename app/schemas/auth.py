from pydantic import BaseModel, EmailStr

from app.schemas.user import OwnerOut, ClinicOut

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    newPassword: str
    confirmPassword: str
    
class ChangePasswordRequest(BaseModel):
    currentPassword: str
    newPassword: str
    confirmPassword: str
    
class UserLoginResponse(BaseModel):
    success: bool
    token: str
    user: OwnerOut | ClinicOut

class BaseAuthResponse(BaseModel):
    success: bool
    message: str