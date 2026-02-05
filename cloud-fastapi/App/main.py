from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import HTTPException
import mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo.connect()
    try:
        # Optional: do a quick ping on startup to surface errors in logs
        database = mongo.db()
        await database.command("ping")
        print("MongoDB ping ok")
        yield
    finally:
        mongo.close()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/db-check")
async def db_check():
    try:
        database = mongo.db()
        await database.command("ping")

        col = database["render_smoketest"]
        write = await col.insert_one({"source": "render", "ok": True})
        doc = await col.find_one({"_id": write.inserted_id})

        return {
            "mongo_ping": "ok",
            "db": database.name,
            "inserted_id": str(write.inserted_id),
            "roundtrip_ok": doc is not None,
        }
    except Exception as e:
        # Return the actual error so we can diagnose immediately
        raise HTTPException(status_code=500, detail=str(e))
