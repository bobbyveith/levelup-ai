"""Flashcard and Category models"""
from .base import Base, Column, Integer, String, Text, DateTime, JSON, ForeignKey, func, relationship

class Category(Base):
    """Category model for organizing flashcards"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    color = Column(String(7), default="#3b82f6")  # Hex color code
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    flashcards = relationship("Flashcard", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

class Flashcard(Base):
    """Flashcard model for storing questions and answers"""
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    tags = Column(JSON, default=list)  # List of string tags
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Relationships
    owner = relationship("User", back_populates="flashcards")
    category = relationship("Category", back_populates="flashcards")
    quiz_questions = relationship("QuizQuestion", back_populates="flashcard")

    def __repr__(self):
        return f"<Flashcard(id={self.id}, question='{self.question[:50]}...')>"
