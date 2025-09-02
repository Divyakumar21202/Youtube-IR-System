
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import src.api.routes as routes
from src.firebase_utils import close_firebase, init_firebase
from src.core.schedular import app_scheduler
from src.core.logger import logger
from src.core.rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# -----------------------------
# Lifespan context (startup + shutdown)
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown tasks:
    - Initialize Firebase
    - Start scheduler
    - Attach rate limiter
    """
    try:
        init_firebase()  # await if async
        app_scheduler.start()
        logger.info("FastAPI app started and scheduler is running")

        # Attach rate limiter to app state
        app.state.limiter = limiter

        yield
    finally:
        close_firebase()
        app_scheduler.shutdown()
        logger.info("Scheduler stopped")

# -----------------------------
# FastAPI app initialization
# -----------------------------
app = FastAPI(
    title="YouTube IR System",
    description="API for fetching and searching latest YouTube videos",
    lifespan=lifespan,
)

# Attach SlowAPI middleware for rate limiting
app.add_middleware(SlowAPIMiddleware)

# Include API routes
app.include_router(router=routes.app_router)

# -----------------------------
# Endpoints
# -----------------------------
@app.get("/")
async def root():
    """Welcome message endpoint"""
    return {"message": "Welcome to YouTube IR System API"}


@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "ok"}

# -----------------------------
# Exception handlers
# -----------------------------
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    Global handler for rate limit exceptions
    """
    logger.warning(f"Rate limit exceeded: {request.client.host}")
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )
