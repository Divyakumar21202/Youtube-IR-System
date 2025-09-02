
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.schedular import app_scheduler

# Lifespan context (startup + shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    app_scheduler.start()
    print("FastAPI app started and scheduler is running")
    yield
    app_scheduler.shutdown()
    print("Scheduler stopped")

# FastAPI app
app = FastAPI(
    title="YouTube IR System",
    description="API for fetching and searching latest YouTube videos",
    lifespan=lifespan,
)

@app.get("/")
async def root():
    return {"message": "Welcome to YouTube IR System API"}

