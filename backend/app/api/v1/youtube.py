"""YouTube API endpoints using SQLAlchemy ORM"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models import User, YouTubeCard
from app.schemas.youtube import YouTubeCardCreate, YouTubeCardUpdate, YouTubeCardResponse
from app.services.youtube_service import YouTubeService

router = APIRouter()

@router.get("/", response_model=List[YouTubeCardResponse])
def get_youtube_cards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    channel: Optional[str] = Query(None),
    with_transcripts: Optional[bool] = Query(None),
    without_flashcards: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all YouTube cards with optional filtering"""
    service = YouTubeService(db)
    
    # Apply filters based on query parameters
    if search:
        youtube_cards = service.search_youtube_cards(search, skip, limit)
    elif channel:
        youtube_cards = service.get_youtube_cards_by_channel(channel, skip, limit)
    elif with_transcripts:
        youtube_cards = service.get_youtube_cards_with_transcripts(skip, limit)
    elif without_flashcards:
        youtube_cards = service.get_youtube_cards_without_flashcards(skip, limit)
    else:
        youtube_cards = service.get_all_youtube_cards(skip, limit)
    
    return youtube_cards

@router.get("/{card_id}", response_model=YouTubeCardResponse)
def get_youtube_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific YouTube card"""
    service = YouTubeService(db)
    card = service.get_youtube_card_by_id(card_id)
    
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="YouTube card not found"
        )
    
    return card

@router.post("/", response_model=YouTubeCardResponse, status_code=status.HTTP_201_CREATED)
def create_youtube_card(
    card_data: YouTubeCardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new YouTube card"""
    service = YouTubeService(db)
    
    try:
        card = service.create_youtube_card(card_data)
        return card
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create YouTube card: {str(e)}"
        )

@router.put("/{card_id}", response_model=YouTubeCardResponse)
def update_youtube_card(
    card_id: int,
    update_data: YouTubeCardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing YouTube card"""
    service = YouTubeService(db)
    
    # Check if card exists
    existing_card = service.get_youtube_card_by_id(card_id)
    if not existing_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="YouTube card not found"
        )
    
    try:
        updated_card = service.update_youtube_card(card_id, update_data)
        return updated_card
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update YouTube card: {str(e)}"
        )

@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_youtube_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a YouTube card"""
    service = YouTubeService(db)
    
    success = service.delete_youtube_card(card_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="YouTube card not found"
        )

@router.get("/stats/overview")
def get_youtube_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get YouTube card statistics"""
    service = YouTubeService(db)
    
    return {
        "total_cards": service.get_youtube_card_count(),
        "recent_cards": service.get_recent_youtube_cards(limit=5)
    }

@router.get("/recent/", response_model=List[YouTubeCardResponse])
def get_recent_youtube_cards(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get most recently added YouTube cards"""
    service = YouTubeService(db)
    cards = service.get_recent_youtube_cards(limit)
    return cards

@router.get("/with-transcripts/", response_model=List[YouTubeCardResponse])
def get_youtube_cards_with_transcripts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get YouTube cards that have transcripts"""
    service = YouTubeService(db)
    cards = service.get_youtube_cards_with_transcripts(skip, limit)
    return cards

@router.get("/without-flashcards/", response_model=List[YouTubeCardResponse])
def get_youtube_cards_without_flashcards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get YouTube cards that don't have flashcards generated yet"""
    service = YouTubeService(db)
    cards = service.get_youtube_cards_without_flashcards(skip, limit)
    return cards

@router.post("/{card_id}/update-flashcard-count")
def update_flashcard_count(
    card_id: int,
    count: int = Query(..., ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update the flashcard count for a YouTube card"""
    service = YouTubeService(db)
    
    success = service.update_flashcard_count(card_id, count)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="YouTube card not found"
        )
    
    return {"message": f"Flashcard count updated to {count}"}

@router.get("/search/")
def search_youtube_cards(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search YouTube cards"""
    service = YouTubeService(db)
    cards = service.search_youtube_cards(q, skip, limit)
    return cards

@router.get("/by-channel/{channel}")
def get_youtube_cards_by_channel(
    channel: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get YouTube cards by channel"""
    service = YouTubeService(db)
    cards = service.get_youtube_cards_by_channel(channel, skip, limit)
    return cards 