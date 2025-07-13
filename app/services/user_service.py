from fastapi import HTTPException, status

from app.db.memory import db
from app.schemas.user import UserType
from app.utils.response_builder import get_user_output_model

def get_user_profile(user: dict) -> dict:
    return get_user_output_model(user)

def update_user_profile(user: dict, updates: dict) -> dict:
    if user["userType"] != UserType.CLINIC and "locality" in updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only clinics can update 'locality'."
        )

    try:
        updated_user = db.update(user["id"], updates)
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

    return get_user_output_model(updated_user)

def delete_user_account(user: dict) -> dict:
    deleted = db.delete(user["id"])
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request."
        )
    
    return {
        "success": True,
        "message": "Account deleted successfully."
    }