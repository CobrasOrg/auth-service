from pydantic import BaseModel, EmailStr, SecretStr, field_validator, model_validator

from app.schemas.user import OwnerOut, ClinicOut, UserType

from app.utils.validators import (
    validate_password_data, validate_token_data,
    validate_confirm_password, validate_current_password_exists
)

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    newPassword: SecretStr
    confirmPassword: SecretStr

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
    currentPassword: SecretStr
    newPassword: SecretStr
    confirmPassword: SecretStr

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

class TokenVerificationResponse(BaseModel):
    success: bool
    user_id: str
    user_type: UserType