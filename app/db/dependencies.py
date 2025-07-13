from app.db.mongo import MongoUserDB
from app.db.database import get_database
from app.db.mongo_token_store import MongoRevokedTokenStore

_user_db_instance: MongoUserDB | None = None
_revoked_token_store: MongoRevokedTokenStore | None = None

async def get_user_db() -> MongoUserDB:
    global _user_db_instance
    if not _user_db_instance:
        db = await get_database()
        _user_db_instance = MongoUserDB(db)
        await _user_db_instance.init_indexes()
    return _user_db_instance

async def get_revoked_token_store() -> MongoRevokedTokenStore:
    global _revoked_token_store
    if not _revoked_token_store:
        db = await get_database()
        _revoked_token_store = MongoRevokedTokenStore(db)
        await _revoked_token_store.init_indexes()
    return _revoked_token_store
