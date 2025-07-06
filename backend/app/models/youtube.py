"""YouTube card model for storing extracted video information"""
from .base import Base, Column, Integer, String, Text, DateTime, func

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
