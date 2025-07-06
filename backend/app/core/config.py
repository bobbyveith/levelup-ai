"""Configuration settings for LevelUp AI"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # App info
    app_name: str = "LevelUp AI"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    
    # Directory paths
    data_dir: str = "data"
    static_dir: str = "../frontend/static"
    templates_dir: str = "../frontend/templates"
    
    # CORS settings
    allowed_origins: List[str] = ["*"]
    
    # Database settings
    database_url: str = "sqlite:///./data/levelup.db"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Create global settings instance
settings = Settings() 