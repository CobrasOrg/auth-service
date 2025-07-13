from fastapi import APIRouter, Depends

from app.db.mongo import MongoUserDB
from app.schemas.auth import BaseResponse
from app.core.auth import get_current_user
from app.db.dependencies import get_user_db
from app.schemas.user import OwnerUpdate, OwnerOut, ClinicUpdate, ClinicOut
from app.services.user_service import get_user_profile, update_user_profile, delete_user_account

router = APIRouter(prefix="/user", tags=["user"])

@router.get(
    "/profile",
    response_model=OwnerOut | ClinicOut,
    summary="Get current user's profile",
    description="Returns the profile data of the currently authenticated user. The response varies depending on whether the user is an owner or a clinic.",
    responses={
        200: {"description": "Profile retrieved successfully"},
        401: {"description": "Unauthorized - Invalid or expired token"},
        404: {"description": "User not found"},
    }
)
async def get_profile(
    current_user: dict = Depends(get_current_user),
    user_db: MongoUserDB = Depends(get_user_db),
):
    return await get_user_profile(current_user, user_db)

@router.patch(
    "/profile",
    response_model=OwnerOut | ClinicOut,
    summary="Update current user's profile",
    description="Updates fields in the profile of the currently authenticated user. Clinic users can update the `locality` field; owners cannot.",
    responses={
        200: {"description": "Profile updated successfully"},
        400: {"description": "Bad request - unauthorized field or invalid input"},
        401: {"description": "Unauthorized - Invalid or expired token"},
        404: {"description": "User not found"}
    }
)
async def update_profile(
    data: OwnerUpdate | ClinicUpdate,
    current_user: dict = Depends(get_current_user),
    user_db: MongoUserDB = Depends(get_user_db),
):
    updates = data.model_dump(exclude_unset=True)
    return await update_user_profile(current_user, updates, user_db)

@router.delete(
    "/account",
    response_model=BaseResponse,
    summary="Delete user account",
    description="Deletes the account of the currently authenticated user. This action is irreversible.",
    responses={
        200: {
            "description": "Account deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Account deleted successfully"
                    }
                }
            }
        },
        401: {"description": "Unauthorized - Invalid or expired token"},
        404: {"description": "User not found or already deleted"}
    }
)
async def delete_account(
    current_user: dict = Depends(get_current_user),
    user_db: MongoUserDB = Depends(get_user_db),
):
    return await delete_user_account(current_user, user_db)
