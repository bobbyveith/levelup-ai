"""YouTube Pydantic schemas for API validation"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

class YouTubeCardBase(BaseModel):
    """Base YouTube card schema"""
    title: str = Field(..., min_length=1, max_length=200, description="Video title")
    url: str = Field(..., description="YouTube video URL")
    description: Optional[str] = Field(None, max_length=1000, description="Video description")
    channel: Optional[str] = Field(None, max_length=100, description="Channel name")
    duration: Optional[int] = Field(None, ge=0, description="Duration in seconds")
    transcript: Optional[str] = Field(None, description="Video transcript")

class YouTubeCardCreate(YouTubeCardBase):
    """Schema for creating a YouTube card"""
    pass

class YouTubeCardUpdate(BaseModel):
    """Schema for updating a YouTube card"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    channel: Optional[str] = Field(None, max_length=100)
    duration: Optional[int] = Field(None, ge=0)
    transcript: Optional[str] = None
    flashcard_count: Optional[int] = Field(None, ge=0)

class YouTubeCardResponse(YouTubeCardBase):
    """Schema for YouTube card response"""
    id: int
    flashcard_count: int
    extracted_at: datetime

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