from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.db.mongo import MongoUserDB
from app.api.v1.api import api_router
from app.db.mongo_token_store import MongoRevokedTokenStore
from app.core.exceptions import validation_exception_handler, http_exception_handler
from app.db.database import connect_to_mongo, close_mongo_connection, get_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    db = await get_database()

    # Token cleanup index
    token_store = MongoRevokedTokenStore(db)
    await token_store.init_indexes()

    # User email/id indexes
    user_db = MongoUserDB(db)
    await user_db.init_indexes()

    yield

    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url=f"{settings.API_V1_STR}/docs" ,
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Custom exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

#Prometheus instrumentation
Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    excluded_handlers=["/api/v1/metrics"],
).instrument(app).expose(app, endpoint="/api/v1/metrics")

@app.get(
    "/",
    summary="API welcome message",
    description="Returns a welcome message and the current version of the API.",
    response_description="Welcome message with project name and version",
    responses={
        200: {
            "description": "Welcome response",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Welcome to PetMatch Authentication API",
                        "version": "1.0.0"
                    }
                }
            }
        }
    },
)
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION
    }

@app.get(
    "/health",
    summary="Health check",
    description="Used to check if the API is running and responsive.",
    response_description="Health status and API version",
    responses={
        200: {
            "description": "Healthy response",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "version": "1.0.0"
                    }
                }
            }
        }
    },
)
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 