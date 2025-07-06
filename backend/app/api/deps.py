"""API dependencies and shared logic"""
from fastapi import Depends, HTTPException, status
from backend.app.core.database import db, JSONDatabase

def get_database() -> JSONDatabase:
    """Get database instance"""
    return db

def get_current_user():
    """Get current user (placeholder for authentication)"""
    # TODO: Implement authentication
    return {"id": "user1", "name": "Default User"} 