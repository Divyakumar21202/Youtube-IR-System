import httpx
import asyncio
from datetime import datetime, timedelta, timezone
from src.firebase_utils import get_firestore
from firebase_admin import firestore
from src.core.nltk_tokenizer import nltk_tokenizer

# Todo: Replace with a fresh API key before final submission
YOUTUBE_API_KEY = "AIzaSyAkWeMtybNkHzvHlFCLueqX6f7qG_6Lx6w"
# Predefined search query for YouTube API
SEARCH_QUERY = "news"
# Base URL for YouTube Data API v3
BASE_URL = "https://www.googleapis.com/youtube/v3/search"

# Track the last time videos were fetched
now = datetime.now(timezone.utc)
# TODO: Store the published_after time field in the DB so that we can fetch videos that were not loaded when the server was down.
published_after = (now - timedelta(seconds=10)).isoformat() 
last_fetched_time = datetime.now(timezone.utc)

# -----------------------------
# Fetch latest videos from YouTube API
# -----------------------------
async def fetch_latest_videos():
    global last_fetched_time
    params = {
        "part": "snippet",
        "q": SEARCH_QUERY,
        "type": "video",
        "order": "date",
        "publishedAfter": last_fetched_time.isoformat(),
        "maxResults": 5,
        "key": YOUTUBE_API_KEY,
    }

    # Async HTTP request to fetch videos
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError as e:
            print(f"Error fetching videos: {e}")
            return []

    videos = []
    # Extract relevant video info and tokenize title+description
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]
        title = snippet["title"]
        description = snippet["description"]
        tokens = nltk_tokenizer(title) + nltk_tokenizer(description)
        videos.append({
            "id": video_id,
            "title": title,
            "description": description,
            "publishedAt": snippet["publishedAt"],
            "thumbnails": snippet["thumbnails"],
            "tokens": tokens,
        })
    
    #Updating last fetched time, to avoid redundant downloads.
    last_fetched_time = datetime.now(timezone.utc)
    return videos

# -----------------------------
# Save fetched videos to Firestore DB
# -----------------------------
async def save_videos_to_firestore(videos):
    db: firestore.Client = get_firestore()
    loop = asyncio.get_event_loop()

    # Run Firestore writes in executor to avoid blocking the event loop
    for video in videos:
        await loop.run_in_executor(
            None,
            lambda v=video: db.collection("videos")
                              .document(v["id"])
                              .set(v)
        )
    print(f"Saved {len(videos)} videos to Firestore")

# -----------------------------
# Combined task for scheduler
# -----------------------------
async def fetch_and_save_videos():
    videos = await fetch_latest_videos()
    if videos:
        await save_videos_to_firestore(videos)
    else:
        print("No videos uploaded in past few seconds!")
