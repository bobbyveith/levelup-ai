"""Flashcard service for business logic"""
from typing import List, Optional, Dict, Any
from backend.app.core.database import JSONDatabase
from backend.app.models.flashcard import FlashcardModel
from backend.app.schemas.flashcard import FlashcardCreate, FlashcardUpdate

class FlashcardService:
    """Service class for flashcard operations"""
    
    def __init__(self, db: JSONDatabase):
        self.db = db
    
    def get_all_flashcards(self) -> List[Dict[str, Any]]:
        """Get all flashcards"""
        return self.db.get_flashcards()
    
    def get_flashcard_by_id(self, flashcard_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific flashcard by ID"""
        flashcards = self.db.get_flashcards()
        for card in flashcards:
            if card.get("id") == flashcard_id:
                return card
        return None
    
    def create_flashcard(self, flashcard_data: FlashcardCreate) -> Dict[str, Any]:
        """Create a new flashcard"""
        # Generate ID
        existing_cards = self.db.get_flashcards()
        new_id = f"fc_{len(existing_cards) + 1}"
        
        # Create flashcard model
        flashcard = FlashcardModel(
            id=new_id,
            question=flashcard_data.question,
            answer=flashcard_data.answer,
            category=flashcard_data.category,
            difficulty=flashcard_data.difficulty,
            tags=flashcard_data.tags or []
        )
        
        # Add to database
        current_data = self.db.read_json("flashcards.json")
        if "flashcards" not in current_data:
            current_data["flashcards"] = []
        
        current_data["flashcards"].append(flashcard.to_dict())
        
        if self.db.write_json("flashcards.json", current_data):
            return flashcard.to_dict()
        else:
            raise Exception("Failed to create flashcard")
    
    def update_flashcard(self, flashcard_id: str, update_data: FlashcardUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing flashcard"""
        current_data = self.db.read_json("flashcards.json")
        if "flashcards" not in current_data:
            return None
        
        for i, card in enumerate(current_data["flashcards"]):
            if card.get("id") == flashcard_id:
                # Update fields
                if update_data.question is not None:
                    card["question"] = update_data.question
                if update_data.answer is not None:
                    card["answer"] = update_data.answer
                if update_data.category is not None:
                    card["category"] = update_data.category
                if update_data.difficulty is not None:
                    card["difficulty"] = update_data.difficulty
                if update_data.tags is not None:
                    card["tags"] = update_data.tags
                
                # Update timestamp
                from datetime import datetime
                card["updated_at"] = datetime.now().isoformat()
                
                if self.db.write_json("flashcards.json", current_data):
                    return card
                else:
                    raise Exception("Failed to update flashcard")
        
        return None
    
    def delete_flashcard(self, flashcard_id: str) -> bool:
        """Delete a flashcard"""
        current_data = self.db.read_json("flashcards.json")
        if "flashcards" not in current_data:
            return False
        
        original_length = len(current_data["flashcards"])
        current_data["flashcards"] = [
            card for card in current_data["flashcards"] 
            if card.get("id") != flashcard_id
        ]
        
        if len(current_data["flashcards"]) < original_length:
            return self.db.write_json("flashcards.json", current_data)
        
        return False
    
    def get_flashcards_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get flashcards by category"""
        all_cards = self.db.get_flashcards()
        return [card for card in all_cards if card.get("category") == category]
    
    def get_flashcards_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """Get flashcards by difficulty"""
        all_cards = self.db.get_flashcards()
        return [card for card in all_cards if card.get("difficulty") == difficulty] 