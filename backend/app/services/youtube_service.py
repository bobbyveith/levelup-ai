"""YouTube service for business logic using SQLAlchemy ORM"""
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from backend.app.models import YouTubeCard
from backend.app.schemas.youtube import YouTubeCardCreate, YouTubeCardUpdate

class YouTubeService:
    """Service class for YouTube operations using SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_youtube_cards(self, skip: int = 0, limit: int = 100) -> List[YouTubeCard]:
        """Get all YouTube cards with pagination"""
        return self.db.query(YouTubeCard).offset(skip).limit(limit).all()
    
    def get_youtube_card_by_id(self, card_id: int) -> Optional[YouTubeCard]:
        """Get a specific YouTube card by ID"""
        return self.db.query(YouTubeCard).filter(YouTubeCard.id == card_id).first()
    
    def get_youtube_card_by_url(self, url: str) -> Optional[YouTubeCard]:
        """Get a YouTube card by URL"""
        return self.db.query(YouTubeCard).filter(YouTubeCard.url == url).first()
    
    def create_youtube_card(self, card_data: YouTubeCardCreate) -> YouTubeCard:
        """Create a new YouTube card"""
        # Check if card with this URL already exists
        existing_card = self.get_youtube_card_by_url(card_data.url)
        if existing_card:
            return existing_card
        
        # Create new card
        db_card = YouTubeCard(
            title=card_data.title,
            url=card_data.url,
            description=card_data.description,
            transcript=card_data.transcript,
            duration=card_data.duration,
            channel=card_data.channel,
            flashcard_count=0
        )
        
        self.db.add(db_card)
        self.db.commit()
        self.db.refresh(db_card)
        
        return db_card
    
    def update_youtube_card(self, card_id: int, update_data: YouTubeCardUpdate) -> Optional[YouTubeCard]:
        """Update an existing YouTube card"""
        db_card = self.get_youtube_card_by_id(card_id)
        if not db_card:
            return None
        
        # Update fields if provided
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_card, field, value)
        
        self.db.commit()
        self.db.refresh(db_card)
        
        return db_card
    
    def delete_youtube_card(self, card_id: int) -> bool:
        """Delete a YouTube card"""
        db_card = self.get_youtube_card_by_id(card_id)
        if not db_card:
            return False
        
        self.db.delete(db_card)
        self.db.commit()
        
        return True
    
    def search_youtube_cards(self, query: str, skip: int = 0, limit: int = 100) -> List[YouTubeCard]:
        """Search YouTube cards by title, description, or channel"""
        from sqlalchemy import or_
        
        search_filter = or_(
            YouTubeCard.title.contains(query),
            YouTubeCard.description.contains(query),
            YouTubeCard.channel.contains(query)
        )
        
        return (
            self.db.query(YouTubeCard)
            .filter(search_filter)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_youtube_cards_by_channel(self, channel: str, skip: int = 0, limit: int = 100) -> List[YouTubeCard]:
        """Get YouTube cards by channel"""
        return (
            self.db.query(YouTubeCard)
            .filter(YouTubeCard.channel == channel)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update_flashcard_count(self, card_id: int, count: int) -> bool:
        """Update the flashcard count for a YouTube card"""
        db_card = self.get_youtube_card_by_id(card_id)
        if not db_card:
            return False
        
        db_card.flashcard_count = count
        self.db.commit()
        
        return True
    
    def get_youtube_card_count(self) -> int:
        """Get total number of YouTube cards"""
        return self.db.query(YouTubeCard).count()
    
    def get_recent_youtube_cards(self, limit: int = 10) -> List[YouTubeCard]:
        """Get most recently added YouTube cards"""
        return (
            self.db.query(YouTubeCard)
            .order_by(YouTubeCard.extracted_at.desc())
            .limit(limit)
            .all()
        )
    
    def get_youtube_cards_with_transcripts(self, skip: int = 0, limit: int = 100) -> List[YouTubeCard]:
        """Get YouTube cards that have transcripts"""
        return (
            self.db.query(YouTubeCard)
            .filter(YouTubeCard.transcript.isnot(None))
            .filter(YouTubeCard.transcript != "")
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_youtube_cards_without_flashcards(self, skip: int = 0, limit: int = 100) -> List[YouTubeCard]:
        """Get YouTube cards that don't have flashcards generated yet"""
        return (
            self.db.query(YouTubeCard)
            .filter(YouTubeCard.flashcard_count == 0)
            .offset(skip)
            .limit(limit)
            .all()
        ) 