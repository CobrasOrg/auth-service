from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, model_validator

from app.utils.validators import (
    validate_password_data, validate_name_data, validate_phone_data, 
    validate_address_data, validate_email_data, validate_locality_data, validate_confirm_password
)

class UserType(str, Enum):
    OWNER = "owner"
    CLINIC = "clinic"

class BaseUserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirmPassword: str
    phone: str
    address: str

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
    pass

class ClinicRegister(BaseUserRegister):
    locality: str

    @field_validator("locality")
    def validate_locality(cls, value):
        return validate_locality_data(value)

class BaseUserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    address: str
    userType: UserType
    createdAt: datetime
    updatedAt: datetime

class OwnerOut(BaseUserOut):
    pass

class ClinicOut(BaseUserOut):
    locality: str

class BaseUserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

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
    pass

class ClinicUpdate(BaseUserUpdate):
    locality: Optional[str] = None

    @field_validator("locality")
    def validate_locality(cls, value):
        if value:
            return validate_locality_data(value)

class BaseRegisterResponse(BaseModel):
    success: bool
    token: str

class OwnerRegisterResponse(BaseRegisterResponse):
    user: OwnerOut

class ClinicRegisterResponse(BaseRegisterResponse):
    user: ClinicOut