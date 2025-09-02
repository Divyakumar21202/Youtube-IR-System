
from contextlib import asynccontextmanager
from fastapi import FastAPI
import src.api.routes as routes
from src.firebase_utils import close_firebase, init_firebase
from src.core.schedular import app_scheduler

# Lifespan context (startup + shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    app_scheduler.start()
    print("FastAPI app started and scheduler is running")
    init_firebase()
    yield
    close_firebase()
    app_scheduler.shutdown()
    print("Scheduler stopped")

# FastAPI app
app = FastAPI(
    title="YouTube IR System",
    description="API for fetching and searching latest YouTube videos",
    lifespan=lifespan,
)

app.include_router(router=routes.app_router)

@app.get("/")
async def root():
    return {"message": "Welcome to YouTube IR System API"}

