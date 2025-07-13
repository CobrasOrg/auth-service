from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, SecretStr, Field, field_validator, model_validator

from app.utils.validators import(
    validate_password_data, validate_name_data, validate_phone_data, 
    validate_address_data, validate_email_data, validate_locality_data, 
    validate_confirm_password
)

class UserType(str, Enum):
    OWNER = "owner"
    CLINIC = "clinic"

class BaseUserRegister(BaseModel):
    name: str = Field(..., description="Full name of the user")
    email: EmailStr = Field(..., description="Valid email address")
    password: SecretStr = Field(..., description="Secure password")
    confirmPassword: SecretStr = Field(..., description="Password confirmation")
    phone: str = Field(..., description="Phone number with country code")
    address: str = Field(..., description="Street address")

    @field_validator("password")
    def validate_password(cls, value): 
        return validate_password_data(value)

    @field_validator("name")
    def validate_name(cls, value):
        return validate_name_data(value)

    @field_validator("phone", mode="before")
    def validate_phone(cls, value):
        return validate_phone_data(value)

    @field_validator("address")
    def validate_address(cls, value):
        return validate_address_data(value)
    
    @field_validator("email", mode="before")
    def validate_email(cls, value):
        return validate_email_data(value)
    
    @model_validator(mode="after")
    def validate_confirm(self):
        validate_confirm_password(self.password, self.confirmPassword)
        return self

class OwnerRegister(BaseUserRegister):
    """Schema for registering an owner user."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Carlos Herrera",
                "email": "carlos@example.com",
                "password": "StrongPass123!",
                "confirmPassword": "StrongPass123!",
                "phone": "+573001234567",
                "address": "Calle 123 #45-67"
            }
        }
    }

class ClinicRegister(BaseUserRegister):
    locality: str = Field(..., description="City or municipality where the clinic is located")

    @field_validator("locality")
    def validate_locality(cls, value):
        return validate_locality_data(value)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Clínica Vida",
                "email": "contacto@vidaclinic.com",
                "password": "SecureP@ssword123",
                "confirmPassword": "SecureP@ssword123",
                "phone": "+57123456789",
                "address": "Carrera 7 #45-89",
                "locality": "Medellín"
            }
        }
    }

class BaseUserOut(BaseModel):
    id: str = Field(..., description="User's unique identifier")
    name: str
    email: EmailStr
    phone: str
    address: str
    userType: UserType
    createdAt: datetime
    updatedAt: datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "65b4f50a-b8c6-4d04-8e54-730675247781",
                "name": "Carlos Herrera",
                "email": "carlos@example.com",
                "phone": "+573001234567",
                "address": "Calle 123 #45-67",
                "userType": "owner",
                "createdAt": "2025-07-13T12:34:56.789Z",
                "updatedAt": "2025-07-13T13:00:00.000Z"
            }
        }
    }

class OwnerOut(BaseUserOut):
    pass

class ClinicOut(BaseUserOut):
    locality: str = Field(..., description="City or municipality where the clinic is located")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "65b4f50a-b8c6-4d04-8e54-730675247781",
                "name": "Clínica Vida",
                "email": "contacto@vidaclinic.com",
                "phone": "+57123456789",
                "address": "Carrera 7 #45-89",
                "userType": "clinic",
                "locality": "Medellín",
                "createdAt": "2025-07-13T12:34:56.789Z",
                "updatedAt": "2025-07-13T13:00:00.000Z"
            }
        }
    }

class BaseUserUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Updated full name")
    email: Optional[EmailStr] = Field(None, description="Updated email address")
    phone: Optional[str] = Field(None, description="Updated phone number")
    address: Optional[str] = Field(None, description="Updated address")

    @field_validator("name")
    def validate_name(cls, value):
        if value:
            return validate_name_data(value)

    @field_validator("phone", mode="before")
    def validate_phone(cls, value):
        if value:
            return validate_phone_data(value)

    @field_validator("address")
    def validate_address(cls, value):
        if value:
            return validate_address_data(value)
    
    @field_validator("email", mode="before")
    def validate_email(cls, value):
        if value:
            return validate_email_data(value)

class OwnerUpdate(BaseUserUpdate):
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Carlos Andrés",
                "email": "carlos.a@example.com",
                "phone": "+573002223344",
                "address": "Calle 45 #67-89"
            }
        }
    }

class ClinicUpdate(BaseUserUpdate):
    locality: Optional[str] = Field(None, description="Updated locality")

    @field_validator("locality")
    def validate_locality(cls, value):
        if value:
            return validate_locality_data(value)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Clínica Esperanza",
                "email": "esperanza@clinic.co",
                "phone": "+57111222333",
                "address": "Carrera 9 #100-20",
                "locality": "Bogotá"
            }
        }
    }

class BaseRegisterResponse(BaseModel):
    success: bool
    token: str = Field(..., description="JWT access token")

class OwnerRegisterResponse(BaseRegisterResponse):
    user: OwnerOut

class ClinicRegisterResponse(BaseRegisterResponse):
    user: ClinicOut