#!/usr/bin/env python3
"""
LevelUp AI - Application Runner

This script starts the FastAPI application with proper configuration.
"""

import sys
import os
import uvicorn

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Run the FastAPI application"""
    from backend.app.core.config import settings
    
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"🌐 Server will be available at: http://{settings.host}:{settings.port}")
    print(f"📖 API documentation: http://{settings.host}:{settings.port}/docs")
    print(f"🔧 Debug mode: {settings.debug}")
    print("-" * 50)
    
    uvicorn.run(
        "backend.app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning"
    )

if __name__ == "__main__":
    main() 