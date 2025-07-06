"""API v1 router aggregation"""
from fastapi import APIRouter
from backend.app.api.v1.endpoints import flashcards, quiz, youtube

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(flashcards.router, prefix="/flashcards", tags=["flashcards"])
api_router.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
api_router.include_router(youtube.router, prefix="/youtube", tags=["youtube"]) 