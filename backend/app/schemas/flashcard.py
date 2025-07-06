"""Flashcard Pydantic schemas for API validation"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class FlashcardBase(BaseModel):
    """Base flashcard schema"""
    question: str = Field(..., min_length=1, max_length=1000, description="The question text")
    answer: str = Field(..., min_length=1, max_length=1000, description="The answer text")
    category: Optional[str] = Field(None, max_length=100, description="Category of the flashcard")
    difficulty: Optional[str] = Field(None, regex="^(easy|medium|hard)$", description="Difficulty level")
    tags: Optional[List[str]] = Field(default_factory=list, description="List of tags")

class FlashcardCreate(FlashcardBase):
    """Schema for creating a new flashcard"""
    pass

class FlashcardUpdate(BaseModel):
    """Schema for updating a flashcard"""
    question: Optional[str] = Field(None, min_length=1, max_length=1000)
    answer: Optional[str] = Field(None, min_length=1, max_length=1000)
    category: Optional[str] = Field(None, max_length=100)
    difficulty: Optional[str] = Field(None, regex="^(easy|medium|hard)$")
    tags: Optional[List[str]] = None

class FlashcardResponse(FlashcardBase):
    """Schema for flashcard response"""
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Flashcard(FlashcardResponse):
    """Full flashcard schema"""
    pass 