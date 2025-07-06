"""Quiz Pydantic schemas for API validation"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class QuizQuestion(BaseModel):
    """Individual quiz question schema"""
    question: str = Field(..., description="The question text")
    answer: str = Field(..., description="The correct answer")
    options: Optional[List[str]] = Field(default_factory=list, description="Multiple choice options")
    type: str = Field(default="multiple_choice", description="Question type")

class QuizBase(BaseModel):
    """Base quiz schema"""
    title: str = Field(..., min_length=1, max_length=200, description="Quiz title")
    description: Optional[str] = Field(None, max_length=500, description="Quiz description")
    questions: List[QuizQuestion] = Field(..., description="List of quiz questions")

class QuizCreate(BaseModel):
    """Schema for creating a new quiz"""
    title: Optional[str] = Field(None, max_length=200, description="Quiz title")
    num_questions: int = Field(default=5, ge=1, le=20, description="Number of questions to generate")
    category: Optional[str] = Field(None, description="Category filter for questions")
    difficulty: Optional[str] = Field(None, regex="^(easy|medium|hard)$", description="Difficulty filter")

class QuizResponse(QuizBase):
    """Schema for quiz response"""
    id: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Quiz(QuizResponse):
    """Full quiz schema"""
    pass 