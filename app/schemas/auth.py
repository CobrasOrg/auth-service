from pydantic import BaseModel, EmailStr, field_validator, model_validator

from app.schemas.user import OwnerOut, ClinicOut

from app.utils.validators import (
    validate_password_data, validate_token_data,
    validate_confirm_password, validate_current_password_exists
)

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    newPassword: str
    confirmPassword: str

    @field_validator("newPassword")
    def validate_password(cls, value): 
        return validate_password_data(value)

    @field_validator("token")
    def validate_token(cls, value):
        return validate_token_data(value)
    
    @model_validator(mode="after")
    def validate_confirm(self):
        validate_confirm_password(self.newPassword, self.confirmPassword)
        return self
    
class ChangePasswordRequest(BaseModel):
    currentPassword: str
    newPassword: str
    confirmPassword: str

    @field_validator("currentPassword")
    def validate_current_password(cls, value): 
        return validate_current_password_exists(value)

    @field_validator("newPassword")
    def validate_new_password(cls, value): 
        return validate_password_data(value)
    
    @model_validator(mode="after")
    def validate_confirm(self):
        validate_confirm_password(self.newPassword, self.confirmPassword)
        return self
    
class UserLoginResponse(BaseModel):
    success: bool
    token: str
    user: OwnerOut | ClinicOut

class BaseResponse(BaseModel):
    success: bool
    message: str