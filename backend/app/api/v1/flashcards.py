"""Flashcard API endpoints using SQLAlchemy ORM"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user
from backend.app.models import User, Flashcard
from backend.app.schemas.flashcard import FlashcardCreate, FlashcardUpdate, FlashcardResponse
from backend.app.services.flashcard_service import FlashcardService

router = APIRouter()

@router.get("/", response_model=List[FlashcardResponse])
def get_flashcards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all flashcards with optional filtering"""
    service = FlashcardService(db)
    
    # Apply filters based on query parameters
    if search:
        flashcards = service.search_flashcards(search, skip, limit)
    elif category:
        flashcards = service.get_flashcards_by_category(category, skip, limit)
    elif difficulty:
        flashcards = service.get_flashcards_by_difficulty(difficulty, skip, limit)
    else:
        flashcards = service.get_all_flashcards(skip, limit)
    
    return flashcards

@router.get("/{flashcard_id}", response_model=FlashcardResponse)
def get_flashcard(
    flashcard_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific flashcard"""
    service = FlashcardService(db)
    flashcard = service.get_flashcard_by_id(flashcard_id)
    
    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found"
        )
    
    return flashcard

@router.post("/", response_model=FlashcardResponse, status_code=status.HTTP_201_CREATED)
def create_flashcard(
    flashcard_data: FlashcardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new flashcard"""
    service = FlashcardService(db)
    
    try:
        flashcard = service.create_flashcard(flashcard_data, current_user.id)
        return flashcard
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create flashcard: {str(e)}"
        )

@router.put("/{flashcard_id}", response_model=FlashcardResponse)
def update_flashcard(
    flashcard_id: int,
    update_data: FlashcardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing flashcard"""
    service = FlashcardService(db)
    
    # Check if flashcard exists
    existing_flashcard = service.get_flashcard_by_id(flashcard_id)
    if not existing_flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found"
        )
    
    # TODO: Add ownership check if needed
    # if existing_flashcard.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    try:
        updated_flashcard = service.update_flashcard(flashcard_id, update_data)
        return updated_flashcard
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update flashcard: {str(e)}"
        )

@router.delete("/{flashcard_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flashcard(
    flashcard_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a flashcard"""
    service = FlashcardService(db)
    
    # Check if flashcard exists
    existing_flashcard = service.get_flashcard_by_id(flashcard_id)
    if not existing_flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found"
        )
    
    # TODO: Add ownership check if needed
    # if existing_flashcard.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    success = service.delete_flashcard(flashcard_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete flashcard"
        )

@router.get("/stats/overview")
def get_flashcard_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get flashcard statistics"""
    service = FlashcardService(db)
    
    return {
        "total_flashcards": service.get_flashcard_count(),
        "count_by_difficulty": service.get_flashcard_count_by_difficulty(),
        "categories": [{"id": cat.id, "name": cat.name, "color": cat.color} for cat in service.get_categories()]
    }

@router.get("/categories/")
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all categories"""
    service = FlashcardService(db)
    categories = service.get_categories()
    
    return [{"id": cat.id, "name": cat.name, "description": cat.description, "color": cat.color} for cat in categories]

@router.get("/my-flashcards/", response_model=List[FlashcardResponse])
def get_my_flashcards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's flashcards"""
    service = FlashcardService(db)
    flashcards = service.get_flashcards_by_owner(current_user.id, skip, limit)
    return flashcards 