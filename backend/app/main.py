"""Main FastAPI application with SQLAlchemy database support"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import flashcards, quiz, youtube

# Initialize database tables
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="LevelUp AI - Smart Learning Platform with SQLAlchemy",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="../frontend/templates")

# Include API routers
app.include_router(flashcards.router, prefix="/api/v1/flashcards", tags=["flashcards"])
app.include_router(quiz.router, prefix="/api/v1/quiz", tags=["quiz"])
app.include_router(youtube.router, prefix="/api/v1/youtube", tags=["youtube"])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "LevelUp AI is running with SQLAlchemy database",
        "version": "1.0.0"
    }

@app.get("/api/v1/health")
async def api_health():
    """API health check"""
    return {
        "status": "healthy",
        "database": "SQLAlchemy + SQLite",
        "features": [
            "Flashcard Management",
            "Quiz Generation",
            "YouTube Integration",
            "User Management",
            "Progress Tracking"
        ]
    }

@app.get("/api/v1/")
async def api_info():
    """API information"""
    return {
        "message": "LevelUp AI API v1.0",
        "database": "SQLAlchemy + SQLite",
        "endpoints": {
            "flashcards": "/api/v1/flashcards",
            "quiz": "/api/v1/quiz",
            "youtube": "/api/v1/youtube"
        },
        "docs": "/api/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 