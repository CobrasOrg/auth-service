from enum import Enum
from jose import jwt
from uuid import uuid4
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from jose.exceptions import ExpiredSignatureError, JWTError

from app.core.config import settings
from app.db.mongo_token_store import MongoRevokedTokenStore

class TokenType(str, Enum):
    ACCESS = "access"
    RESET = "reset"

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
RESET_TOKEN_EXPIRE_MINUTES = settings.RESET_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": TokenType.ACCESS, "jti": str(uuid4()), "iat": datetime.now(timezone.utc)})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_reset_token(user_id: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user_id, "exp": expire, "type": TokenType.RESET}
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def verify_token(token: str, expected_type: TokenType, store: MongoRevokedTokenStore) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if await store.is_revoked(token):
            raise HTTPException(status_code=401, detail="Token has been revoked.")

        if not payload.get("sub"):
            raise HTTPException(status_code=401, detail="Invalid token payload.")

        if payload.get("type") != expected_type:
            raise HTTPException(status_code=403, detail="Invalid token type.")

        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail=f"{expected_type.value.capitalize()} token has expired.")
    
    except JWTError:
        raise HTTPException(status_code=401, detail=f"Invalid {expected_type.value.capitalize()} token.")

async def revoke_token(token: str, store: MongoRevokedTokenStore) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            await store.revoke(token, expires_at)
            return True
    except JWTError:
        pass
    return False
