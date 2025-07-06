"""LevelUp AI - Main FastAPI Application"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.api.v1.api import api_router

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="Smart Learning Platform with AI-Powered Flashcards and Quizzes"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

# Templates
templates = Jinja2Templates(directory=settings.templates_dir)

# Include API router
app.include_router(api_router, prefix=settings.api_v1_prefix)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "app": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
    }

@app.get("/flashcards", response_class=HTMLResponse)
async def flashcards_page(request: Request):
    """Serve the flashcards page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/quiz", response_class=HTMLResponse)
async def quiz_page(request: Request):
    """Serve the quiz page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/youtube", response_class=HTMLResponse)
async def youtube_page(request: Request):
    """Serve the YouTube extraction page"""
    return templates.TemplateResponse("index.html", {"request": request})

# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup"""
    print(f"🚀 {settings.app_name} v{settings.app_version} starting up...")
    print(f"📊 Debug mode: {settings.debug}")
    print(f"🔗 API docs available at: http://{settings.host}:{settings.port}/docs")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    print(f"🛑 {settings.app_name} shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port,
        reload=settings.debug
    ) 