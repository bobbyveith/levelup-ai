"""Database configuration and SQLAlchemy setup"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import os

from backend.app.core.config import settings

# Ensure data directory exists
os.makedirs(settings.data_dir, exist_ok=True)

# Create SQLite database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///./{settings.data_dir}/levelup.db"

# Create engine with SQLite-specific settings
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={
        "check_same_thread": False,  # Allow SQLite to be used with FastAPI
    },
    echo=settings.debug,  # Log SQL queries in debug mode
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    
    This will be used as a FastAPI dependency to inject database sessions
    into route handlers and services.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    # Import models to register them with Base
    from backend.app import models
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all database tables (for testing/reset)"""
    Base.metadata.drop_all(bind=engine)

# Database utilities
def init_db():
    """Initialize database with tables"""
    create_tables()

def reset_db():
    """Reset database (drop and recreate all tables)"""
    drop_tables()
    create_tables() 