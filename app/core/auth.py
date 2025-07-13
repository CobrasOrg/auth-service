from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.db.mongo import MongoUserDB
from app.core.tokens import verify_token, TokenType
from app.db.mongo_token_store import MongoRevokedTokenStore
from app.db.dependencies import get_user_db, get_revoked_token_store

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_db: MongoUserDB = Depends(get_user_db),
    store: MongoRevokedTokenStore = Depends(get_revoked_token_store),
):
    payload = await verify_token(token, TokenType.ACCESS, store)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    user = await user_db.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    return user