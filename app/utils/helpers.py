from datetime import datetime, timezone
from fastapi import status, HTTPException

from app.db.memory import db
from app.core.security import hash_password
from app.core.tokens import create_access_token

from app.schemas.user import (
    UserType,
    OwnerRegister, OwnerOut,
    ClinicRegister, ClinicOut
)

def build_access_token(user: dict):
    token_data = {"sub": user["id"], "userType": user["userType"]} 
    return create_access_token(token_data)

def build_user_out(user: dict):
    user_copy = user.copy()
    user_copy.pop("password", None)

    if user_copy["userType"] == UserType.CLINIC:
        return ClinicOut(**user_copy)
    else:
        return OwnerOut(**user_copy)

def register_user(user_data: OwnerRegister | ClinicRegister, user_type: UserType):
    if db.get_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    
    now = datetime.now(timezone.utc)

    user_info = {
        "name": user_data.name,
        "email": user_data.email,
        "password": hash_password(user_data.password),
        "phone": user_data.phone,
        "address": user_data.address,
        "userType": user_type,
        "createdAt": now,
        "updatedAt": now
    }

    if user_type == UserType.CLINIC and isinstance(user_data, ClinicRegister):
        user_info["locality"] = user_data.locality

    created = db.create(user_info)

    token = build_access_token(created)
    user_out = build_user_out(created)

    return {
        "success": True,
        "user": user_out,
        "token": token
    }