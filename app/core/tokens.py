from enum import Enum
from jose import jwt
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