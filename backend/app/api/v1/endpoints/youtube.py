"""YouTube API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.app.core.database import JSONDatabase
from backend.app.api.deps import get_database
from backend.app.schemas.youtube import YouTubeCard, YouTubeCardResponse

router = APIRouter()

@router.get("/", response_model=List[YouTubeCardResponse])
async def get_youtube_cards(db: JSONDatabase = Depends(get_database)):
    """Get all YouTube cards"""
    youtube_cards = db.get_youtube_cards()
    return youtube_cards

@router.post("/extract")
async def extract_youtube_content(
    youtube_url: str,
    db: JSONDatabase = Depends(get_database)
):
    """Extract content from YouTube URL"""
    # TODO: Implement YouTube content extraction
    # This would use the youtube-transcript-api and AI to create flashcards
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="YouTube content extraction not implemented yet"
    ) 