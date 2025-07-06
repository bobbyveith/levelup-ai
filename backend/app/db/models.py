"""SQLAlchemy models for LevelUp AI"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    """User model for authentication and profile management"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    preferences = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    flashcards = relationship("Flashcard", back_populates="owner", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

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

class Quiz(Base):
    """Quiz model for storing quiz information"""
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    total_questions = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}')>"

class QuizQuestion(Base):
    """Quiz question model linking quizzes to flashcards"""
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    question_order = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    options = Column(JSON, default=list)  # List of answer options
    question_type = Column(String(50), default="multiple_choice")

    # Foreign keys
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id"), nullable=True)

    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    flashcard = relationship("Flashcard", back_populates="quiz_questions")
    answers = relationship("QuizAnswer", back_populates="question")

    def __repr__(self):
        return f"<QuizQuestion(id={self.id}, quiz_id={self.quiz_id})>"

class QuizAttempt(Base):
    """Quiz attempt model for tracking user quiz sessions"""
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, default=0.0)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    answers = relationship("QuizAnswer", back_populates="attempt", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<QuizAttempt(id={self.id}, score={self.score}, completed={self.completed})>"

class QuizAnswer(Base):
    """Quiz answer model for storing user responses"""
    __tablename__ = "quiz_answers"

    id = Column(Integer, primary_key=True, index=True)
    selected_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign keys
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)

    # Relationships
    attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("QuizQuestion", back_populates="answers")

    def __repr__(self):
        return f"<QuizAnswer(id={self.id}, is_correct={self.is_correct})>"

class YouTubeCard(Base):
    """YouTube card model for storing extracted video information"""
    __tablename__ = "youtube_cards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    url = Column(String(500), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    transcript = Column(Text, nullable=True)
    duration = Column(Integer, nullable=True)  # Duration in seconds
    channel = Column(String(100), nullable=True)
    extracted_at = Column(DateTime(timezone=True), server_default=func.now())
    flashcard_count = Column(Integer, default=0)

    def __repr__(self):
        return f"<YouTubeCard(id={self.id}, title='{self.title}')>" 