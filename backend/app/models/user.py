"""User data models"""
from typing import Optional, Dict, Any
from datetime import datetime

class UserModel:
    """User data model for internal use"""
    
    def __init__(
        self,
        id: str,
        name: str,
        email: Optional[str] = None,
        preferences: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.email = email
        self.preferences = preferences or {}
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "preferences": self.preferences,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "UserModel":
        """Create from dictionary"""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            email=data.get("email"),
            preferences=data.get("preferences", {}),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None
        ) 