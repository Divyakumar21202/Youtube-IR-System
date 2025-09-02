from fastapi import APIRouter
from src.api import search,videos

# Define App Router
app_router = APIRouter()

# Added Search router in App Router
app_router.include_router(search.router)


# Added Videos Router in App Router
app_router.include_router(videos.router)