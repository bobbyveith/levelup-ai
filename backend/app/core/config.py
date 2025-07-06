from pydantic import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # App info
    app_name: str = "LevelUp AI"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # OpenAI
    openai_api_key: Optional[str] = None
    
    # Paths
    data_dir: str = "data"
    static_dir: str = "frontend/static"
    templates_dir: str = "frontend/templates"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings() 