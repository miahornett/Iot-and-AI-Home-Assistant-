# mongo.py
import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

_client: AsyncIOMotorClient | None = None

def connect() -> None:
    global _client
    if _client is None:
        uri = os.environ["MONGODB_URI"]
        _client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=10000)

def close() -> None:
    global _client
    if _client:
        _client.close()
        _client = None

def db() -> AsyncIOMotorDatabase:
    if _client is None:
        raise RuntimeError("Mongo client not initialized. Call connect() first.")
    database = _client.get_default_database()
    if database is None:
        raise RuntimeError("No default database set in MONGODB_URI.")
    return database
