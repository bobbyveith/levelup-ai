"""YouTube Pydantic schemas for API validation"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

class YouTubeCardBase(BaseModel):
    """Base YouTube card schema"""
    title: str = Field(..., min_length=1, max_length=200, description="Video title")
    url: HttpUrl = Field(..., description="YouTube video URL")
    description: Optional[str] = Field(None, max_length=1000, description="Video description")
    transcript: Optional[str] = Field(None, description="Video transcript")
    duration: Optional[int] = Field(None, ge=0, description="Video duration in seconds")
    channel: Optional[str] = Field(None, max_length=100, description="Channel name")

class YouTubeCardCreate(YouTubeCardBase):
    """Schema for creating a new YouTube card"""
    pass

class YouTubeCardResponse(YouTubeCardBase):
    """Schema for YouTube card response"""
    id: str
    extracted_at: Optional[datetime] = None
    flashcard_count: Optional[int] = Field(default=0, description="Number of flashcards generated")
    
    class Config:
        from_attributes = True

class YouTubeCard(YouTubeCardResponse):
    """Full YouTube card schema"""
    pass

class YouTubeExtractRequest(BaseModel):
    """Schema for YouTube content extraction request"""
    url: HttpUrl = Field(..., description="YouTube video URL")
    generate_flashcards: bool = Field(default=True, description="Whether to generate flashcards")
    max_flashcards: int = Field(default=10, ge=1, le=50, description="Maximum number of flashcards to generate") 