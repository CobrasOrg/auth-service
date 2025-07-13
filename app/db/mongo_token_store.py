from pymongo import ASCENDING
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from motor.motor_asyncio import AsyncIOMotorDatabase

REV_TOKENS_COLLECTION = "revoked_tokens"

class MongoRevokedTokenStore:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[REV_TOKENS_COLLECTION]

    async def init_indexes(self):
        await self.collection.create_index(
            [("expiresAt", ASCENDING)],
            expireAfterSeconds=0
        )

    async def revoke(self, token: str, expires_at: datetime):
        try:
            await self.collection.insert_one({
                "_id": token,
                "expiresAt": expires_at
            })
        except DuplicateKeyError:
            pass

    async def is_revoked(self, token: str) -> bool:
        doc = await self.collection.find_one({"_id": token})
        return doc is not None

    async def reset(self):
        await self.collection.delete_many({})
