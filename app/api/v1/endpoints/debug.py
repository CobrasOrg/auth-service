from fastapi import APIRouter, Depends, HTTPException
from app.db.mongo import MongoUserDB
from app.db.dependencies import get_user_db
from app.core.tokens import create_reset_token
from app.core.config import settings

from app.schemas.auth import ForgotPasswordRequest

router = APIRouter(prefix="/debug", tags=["debug"])

@router.post("/reset-token")
async def generate_reset_token_test(request: ForgotPasswordRequest, user_db: MongoUserDB = Depends(get_user_db)):
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    user = await user_db.get_by_email(request.email.strip().lower())
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_reset_token(str(user["id"]))
    return {"token": token}
