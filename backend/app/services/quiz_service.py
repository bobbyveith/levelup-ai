"""Quiz service for business logic using SQLAlchemy ORM"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.models import Quiz, QuizQuestion, QuizAttempt, QuizAnswer, Flashcard, User
from app.schemas.quiz import QuizCreate, QuizAttemptCreate, QuizAnswerCreate

class QuizService:
    """Service class for quiz operations using SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_quiz(self, quiz_data: QuizCreate) -> Quiz:
        """Create a new quiz from flashcards"""
        # Create quiz
        db_quiz = Quiz(
            title=quiz_data.title,
            description=quiz_data.description,
            total_questions=len(quiz_data.flashcard_ids) if quiz_data.flashcard_ids else 0
        )
        
        self.db.add(db_quiz)
        self.db.commit()
        self.db.refresh(db_quiz)
        
        # Add questions from flashcards
        if quiz_data.flashcard_ids:
            for order, flashcard_id in enumerate(quiz_data.flashcard_ids, 1):
                flashcard = self.db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
                if flashcard:
                    quiz_question = QuizQuestion(
                        quiz_id=db_quiz.id,
                        flashcard_id=flashcard_id,
                        question_order=order,
                        question_text=flashcard.question,
                        correct_answer=flashcard.answer,
                        question_type="open_text"
                    )
                    self.db.add(quiz_question)
            
            self.db.commit()
        
        return db_quiz
    
    def get_quiz_by_id(self, quiz_id: int) -> Optional[Quiz]:
        """Get a quiz by ID with questions"""
        return self.db.query(Quiz).filter(Quiz.id == quiz_id).first()
    
    def get_all_quizzes(self, skip: int = 0, limit: int = 100) -> List[Quiz]:
        """Get all quizzes with pagination"""
        return self.db.query(Quiz).offset(skip).limit(limit).all()
    
    def start_quiz_attempt(self, quiz_id: int, user_id: Optional[int] = None) -> QuizAttempt:
        """Start a new quiz attempt"""
        quiz = self.get_quiz_by_id(quiz_id)
        if not quiz:
            raise ValueError("Quiz not found")
        
        attempt = QuizAttempt(
            quiz_id=quiz_id,
            user_id=user_id,
            total_questions=quiz.total_questions,
            score=0.0,
            correct_answers=0,
            completed=False
        )
        
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        
        return attempt
    
    def submit_quiz_answer(self, attempt_id: int, question_id: int, answer: str) -> QuizAnswer:
        """Submit an answer for a quiz question"""
        # Get the question to check correct answer
        question = self.db.query(QuizQuestion).filter(QuizQuestion.id == question_id).first()
        if not question:
            raise ValueError("Question not found")
        
        # Check if answer is correct (simple string comparison for now)
        is_correct = answer.lower().strip() == question.correct_answer.lower().strip()
        
        # Create answer record
        quiz_answer = QuizAnswer(
            attempt_id=attempt_id,
            question_id=question_id,
            selected_answer=answer,
            is_correct=is_correct
        )
        
        self.db.add(quiz_answer)
        
        # Update attempt statistics
        attempt = self.db.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).first()
        if attempt and is_correct:
            attempt.correct_answers += 1
            attempt.score = (attempt.correct_answers / attempt.total_questions) * 100
        
        self.db.commit()
        self.db.refresh(quiz_answer)
        
        return quiz_answer
    
    def complete_quiz_attempt(self, attempt_id: int) -> QuizAttempt:
        """Mark a quiz attempt as completed"""
        attempt = self.db.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).first()
        if not attempt:
            raise ValueError("Quiz attempt not found")
        
        attempt.completed = True
        attempt.completed_at = datetime.now()
        
        self.db.commit()
        self.db.refresh(attempt)
        
        return attempt
    
    def get_quiz_attempt(self, attempt_id: int) -> Optional[QuizAttempt]:
        """Get a quiz attempt by ID"""
        return self.db.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).first()
    
    def get_user_quiz_attempts(self, user_id: int, skip: int = 0, limit: int = 100) -> List[QuizAttempt]:
        """Get quiz attempts for a user"""
        return (
            self.db.query(QuizAttempt)
            .filter(QuizAttempt.user_id == user_id)
            .order_by(QuizAttempt.started_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_quiz_questions(self, quiz_id: int) -> List[QuizQuestion]:
        """Get all questions for a quiz"""
        return (
            self.db.query(QuizQuestion)
            .filter(QuizQuestion.quiz_id == quiz_id)
            .order_by(QuizQuestion.question_order)
            .all()
        )
    
    def get_quiz_statistics(self, quiz_id: int) -> dict:
        """Get statistics for a quiz"""
        total_attempts = self.db.query(QuizAttempt).filter(QuizAttempt.quiz_id == quiz_id).count()
        completed_attempts = self.db.query(QuizAttempt).filter(
            QuizAttempt.quiz_id == quiz_id,
            QuizAttempt.completed == True
        ).count()
        
        avg_score = self.db.query(func.avg(QuizAttempt.score)).filter(
            QuizAttempt.quiz_id == quiz_id,
            QuizAttempt.completed == True
        ).scalar() or 0
        
        return {
            "total_attempts": total_attempts,
            "completed_attempts": completed_attempts,
            "completion_rate": (completed_attempts / total_attempts * 100) if total_attempts > 0 else 0,
            "average_score": round(avg_score, 2)
        }
    
    def generate_quiz_from_flashcards(self, flashcard_ids: List[int], title: str, description: str = "") -> Quiz:
        """Generate a quiz from selected flashcards"""
        quiz_data = QuizCreate(
            title=title,
            description=description,
            flashcard_ids=flashcard_ids
        )
        return self.create_quiz(quiz_data)
    
    def delete_quiz(self, quiz_id: int) -> bool:
        """Delete a quiz and all associated attempts"""
        quiz = self.get_quiz_by_id(quiz_id)
        if not quiz:
            return False
        
        self.db.delete(quiz)
        self.db.commit()
        
        return True 