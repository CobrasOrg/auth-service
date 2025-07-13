from uuid import uuid4
from typing import Optional, List
from pymongo import ReturnDocument
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase

class MongoUserDB:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def init_indexes(self):
        await self.collection.create_index("email", unique=True)
        await self.collection.create_index("id", unique=True)

    async def reset(self):
        await self.collection.delete_many({})

    async def get_by_id(self, user_id: str) -> Optional[dict]:
        if not user_id:
            return None
        return await self.collection.find_one({"id": user_id})

    async def get_by_email(self, email: str) -> Optional[dict]:
        if not email:
            return None
        return await self.collection.find_one({"email": email.strip().lower()})

    async def create(self, user_data: dict) -> dict:
        if not user_data or "email" not in user_data:
            raise ValueError("User data must contain email.")

        email = user_data["email"].strip().lower()
        existing = await self.get_by_email(email)
        if existing:
            raise ValueError("Email already exists.")

        user_id = str(uuid4())
        now = datetime.now(timezone.utc)

        user_data_copy = user_data.copy()
        user_data_copy.update({
            "id": user_id,
            "email": email,
            "createdAt": now,
            "updatedAt": now
        })

        await self.collection.insert_one(user_data_copy)
        return user_data_copy

    async def get_all(self) -> List[dict]:
        cursor = self.collection.find({})
        return await cursor.to_list(length=None)

    async def update(self, user_id: str, updates: dict) -> Optional[dict]:
        if not user_id or not updates:
            return None

        updates = updates.copy()
        if "email" in updates:
            updates["email"] = updates["email"].strip().lower()

            existing = await self.get_by_email(updates["email"])
            if existing and existing["id"] != user_id:
                raise ValueError("Email already exists.")

        updates["updatedAt"] = datetime.now(timezone.utc)

        return await self.collection.find_one_and_update(
            {"id": user_id},
            {"$set": updates},
            return_document=ReturnDocument.AFTER
        )

    async def delete(self, user_id: str) -> Optional[dict]:
        if not user_id:
            return None
        return await self.collection.find_one_and_delete({"id": user_id})
