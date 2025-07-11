from fastapi import APIRouter, status, Depends, HTTPException

from app.db.memory import db
from app.core.auth import get_current_user, oauth2_scheme
from app.utils.email import send_password_reset_email, test_password_reset_email
from app.core.security import hash_password, verify_password
from app.core.tokens import create_reset_token, verify_token, revoke_token, TokenType
from app.utils.helpers import build_access_token, build_user_out, register_user

from app.schemas.auth import (
    ResetPasswordRequest, ChangePasswordRequest, ForgotPasswordRequest,
    BaseAuthResponse, UserLoginRequest, UserLoginResponse
)

from app.schemas.user import(
    UserType,
    OwnerRegister, OwnerRegisterResponse,
    ClinicRegister, ClinicRegisterResponse
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginResponse)
def login(user: UserLoginRequest):
    db_user = db.get_by_email(user.email.strip().lower())

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token = build_access_token(db_user)
    user_out = build_user_out(db_user)

    return {
        "success": True,
        "user": user_out,
        "token": token
    }

@router.post("/logout", response_model=BaseAuthResponse)
def logout(token: str = Depends(oauth2_scheme)):
    revoked = revoke_token(token)

    if not revoked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token or already expired."
        )

    return {
        "success": True,
        "message": "Logged out successfully."
    }
    
@router.post("/register/owner", response_model=OwnerRegisterResponse, status_code=201)
def register_owner(data: OwnerRegister):
    result = register_user(data, UserType.OWNER)
    return result

@router.post("/register/clinic", response_model=ClinicRegisterResponse, status_code=201)
def register_clinic(data: ClinicRegister):
    result = register_user(data, UserType.CLINIC)
    return result

@router.post("/forgot-password", response_model=BaseAuthResponse)
def forgot_password(request: ForgotPasswordRequest):
    user = db.get_by_email(request.email)
    
    if user:
            try:
                reset_token = create_reset_token(user["id"])
                
                #send_password_reset_email(user["email"], reset_token)
                test_password_reset_email(user["email"], reset_token)
            except Exception as e:
                pass

    return {
        "success": True,
        "message": "Password reset email sent."
    }

@router.post("/reset-password", response_model=BaseAuthResponse)
def reset_password(data: ResetPasswordRequest):
    payload = verify_token(data.token, TokenType.RESET)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload."
        )

    new_hashed = hash_password(data.newPassword)
    db.update(user_id, {"password": new_hashed})

    revoke_token(data.token)

    return {
        "success": True, 
        "message": "Password has been updated successfully."
    }

@router.put("/change-password", response_model=BaseAuthResponse)
def change_password(data: ChangePasswordRequest, current_user: dict = Depends(get_current_user)):
    if not verify_password(data.currentPassword, current_user["password"]):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is not correct."
        )

    new_hashed = hash_password(data.newPassword)
    db.update(current_user["id"], {"password": new_hashed})

    return {
        "success": True, 
        "message": "Password has been updated successfully."
    }