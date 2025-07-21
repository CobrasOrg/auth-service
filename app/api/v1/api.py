from fastapi import APIRouter

from app.api.v1.endpoints import auth, user
from app.api.v1.endpoints import debug
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)

if settings.DEBUG:
    api_router.include_router(debug.router)