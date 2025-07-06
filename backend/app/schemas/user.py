"""User Pydantic schemas for API validation"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema"""
    name: str = Field(..., min_length=1, max_length=100, description="User name")
    email: Optional[EmailStr] = Field(None, description="User email")

class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass

class UserUpdate(BaseModel):
    """Schema for updating a user"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    preferences: Optional[Dict[str, Any]] = None

class UserResponse(UserBase):
    """Schema for user response"""
    id: str
    preferences: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class User(UserResponse):
    """Full user schema"""
    pass 