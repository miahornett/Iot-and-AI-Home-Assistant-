from contextlib import asynccontextmanager
from fastapi import FastAPI
import mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo.connect()
    try:
        yield
    finally:
        mongo.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello from MongoDB-connected FastAPI!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/test-write")
async def test_write():
    database = mongo.db()
    result = await database["test"].insert_one({"hello": "world"})
    return {"inserted_id": str(result.inserted_id)}