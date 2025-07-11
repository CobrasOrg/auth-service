from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

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
    
class OwnerRegister(BaseUserRegister):
    pass

class ClinicRegister(BaseUserRegister):
    locality: str

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
    
class OwnerUpdate(BaseUserUpdate):
    pass

class ClinicUpdate(BaseUserUpdate):
    locality: Optional[str] = None

class BaseRegisterResponse(BaseModel):
    success: bool
    token: str

class OwnerRegisterResponse(BaseRegisterResponse):
    user: OwnerOut

class ClinicRegisterResponse(BaseRegisterResponse):
    user: ClinicOut