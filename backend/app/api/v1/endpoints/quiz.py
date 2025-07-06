"""Quiz API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.app.core.database import JSONDatabase
from backend.app.api.deps import get_database
from backend.app.schemas.quiz import Quiz, QuizCreate, QuizResponse

router = APIRouter()

@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(
    quiz_request: QuizCreate,
    db: JSONDatabase = Depends(get_database)
):
    """Generate a new quiz from flashcards"""
    # TODO: Implement quiz generation logic
    flashcards = db.get_flashcards()
    
    if not flashcards:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No flashcards available to generate quiz"
        )
    
    # Simple quiz generation (take first few flashcards)
    quiz_questions = flashcards[:quiz_request.num_questions] if len(flashcards) >= quiz_request.num_questions else flashcards
    
    quiz_data = {
        "id": f"quiz_{len(quiz_questions)}",
        "title": quiz_request.title or "Generated Quiz",
        "questions": [
            {
                "question": card.get("question", ""),
                "answer": card.get("answer", ""),
                "options": card.get("options", []),
                "type": card.get("type", "multiple_choice")
            }
            for card in quiz_questions
        ]
    }
    
    return quiz_data

@router.get("/", response_model=List[QuizResponse])
async def get_quizzes(db: JSONDatabase = Depends(get_database)):
    """Get all quizzes"""
    # TODO: Implement quiz storage and retrieval
    return [] 