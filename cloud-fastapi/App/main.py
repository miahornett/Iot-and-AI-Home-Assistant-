"""from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from . import mongo  # important: relative import

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo.connect()
    try:
        yield
    finally:
        mongo.close()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}
