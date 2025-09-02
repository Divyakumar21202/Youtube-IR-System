import httpx
import asyncio
from datetime import datetime, timedelta, timezone
from src.firebase_utils import get_firestore
from firebase_admin import firestore
from src.core.nltk_tokenizer import nltk_tokenizer

# -----------------------------
# API Key Management
# -----------------------------
YOUTUBE_API_KEYS = [
    "AIzaSyBYiUmQUS8kldCkshqxH5iI-pGB5nWY34Y",
    "AIzaSyA4-Lylxxgs10xxPcrGJazsXKUmn62z_2I",
    "AIzaSyCw_PnUJKCkO3aPDcnZP2XpOfUP9dOr0xM",
    "AIzaSyDnuUDLySpf3E3iZQ0o7kAFcbRAzwIrSdk",
]
current_key_index = 0

def get_next_api_key():
    """Round-robin key selection"""
    global current_key_index, YOUTUBE_API_KEYS
    if not YOUTUBE_API_KEYS:
        raise RuntimeError("No valid YouTube API keys available!")

    key = YOUTUBE_API_KEYS[current_key_index]
    current_key_index = (current_key_index + 1) % len(YOUTUBE_API_KEYS)
    return key

def remove_api_key(key: str):
    """Remove exhausted key from the pool"""
    global YOUTUBE_API_KEYS, current_key_index
    if key in YOUTUBE_API_KEYS:
        YOUTUBE_API_KEYS.remove(key)
        # Adjust index so it doesn’t go out of range
        current_key_index %= max(len(YOUTUBE_API_KEYS), 1)

# -----------------------------
# Other Config
# -----------------------------
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
    api_key = get_next_api_key()

    params = {
        "part": "snippet",
        "q": SEARCH_QUERY,
        "type": "video",
        "order": "date",
        "publishedAfter": last_fetched_time.isoformat(),
        "maxResults": 5,
        "key": api_key,
    }

    # Async HTTP request to fetch videos
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(BASE_URL, params=params, timeout=10)
            if resp.status_code == 403:
                print(f"API key exhausted: {api_key}, removing...")
                remove_api_key(api_key)
                return await fetch_latest_videos()  # Retry with next key
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
    if not YOUTUBE_API_KEYS:
        print("No valid API keys left. Stopping fetch.")
        return
    videos = await fetch_latest_videos()
    if videos:
        await save_videos_to_firestore(videos)
    else:
        print("No videos uploaded in past few seconds!")
