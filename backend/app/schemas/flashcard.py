"""Flashcard Pydantic schemas for API validation"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class FlashcardBase(BaseModel):
    """Base flashcard schema"""
    question: str = Field(..., min_length=1, max_length=1000, description="Question text")
    answer: str = Field(..., min_length=1, max_length=1000, description="Answer text")
    category: Optional[str] = Field(None, max_length=100, description="Category name")
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$", description="Difficulty level")
    tags: Optional[List[str]] = Field(default_factory=list, description="List of tags")

class FlashcardCreate(FlashcardBase):
    """Schema for creating a new flashcard"""
    pass

class FlashcardUpdate(BaseModel):
    """Schema for updating a flashcard"""
    question: Optional[str] = Field(None, min_length=1, max_length=1000)
    answer: Optional[str] = Field(None, min_length=1, max_length=1000)
    category: Optional[str] = Field(None, max_length=100)
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$")
    tags: Optional[List[str]] = None

class FlashcardResponse(FlashcardBase):
    """Schema for flashcard response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: Optional[int] = None
    category_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class Flashcard(FlashcardResponse):
    """Full flashcard schema"""
    pass 