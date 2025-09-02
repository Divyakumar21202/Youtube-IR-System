from pydantic import BaseModel
from typing import List

class Video(BaseModel):
    id: str
    title: str
    description: str
    publishedAt: str

class VideoResponse(BaseModel):
    page: int
    limit: int
    count: int
    videos: List[Video]
