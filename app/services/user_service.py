from fastapi import HTTPException, status

from app.db.mongo import MongoUserDB
from app.schemas.user import UserType, Locality
from app.utils.response_builder import get_user_output_model

async def get_user_profile(user: dict, user_db: MongoUserDB) -> dict:
    db_user = await user_db.get_by_id(user["id"])
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    return get_user_output_model(db_user)

async def update_user_profile(user: dict, updates: dict, user_db: MongoUserDB) -> dict:
    if user["userType"] != UserType.CLINIC and "locality" in updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only clinics can update 'locality'."
        )

    try:
        updated_user = await user_db.update(user["id"], updates)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return get_user_output_model(updated_user)

async def delete_user_account(user: dict, user_db: MongoUserDB) -> dict:
    deleted = await user_db.delete(user["id"])
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
        
    return {
        "success": True,
        "message": "Account deleted successfully."
    }
