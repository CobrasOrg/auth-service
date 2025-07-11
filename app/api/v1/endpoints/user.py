from fastapi import APIRouter, Depends, status, HTTPException

from app.db.memory import db
from app.core.auth import get_current_user
from app.utils.helpers import build_user_out

from app.schemas.user import(
    UserType,
    OwnerUpdate, OwnerOut,
    ClinicUpdate, ClinicOut
)

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/profile", response_model=OwnerOut | ClinicOut)
def get_profile(current_user: dict = Depends(get_current_user)):
    return build_user_out(current_user)

@router.patch("/profile", response_model=OwnerOut | ClinicOut)
def update_profile(data: OwnerUpdate | ClinicUpdate, current_user: dict = Depends(get_current_user)):
    updates = data.model_dump(exclude_unset=True)

    if current_user["userType"] != UserType.CLINIC and "locality" in updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only clinics can update 'locality'."
        )
    try:
        updated_user = db.update(current_user["id"], updates)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request."
        )

    return build_user_out(updated_user)

@router.delete("/account")
def delete_account(current_user: dict = Depends(get_current_user)):
    deleted = db.delete(current_user["id"])
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request."
        )
    
    return {
        "success": True,
        "message": "Account deleted successfully."
    }