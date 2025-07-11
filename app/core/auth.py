from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.db.memory import db
from app.core.tokens import verify_token, TokenType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token, TokenType.ACCESS)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    user = db.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    return user