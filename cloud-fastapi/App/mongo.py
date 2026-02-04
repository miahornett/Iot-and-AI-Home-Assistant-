import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

_client: AsyncIOMotorClient | None = None

def connect() -> None:
    """Initialize the global Mongo client."""
    global _client
    uri = os.environ["MONGODB_URI"]
    _client = AsyncIOMotorClient(uri)

def close() -> None:
    """Close the global Mongo client."""
    global _client
    if _client is not None:
        _client.close()
        _client = None

def db() -> AsyncIOMotorDatabase:
    """Get the default database from the Mongo URI path."""
    if _client is None:
        raise RuntimeError("Mongo client not initialized. Call connect() first.")
    database = _client.get_default_database()
    if database is None:
        raise RuntimeError(
            "No default database set in MONGODB_URI. Add '/<db_name>' to the URI."
        )
    return database
