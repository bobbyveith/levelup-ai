"""Flashcards API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.app.core.database import JSONDatabase
from backend.app.api.deps import get_database
from backend.app.schemas.flashcard import Flashcard, FlashcardCreate, FlashcardResponse

router = APIRouter()

@router.get("/", response_model=List[FlashcardResponse])
async def get_flashcards(db: JSONDatabase = Depends(get_database)):
    """Get all flashcards"""
    flashcards = db.get_flashcards()
    return flashcards

@router.post("/", response_model=FlashcardResponse)
async def create_flashcard(
    flashcard: FlashcardCreate,
    db: JSONDatabase = Depends(get_database)
):
    """Create a new flashcard"""
    # TODO: Implement flashcard creation
    flashcard_data = flashcard.dict()
    flashcard_data["id"] = f"fc_{len(db.get_flashcards()) + 1}"
    
    # Add to database
    current_data = db.read_json("flashcards.json")
    if "flashcards" not in current_data:
        current_data["flashcards"] = []
    current_data["flashcards"].append(flashcard_data)
    
    if db.write_json("flashcards.json", current_data):
        return flashcard_data
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create flashcard"
        )

@router.get("/{flashcard_id}", response_model=FlashcardResponse)
async def get_flashcard(
    flashcard_id: str,
    db: JSONDatabase = Depends(get_database)
):
    """Get a specific flashcard"""
    flashcards = db.get_flashcards()
    for card in flashcards:
        if card.get("id") == flashcard_id:
            return card
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Flashcard not found"
    ) 