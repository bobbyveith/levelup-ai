"""Quiz API endpoints using SQLAlchemy ORM"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user
from backend.app.models import User, Quiz, QuizAttempt
from backend.app.schemas.quiz import (
    QuizCreate, QuizResponse, QuizAttemptCreate, QuizAttemptResponse, 
    QuizAnswerCreate, QuizAnswerResponse, QuizQuestionResponse
)
from backend.app.services.quiz_service import QuizService

router = APIRouter()

@router.get("/", response_model=List[QuizResponse])
def get_quizzes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all quizzes"""
    service = QuizService(db)
    quizzes = service.get_all_quizzes(skip, limit)
    return quizzes

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific quiz"""
    service = QuizService(db)
    quiz = service.get_quiz_by_id(quiz_id)
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    return quiz

@router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def create_quiz(
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new quiz"""
    service = QuizService(db)
    
    try:
        quiz = service.create_quiz(quiz_data)
        return quiz
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create quiz: {str(e)}"
        )

@router.get("/{quiz_id}/questions", response_model=List[QuizQuestionResponse])
def get_quiz_questions(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all questions for a quiz"""
    service = QuizService(db)
    
    # Check if quiz exists
    quiz = service.get_quiz_by_id(quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    questions = service.get_quiz_questions(quiz_id)
    return questions

@router.post("/{quiz_id}/attempts", response_model=QuizAttemptResponse, status_code=status.HTTP_201_CREATED)
def start_quiz_attempt(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start a new quiz attempt"""
    service = QuizService(db)
    
    try:
        attempt = service.start_quiz_attempt(quiz_id, current_user.id)
        return attempt
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to start quiz attempt: {str(e)}"
        )

@router.get("/attempts/{attempt_id}", response_model=QuizAttemptResponse)
def get_quiz_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a quiz attempt"""
    service = QuizService(db)
    attempt = service.get_quiz_attempt(attempt_id)
    
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz attempt not found"
        )
    
    # TODO: Add ownership check if needed
    # if attempt.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    return attempt

@router.post("/attempts/{attempt_id}/answers", response_model=QuizAnswerResponse, status_code=status.HTTP_201_CREATED)
def submit_quiz_answer(
    attempt_id: int,
    answer_data: QuizAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit an answer for a quiz question"""
    service = QuizService(db)
    
    # Check if attempt exists and belongs to user
    attempt = service.get_quiz_attempt(attempt_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz attempt not found"
        )
    
    # TODO: Add ownership check if needed
    # if attempt.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    try:
        answer = service.submit_quiz_answer(attempt_id, answer_data.question_id, answer_data.selected_answer)
        return answer
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to submit answer: {str(e)}"
        )

@router.post("/attempts/{attempt_id}/complete", response_model=QuizAttemptResponse)
def complete_quiz_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Complete a quiz attempt"""
    service = QuizService(db)
    
    # Check if attempt exists and belongs to user
    attempt = service.get_quiz_attempt(attempt_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz attempt not found"
        )
    
    # TODO: Add ownership check if needed
    # if attempt.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    try:
        completed_attempt = service.complete_quiz_attempt(attempt_id)
        return completed_attempt
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to complete quiz: {str(e)}"
        )

@router.get("/attempts/my-attempts", response_model=List[QuizAttemptResponse])
def get_my_quiz_attempts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's quiz attempts"""
    service = QuizService(db)
    attempts = service.get_user_quiz_attempts(current_user.id, skip, limit)
    return attempts

@router.get("/{quiz_id}/statistics")
def get_quiz_statistics(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get quiz statistics"""
    service = QuizService(db)
    
    # Check if quiz exists
    quiz = service.get_quiz_by_id(quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    stats = service.get_quiz_statistics(quiz_id)
    return stats

@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a quiz"""
    service = QuizService(db)
    
    success = service.delete_quiz(quiz_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )

@router.post("/generate-from-flashcards", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def generate_quiz_from_flashcards(
    title: str = Query(..., description="Quiz title"),
    description: str = Query("", description="Quiz description"),
    flashcard_ids: List[int] = Query(..., description="List of flashcard IDs to include"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a quiz from selected flashcards"""
    service = QuizService(db)
    
    try:
        quiz = service.generate_quiz_from_flashcards(flashcard_ids, title, description)
        return quiz
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to generate quiz: {str(e)}"
        ) 