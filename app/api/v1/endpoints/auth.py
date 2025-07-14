from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.db.mongo import MongoUserDB
from app.core.auth import get_current_user, security
from app.db.mongo_token_store import MongoRevokedTokenStore
from app.db.dependencies import get_user_db, get_revoked_token_store

from app.services.auth_service import(
    verify_user_token,
    register_user, authenticate_user, logout_user,
    change_password,  initiate_password_reset, reset_password
)

from app.schemas.auth import(
    ResetPasswordRequest, ChangePasswordRequest, ForgotPasswordRequest,
    BaseResponse, UserLoginRequest, UserLoginResponse, TokenVerificationResponse
)

from app.schemas.user import(
    UserType,
    OwnerRegister, OwnerRegisterResponse,
    ClinicRegister, ClinicRegisterResponse
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/login",
    response_model=UserLoginResponse,
    summary="User login",
    description="Authenticates a user using their email and password and returns an access token.",
    responses={
        200: {"description": "User authenticated successfully"},
        401: {"description": "Invalid email or password"}
    }
)
async def login(user: UserLoginRequest, user_db: MongoUserDB = Depends(get_user_db)):
    return await authenticate_user(user.email, user.password.get_secret_value(), user_db)


@router.post(
    "/logout",
    response_model=BaseResponse,
    summary="Logout current user",
    description="Revokes the access token, effectively logging the user out.",
    responses={
        200: {
            "description": "Logged out successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Logged out successfully."
                    }
                }
            }
        },
        400: {"description": "Invalid token or already expired"},
    }
)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    store: MongoRevokedTokenStore = Depends(get_revoked_token_store),
):
    token = credentials.credentials
    return await logout_user(token, store)

@router.post(
    "/register/owner",
    response_model=OwnerRegisterResponse,
    status_code=201,
    summary="Register new owner",
    description="Registers a new pet owner with required profile information.",
    responses={
        201: {"description": "Owner registered successfully"},
        400: {"description": "Email already registered"}
    }
)
async def register_owner(data: OwnerRegister, user_db: MongoUserDB = Depends(get_user_db)):
    return await register_user(data, UserType.OWNER, user_db)


@router.post(
    "/register/clinic",
    response_model=ClinicRegisterResponse,
    status_code=201,
    summary="Register new clinic",
    description="Registers a new clinic user with required profile information and locality.",
    responses={
        201: {"description": "Clinic registered successfully"},
        400: {"description": "Email already registered"}
    }
)
async def register_clinic(data: ClinicRegister, user_db: MongoUserDB = Depends(get_user_db)):
    return await register_user(data, UserType.CLINIC, user_db)


@router.post(
    "/forgot-password",
    response_model=BaseResponse,
    summary="Send password reset email",
    description="Sends a password reset link to the provided email address if the user exists.",
    responses={
        200: {
            "description": "Password reset email sent",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Password reset email sent."
                    }
                }
            }
        },
        422: {"description": "Validation error"}
    }
)
async def forgot_password(request: ForgotPasswordRequest, user_db: MongoUserDB = Depends(get_user_db)):
    return await initiate_password_reset(request.email, user_db)


@router.post(
    "/reset-password",
    response_model=BaseResponse,
    summary="Reset password",
    description="Resets the user's password using a valid reset token.",
    responses={
        200: {"description": "Password reset successfully"},
        401: {"description": "Invalid or expired token"},
        404: {"description": "User not found"}
    }
)
async def reset_password_endpoint(
    data: ResetPasswordRequest,
    user_db: MongoUserDB = Depends(get_user_db),
    store: MongoRevokedTokenStore = Depends(get_revoked_token_store),
):
    return await reset_password(data.token, data.newPassword.get_secret_value(), user_db, store)


@router.put(
    "/change-password",
    response_model=BaseResponse,
    summary="Change password",
    description="Allows an authenticated user to change their password by providing the current one.",
    responses={
        200: {"description": "Password changed successfully"},
        401: {"description": "Current password is incorrect"}
    }
)
async def change_password_endpoint(
    data: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    user_db: MongoUserDB = Depends(get_user_db),
):
    return await change_password(current_user, data.currentPassword.get_secret_value(), data.newPassword.get_secret_value(), user_db)


@router.post(
    "/verify-token",
    response_model=TokenVerificationResponse,
    summary="Verify access token",
    description="Validates an access token and returns associated user information if it's valid.",
    responses={
        200: {"description": "Token is valid"},
        401: {"description": "Invalid or expired token"}
    }
)
async def verify_token_API(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_db: MongoUserDB = Depends(get_user_db),
    store: MongoRevokedTokenStore = Depends(get_revoked_token_store),
):
    token = credentials.credentials
    return await verify_user_token(token, user_db, store)

