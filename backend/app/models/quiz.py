"""Quiz-related models"""
from .base import Base, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON, func, relationship

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
