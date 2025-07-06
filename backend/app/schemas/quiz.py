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
    description: Optional[str] = Field(None, max_length=1000, description="Quiz description")
    questions: List[QuizQuestion] = Field(..., description="List of quiz questions")

class QuizQuestionBase(BaseModel):
    """Base quiz question schema"""
    question_text: str = Field(..., min_length=1, max_length=1000, description="Question text")
    correct_answer: str = Field(..., min_length=1, max_length=1000, description="Correct answer")
    question_type: Optional[str] = Field("multiple_choice", pattern="^(multiple_choice|open_text|true_false)$")
    options: Optional[List[str]] = Field(default_factory=list, description="Answer options for multiple choice")

class QuizCreate(BaseModel):
    """Schema for creating a quiz"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    flashcard_ids: Optional[List[int]] = Field(default_factory=list, description="Flashcard IDs to include")
    category: Optional[str] = Field(None, max_length=100, description="Category filter")
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$", description="Difficulty filter")
    limit: Optional[int] = Field(10, ge=1, le=50, description="Number of questions")

class QuizResponse(QuizBase):
    """Schema for quiz response"""
    id: int
    total_questions: int
    created_at: datetime

    class Config:
        from_attributes = True

class QuizQuestionResponse(QuizQuestionBase):
    """Schema for quiz question response"""
    id: int
    quiz_id: int
    question_order: int
    flashcard_id: Optional[int] = None

    class Config:
        from_attributes = True

class QuizAttemptCreate(BaseModel):
    """Schema for creating a quiz attempt"""
    quiz_id: int

class QuizAttemptResponse(BaseModel):
    """Schema for quiz attempt response"""
    id: int
    quiz_id: int
    user_id: Optional[int] = None
    score: float
    total_questions: int
    correct_answers: int
    completed: bool
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class QuizAnswerCreate(BaseModel):
    """Schema for creating a quiz answer"""
    question_id: int
    selected_answer: str = Field(..., min_length=1, max_length=1000)

class QuizAnswerResponse(BaseModel):
    """Schema for quiz answer response"""
    id: int
    attempt_id: int
    question_id: int
    selected_answer: str
    is_correct: bool
    answered_at: datetime

    class Config:
        from_attributes = True

class Quiz(QuizResponse):
    """Full quiz schema"""
    pass 