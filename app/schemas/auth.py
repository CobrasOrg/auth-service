from pydantic import BaseModel, EmailStr, SecretStr, Field, field_validator, model_validator

from app.schemas.user import OwnerOut, ClinicOut, UserType

from app.utils.validators import(
    validate_password_data, validate_token_data,
    validate_confirm_password, validate_current_password_exists
)

class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Registered email address of the user", example="jane@example.com")
    password: SecretStr = Field(..., description="User's password", example="MySecureP@ssw0rd")

class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="Email to receive password reset instructions", example="jane@example.com")

class ResetPasswordRequest(BaseModel):
    token: str = Field(..., description="Password reset token sent via email", example="eyJhbGciOiJIUzI1NiIsInR5cCI...")
    newPassword: SecretStr = Field(..., description="New password", example="NewSecur3P@ss!")
    confirmPassword: SecretStr = Field(..., description="Confirmation of the new password", example="NewSecur3P@ss!")

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
    currentPassword: SecretStr = Field(..., description="Current password of the user", example="OldP@ss123")
    newPassword: SecretStr = Field(..., description="New password to set", example="NewSecur3P@ss!")
    confirmPassword: SecretStr = Field(..., description="Confirmation of the new password", example="NewSecur3P@ss!")

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
    success: bool = Field(..., description="Indicates if login was successful", example=True)
    token: str = Field(..., description="JWT access token", example="eyJhbGciOiJIUzI1NiIsInR5cCI...")
    user: OwnerOut | ClinicOut = Field(..., description="User profile data")

class BaseResponse(BaseModel):
    success: bool = Field(..., description="Operation status", example=True)
    message: str = Field(..., description="Informational message", example="Password updated successfully.")

class TokenVerificationResponse(BaseModel):
    success: bool = Field(..., description="Whether the token is valid", example=True)
    user_id: str = Field(..., description="User ID extracted from the token", example="65b4f50a-b8c6-4d04-8e54-730675247781")
    user_type: UserType = Field(..., description="Type of user (owner or clinic)", example="owner")
    email: EmailStr = Field(..., description="Email of the user", example="esperanza@clinic.co")