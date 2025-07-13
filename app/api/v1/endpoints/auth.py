from fastapi import APIRouter, Depends

from app.db.mongo import MongoUserDB
from app.core.auth import get_current_user, oauth2_scheme
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

@router.post("/login", response_model=UserLoginResponse)
async def login(user: UserLoginRequest, user_db: MongoUserDB = Depends(get_user_db)):
    return await authenticate_user(user.email, user.password.get_secret_value(), user_db)

@router.post("/logout", response_model=BaseResponse)
async def logout(
    token: str = Depends(oauth2_scheme),
    store: MongoRevokedTokenStore = Depends(get_revoked_token_store),
):
    return await logout_user(token, store)

    
@router.post("/register/owner", response_model=OwnerRegisterResponse, status_code=201)
async def register_owner(data: OwnerRegister, user_db: MongoUserDB = Depends(get_user_db)):
    return await register_user(data, UserType.OWNER, user_db)

@router.post("/register/clinic", response_model=ClinicRegisterResponse, status_code=201)
async def register_clinic(data: ClinicRegister, user_db: MongoUserDB = Depends(get_user_db)):
    return await register_user(data, UserType.CLINIC, user_db)

@router.post("/forgot-password", response_model=BaseResponse)
async def forgot_password(request: ForgotPasswordRequest, user_db: MongoUserDB = Depends(get_user_db)):
    return await initiate_password_reset(request.email, user_db)

@router.post("/reset-password", response_model=BaseResponse)
async def reset_password_endpoint(
    data: ResetPasswordRequest,
    user_db: MongoUserDB = Depends(get_user_db),
    store: MongoRevokedTokenStore = Depends(get_revoked_token_store),
):
    return await reset_password(data.token, data.newPassword.get_secret_value(), user_db, store)


@router.put("/change-password", response_model=BaseResponse)
async def change_password_endpoint(
    data: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    user_db: MongoUserDB = Depends(get_user_db),
):
    return await change_password(current_user, data.currentPassword.get_secret_value(), data.newPassword.get_secret_value(), user_db)

@router.post("/verify-token", response_model=TokenVerificationResponse)
async def verify_token_API(
    token: str = Depends(oauth2_scheme),
    user_db: MongoUserDB = Depends(get_user_db),
    store: MongoRevokedTokenStore = Depends(get_revoked_token_store),
):
    return await verify_user_token(token, user_db, store)

