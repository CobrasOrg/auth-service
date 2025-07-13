from fastapi import APIRouter, Depends

from app.schemas.auth import BaseResponse
from app.core.auth import get_current_user
from app.services.user_service import get_user_profile, update_user_profile, delete_user_account

from app.schemas.user import(
    OwnerUpdate, OwnerOut,
    ClinicUpdate, ClinicOut
)

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/profile", response_model=OwnerOut | ClinicOut)
def get_profile(current_user: dict = Depends(get_current_user)):
    return get_user_profile(current_user)

@router.patch("/profile", response_model=OwnerOut | ClinicOut)
def update_profile(data: OwnerUpdate | ClinicUpdate, current_user: dict = Depends(get_current_user)):
    updates = data.model_dump(exclude_unset=True)
    return update_user_profile(current_user, updates)

@router.delete("/account", response_model=BaseResponse)
def delete_account(current_user: dict = Depends(get_current_user)):
    return delete_user_account(current_user)