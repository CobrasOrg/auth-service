from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PetMatch Authentication API"
    VERSION: str = "1.0.7"
    DESCRIPTION: str = "PetMatch Authentication and User Management API"
    DEBUG: bool
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    RESET_TOKEN_EXPIRE_MINUTES: int
    
    # Email Configuration
    GMAIL_USER: str
    GMAIL_PASS: str
    EMAIL_FROM_NAME: str = "PetMatch"
    EMAIL_TEMPLATES_DIR: str = "app/templates"
    
    # Frontend URLs
    FRONTEND_URL: str
    RESET_PASSWORD_URL: str
    
    # Database
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "petmatchDB"
    TEST_DB_NAME: str = "petmatchDB_test"
    
    # CORS
    BACKEND_CORS_ORIGINS: str | List[str] = ["*"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @field_validator("GMAIL_USER", mode="before")
    @classmethod
    def validate_gmail_user(cls, v: str) -> str:
        if v and "@" not in v:
            raise ValueError("GMAIL_USER must be a valid email address")
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()