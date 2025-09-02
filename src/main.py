
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Lifespan context (startup + shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

# FastAPI app
app = FastAPI(
    title="YouTube IR System",
    description="API for fetching and searching latest YouTube videos",
    lifespan=lifespan,
)

@app.get("/")
async def root():
    return {"message": "Welcome to YouTube IR System API"}

