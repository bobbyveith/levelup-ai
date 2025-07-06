"""Flashcard service for business logic using SQLAlchemy ORM"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from backend.app.db.models import Flashcard, User, Category
from backend.app.schemas.flashcard import FlashcardCreate, FlashcardUpdate

class FlashcardService:
    """Service class for flashcard operations using SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_flashcards(self, skip: int = 0, limit: int = 100) -> List[Flashcard]:
        """Get all flashcards with pagination"""
        return self.db.query(Flashcard).offset(skip).limit(limit).all()
    
    def get_flashcard_by_id(self, flashcard_id: int) -> Optional[Flashcard]:
        """Get a specific flashcard by ID"""
        return self.db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
    
    def create_flashcard(self, flashcard_data: FlashcardCreate, owner_id: Optional[int] = None) -> Flashcard:
        """Create a new flashcard"""
        # Get or create category if provided
        category_id = None
        if flashcard_data.category:
            category = self.get_or_create_category(flashcard_data.category)
            category_id = category.id
        
        # Create flashcard
        db_flashcard = Flashcard(
            question=flashcard_data.question,
            answer=flashcard_data.answer,
            difficulty=flashcard_data.difficulty or "medium",
            tags=flashcard_data.tags or [],
            owner_id=owner_id,
            category_id=category_id
        )
        
        self.db.add(db_flashcard)
        self.db.commit()
        self.db.refresh(db_flashcard)
        
        return db_flashcard
    
    def update_flashcard(self, flashcard_id: int, update_data: FlashcardUpdate) -> Optional[Flashcard]:
        """Update an existing flashcard"""
        db_flashcard = self.get_flashcard_by_id(flashcard_id)
        if not db_flashcard:
            return None
        
        # Update fields if provided
        update_dict = update_data.dict(exclude_unset=True)
        
        # Handle category update
        if "category" in update_dict:
            category_name = update_dict.pop("category")
            if category_name:
                category = self.get_or_create_category(category_name)
                db_flashcard.category_id = category.id
            else:
                db_flashcard.category_id = None
        
        # Update other fields
        for field, value in update_dict.items():
            setattr(db_flashcard, field, value)
        
        self.db.commit()
        self.db.refresh(db_flashcard)
        
        return db_flashcard
    
    def delete_flashcard(self, flashcard_id: int) -> bool:
        """Delete a flashcard"""
        db_flashcard = self.get_flashcard_by_id(flashcard_id)
        if not db_flashcard:
            return False
        
        self.db.delete(db_flashcard)
        self.db.commit()
        
        return True
    
    def get_flashcards_by_category(self, category_name: str, skip: int = 0, limit: int = 100) -> List[Flashcard]:
        """Get flashcards by category name"""
        return (
            self.db.query(Flashcard)
            .join(Category)
            .filter(Category.name == category_name)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_flashcards_by_difficulty(self, difficulty: str, skip: int = 0, limit: int = 100) -> List[Flashcard]:
        """Get flashcards by difficulty"""
        return (
            self.db.query(Flashcard)
            .filter(Flashcard.difficulty == difficulty)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_flashcards_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Flashcard]:
        """Get flashcards by owner"""
        return (
            self.db.query(Flashcard)
            .filter(Flashcard.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search_flashcards(self, query: str, skip: int = 0, limit: int = 100) -> List[Flashcard]:
        """Search flashcards by question or answer content"""
        search_filter = or_(
            Flashcard.question.contains(query),
            Flashcard.answer.contains(query)
        )
        
        return (
            self.db.query(Flashcard)
            .filter(search_filter)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_or_create_category(self, category_name: str) -> Category:
        """Get existing category or create a new one"""
        category = self.db.query(Category).filter(Category.name == category_name).first()
        if not category:
            category = Category(name=category_name)
            self.db.add(category)
            self.db.commit()
            self.db.refresh(category)
        
        return category
    
    def get_categories(self) -> List[Category]:
        """Get all categories"""
        return self.db.query(Category).all()
    
    def get_flashcard_count(self) -> int:
        """Get total number of flashcards"""
        return self.db.query(Flashcard).count()
    
    def get_flashcard_count_by_difficulty(self) -> dict:
        """Get flashcard count grouped by difficulty"""
        from sqlalchemy import func
        
        results = (
            self.db.query(Flashcard.difficulty, func.count(Flashcard.id))
            .group_by(Flashcard.difficulty)
            .all()
        )
        
        return {difficulty: count for difficulty, count in results} 