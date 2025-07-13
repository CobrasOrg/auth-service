from fastapi import APIRouter, Depends

from app.db.mongo import MongoUserDB
from app.schemas.auth import BaseResponse
from app.core.auth import get_current_user
from app.db.dependencies import get_user_db
from app.schemas.user import OwnerUpdate, OwnerOut, ClinicUpdate, ClinicOut
from app.services.user_service import get_user_profile, update_user_profile, delete_user_account

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/profile", response_model=OwnerOut | ClinicOut)
async def get_profile(
    current_user: dict = Depends(get_current_user),
    user_db: MongoUserDB = Depends(get_user_db),
):
    return await get_user_profile(current_user, user_db)


@router.patch("/profile", response_model=OwnerOut | ClinicOut)
async def update_profile(
    data: OwnerUpdate | ClinicUpdate,
    current_user: dict = Depends(get_current_user),
    user_db: MongoUserDB = Depends(get_user_db),
):
    updates = data.model_dump(exclude_unset=True)
    return await update_user_profile(current_user, updates, user_db)

@router.delete("/account", response_model=BaseResponse)
async def delete_account(
    current_user: dict = Depends(get_current_user),
    user_db: MongoUserDB = Depends(get_user_db),
):
    return await delete_user_account(current_user, user_db)
