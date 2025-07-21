from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def get_database() -> AsyncIOMotorClient:
    if settings.DEBUG:
        return db.client[settings.TEST_DB_NAME]
    return db.client[settings.MONGODB_DB_NAME]

async def connect_to_mongo():
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=10000)
        await client.server_info()
        db.client = client
    except ServerSelectionTimeoutError:
        fallback_client = AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=10000)
        await fallback_client.server_info()
        db.client = fallback_client

async def close_mongo_connection():
    if db.client:
        db.client.close()