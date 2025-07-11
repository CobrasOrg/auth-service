from fastapi import APIRouter, status, HTTPException

from app.db.memory import db
from app.core.security import verify_password
from app.utils.helpers import build_access_token, build_user_out, register_user

from app.schemas.auth import UserLoginRequest, UserLoginResponse

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
    
@router.post("/register/owner", response_model=OwnerRegisterResponse, status_code=201)
def register_owner(data: OwnerRegister):
    result = register_user(data, UserType.OWNER)
    return result

@router.post("/register/clinic", response_model=ClinicRegisterResponse, status_code=201)
def register_clinic(data: ClinicRegister):
    result = register_user(data, UserType.CLINIC)
    return result