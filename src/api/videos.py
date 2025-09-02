from fastapi import APIRouter, Query, Request
from src.firebase_utils import get_firestore
from src.models.schemas import VideoResponse, Video
from src.core.rate_limiter import limiter

router = APIRouter()

@router.get("/videos", response_model=VideoResponse)
@limiter.limit("10/minute") 
async def get_videos(
    request: Request,
    limit: int = Query(10, ge=1, le=50, description="Number of videos per page"),
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
):
    """
    Get videos stored in Firestore with pagination, sorted by publishedAt desc.
    """
    db = get_firestore()
    videos_ref = (
        db.collection("videos")
        .order_by("publishedAt", direction="DESCENDING")
        .limit(limit)
    )

    offset = (page - 1) * limit
    docs = list(videos_ref.stream())

    if offset > 0:
        docs = docs[offset: offset + limit]

    results = [Video(**doc.to_dict()) for doc in docs]

    return VideoResponse(
        page=page,
        limit=limit,
        count=len(results),
        videos=results,
    )
