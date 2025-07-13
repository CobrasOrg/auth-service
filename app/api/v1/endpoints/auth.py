from fastapi import APIRouter, Depends

from app.core.auth import get_current_user, oauth2_scheme

from app.services.auth_service import (
    verify_user_token,
    register_user, authenticate_user, logout_user,
    change_password,  initiate_password_reset, reset_password
)

from app.schemas.auth import (
    ResetPasswordRequest, ChangePasswordRequest, ForgotPasswordRequest,
    BaseResponse, UserLoginRequest, UserLoginResponse, TokenVerificationResponse
)

from app.schemas.user import(
    UserType,
    OwnerRegister, OwnerRegisterResponse,
    ClinicRegister, ClinicRegisterResponse
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginResponse)
def login(user: UserLoginRequest):
    return authenticate_user(user.email, user.password.get_secret_value())

@router.post("/logout", response_model=BaseResponse)
def logout(token: str = Depends(oauth2_scheme)):
    return logout_user(token)
    
@router.post("/register/owner", response_model=OwnerRegisterResponse, status_code=201)
def register_owner(data: OwnerRegister):
    result = register_user(data, UserType.OWNER)
    return result

@router.post("/register/clinic", response_model=ClinicRegisterResponse, status_code=201)
def register_clinic(data: ClinicRegister):
    result = register_user(data, UserType.CLINIC)
    return result

@router.post("/forgot-password", response_model=BaseResponse)
def forgot_password(request: ForgotPasswordRequest):
    return initiate_password_reset(request.email)

@router.post("/reset-password", response_model=BaseResponse)
def reset_password_endpoint(data: ResetPasswordRequest):
    return reset_password(data.token, data.newPassword.get_secret_value())

@router.put("/change-password", response_model=BaseResponse)
def change_password_endpoint(data: ChangePasswordRequest, current_user: dict = Depends(get_current_user)):
    return change_password(current_user, data.currentPassword.get_secret_value(), data.newPassword.get_secret_value())

@router.post("/verify-token", response_model=TokenVerificationResponse)
def verify_token_API(token: str = Depends(oauth2_scheme)):
    return verify_user_token(token)