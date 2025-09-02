from fastapi import APIRouter
from src.api import search

# Define App Router
app_router = APIRouter()

# Added Search router in App Router
app_router.include_router(search.router)
