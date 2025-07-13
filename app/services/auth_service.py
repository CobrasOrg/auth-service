from datetime import datetime, timezone
from fastapi import status, HTTPException

from app.db.mongo import MongoUserDB
from app.utils.email import send_password_reset_email
from app.db.mongo_token_store import MongoRevokedTokenStore
from app.core.security import hash_password, verify_password
from app.utils.response_builder import build_auth_response, build_base_response
from app.core.tokens import create_reset_token, verify_token, revoke_token, TokenType

from app.schemas.user import(
    UserType,
    OwnerRegister,
    ClinicRegister
)

async def register_user(user_data: OwnerRegister | ClinicRegister, user_type: UserType, user_db: MongoUserDB):
    existing = await user_db.get_by_email(user_data.email)
    if existing:
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

    created = await user_db.create({**user_info, "password": hashed_password})
    return build_auth_response(created)

async def authenticate_user(email: str, password: str, user_db: MongoUserDB):
    user = await user_db.get_by_email(email.strip().lower())
    
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )
        
    return build_auth_response(user)

async def update_password_with_token(user_id: str, new_password: str, user_db: MongoUserDB):
    user = await user_db.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    new_hashed = hash_password(new_password)
    await user_db.update(user_id, {"password": new_hashed})
    return build_base_response(message="Password updated successfully.")

async def change_password(user: dict, current_password: str, new_password: str, user_db: MongoUserDB):
    if not verify_password(current_password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect."
        )
    
    new_hashed = hash_password(new_password)
    await user_db.update(user["id"], {"password": new_hashed})
    return build_base_response(message="Password changed successfully.")

async def get_user_by_email(email: str, user_db: MongoUserDB):
    user = await user_db.get_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user

async def verify_user_token(
    token: str,
    user_db: MongoUserDB,
    store: MongoRevokedTokenStore,
) -> dict:
    payload = await verify_token(token, TokenType.ACCESS, store)
    user_id = payload.get("sub")
    user_type = payload.get("userType")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )

    user = await user_db.get_by_id(user_id)
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


async def initiate_password_reset(email: str, user_db: MongoUserDB) -> dict:
    try:
        user = await get_user_by_email(email, user_db)
        reset_token = create_reset_token(user["id"])
        send_password_reset_email(user["email"], reset_token)
    except HTTPException:
        pass  #Prevent email enumeration
    except Exception:
        pass

    return build_base_response(message="Password reset email sent.")

async def reset_password(
    token: str,
    new_password: str,
    user_db: MongoUserDB,
    store: MongoRevokedTokenStore,
) -> dict:
    payload = await verify_token(token, TokenType.RESET, store)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload."
        )

    result = await update_password_with_token(user_id, new_password, user_db)
    await revoke_token(token, store)
    return result

async def logout_user(token: str, store: MongoRevokedTokenStore) -> dict:
    success = await revoke_token(token, store)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token or already expired."
        )
    return build_base_response(message="Logged out successfully.")

