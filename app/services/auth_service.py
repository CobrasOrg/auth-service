from datetime import datetime, timezone
from fastapi import status, HTTPException

from app.db.memory import db
from app.core.security import hash_password, verify_password
from app.core.tokens import create_reset_token, verify_token, revoke_token, TokenType
from app.utils.email import test_password_reset_email
from app.utils.response_builder import build_auth_response, build_base_response, build_base_response

from app.schemas.user import (
    UserType,
    OwnerRegister,
    ClinicRegister
)

def register_user(user_data: OwnerRegister | ClinicRegister, user_type: UserType):
    if db.get_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    
    hashed_password = hash_password(user_data.password.get_secret_value())
    
    user_info = user_data.model_dump(exclude={"password", "confirmPassword"})
    user_info["email"] = user_data.email.strip().lower()

    now = datetime.now(timezone.utc)

    user_info["createdAt"] = now
    user_info["updatedAt"] = now
    user_info["userType"] = user_type

    if user_type == UserType.CLINIC and isinstance(user_data, ClinicRegister):
        user_info["locality"] = user_data.locality

    created = db.create({**user_info, "password": hashed_password})

    return build_auth_response(created)

def authenticate_user(email: str, password: str):
    user = db.get_by_email(email.strip().lower())
    
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )
        
    return build_auth_response(user)

def update_password_with_token(user_id: str, new_password: str):
    user = db.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    new_hashed = hash_password(new_password)
    db.update(user_id, {"password": new_hashed})
    return build_base_response(message="Password updated successfully.")

def change_password(user: dict, current_password: str, new_password: str):
    if not verify_password(current_password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect."
        )
    
    new_hashed = hash_password(new_password)
    db.update(user["id"], {"password": new_hashed})
    return build_base_response(message="Password changed successfully.")

def get_user_by_email(email: str):
    user = db.get_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user

def verify_user_token(token: str) -> dict:
    payload = verify_token(token, TokenType.ACCESS)
    user_id = payload.get("sub")
    user_type = payload.get("userType")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )

    user = db.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found."
        )

    return {
        "success": True,
        "user_id": user_id,
        "user_type": user_type
    }

def initiate_password_reset(email: str) -> dict:
    try:
        user = get_user_by_email(email)
        reset_token = create_reset_token(user["id"])
        test_password_reset_email(user["email"], reset_token)
    except HTTPException:
        # If user not found, we still return success to prevent email enumeration
        pass
    except Exception as e:
        pass

    return build_base_response(message="Password reset email sent.")

def reset_password(token: str, new_password: str) -> dict:
    payload = verify_token(token, TokenType.RESET)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload."
        )

    result = update_password_with_token(user_id, new_password)
    revoke_token(token)
    return result

def logout_user(token: str) -> dict:
    if not revoke_token(token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token or already expired."
        )
    return build_base_response(message="Logged out successfully.")
