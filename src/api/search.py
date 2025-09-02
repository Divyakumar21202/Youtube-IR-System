from fastapi import APIRouter, Query, Request
from src.firebase_utils import get_firestore
from src.core.nltk_tokenizer import nltk_tokenizer
from src.models.schemas import Video, VideoResponse
from src.core.rate_limiter import limiter

router = APIRouter()

@router.get("/search", response_model=VideoResponse)
@limiter.limit("100/minute") 
async def search_content(
    request: Request,
    query: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50)
):
    """
    Search videos by matching query tokens against pre-stored search tokens 
    in Firestore (title + description tokens). 
    Results are sorted by published date in descending order.
    """

    query_tokens = nltk_tokenizer(query)

    db = get_firestore()
    videos_ref = (
        db.collection("videos")
        .where("tokens", "array_contains_any", query_tokens[:10])  # Firestore limit
        .order_by("publishedAt", direction="DESCENDING")
        .limit(limit * page)
    )

    docs = list(videos_ref.stream())

    # Handle pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_docs = docs[start:end]

    # Convert Firestore docs into Pydantic Video models
    results = [Video(**doc.to_dict()) for doc in paginated_docs]

    return VideoResponse(
        page=page,
        limit=limit,
        count=len(results),
        videos=results,
    )
