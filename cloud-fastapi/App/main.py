from contextlib import asynccontextmanager
from fastapi import FastAPI
from . import mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo.connect()
    try:
        yield
    finally:
        mongo.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "ok"}
