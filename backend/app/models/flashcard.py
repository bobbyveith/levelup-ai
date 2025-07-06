"""Flashcard data models"""
from typing import Optional, List
from datetime import datetime

class FlashcardModel:
    """Flashcard data model for internal use"""
    
    def __init__(
        self,
        id: str,
        question: str,
        answer: str,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        tags: Optional[List[str]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
        self.tags = tags or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "difficulty": self.difficulty,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "FlashcardModel":
        """Create from dictionary"""
        return cls(
            id=data.get("id"),
            question=data.get("question"),
            answer=data.get("answer"),
            category=data.get("category"),
            difficulty=data.get("difficulty"),
            tags=data.get("tags", []),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None
        ) 