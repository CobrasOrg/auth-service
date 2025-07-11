from enum import Enum
from jose import jwt, JWTError
from fastapi import HTTPException
from jose.exceptions import ExpiredSignatureError
from datetime import datetime, timedelta, timezone

from app.core.config import settings

class TokenType(str, Enum):
    ACCESS = "access"

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": TokenType.ACCESS})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, expected_type: TokenType):    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if not payload.get("sub"):
            raise HTTPException(status_code=401, detail="Invalid token payload.")
        
        if payload.get("type") != expected_type:
            raise HTTPException(status_code=403, detail="Invalid token type.")
        
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail=f"{expected_type.value.capitalize()} token has expired.")
    
    except JWTError:
        raise HTTPException(status_code=401, detail=f"Invalid {expected_type.value.capitalize()} token.")