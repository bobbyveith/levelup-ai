"""API dependencies and shared logic"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.db.models import User

def get_database() -> Session:
    """Get database session dependency"""
    return Depends(get_db)

def get_current_user(db: Session = Depends(get_db)) -> User:
    """Get current user (placeholder for authentication)"""
    # TODO: Implement real authentication
    # For now, get or create a default user
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = User(id=1, name="Default User", email="user@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def get_db_session() -> Session:
    """Direct database session dependency"""
    return Depends(get_db) 