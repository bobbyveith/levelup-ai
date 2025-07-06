"""Database configuration and connections"""
import json
import os
from typing import Dict, Any, List
from backend.app.core.config import settings

class JSONDatabase:
    """Simple JSON file database for the LevelUp AI app"""
    
    def __init__(self):
        self.data_dir = settings.data_dir
        
    def read_json(self, filename: str) -> Dict[str, Any]:
        """Read data from JSON file"""
        file_path = os.path.join(self.data_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def write_json(self, filename: str, data: Dict[str, Any]) -> bool:
        """Write data to JSON file"""
        file_path = os.path.join(self.data_dir, filename)
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing to {filename}: {e}")
            return False
    
    def get_flashcards(self) -> List[Dict[str, Any]]:
        """Get all flashcards"""
        data = self.read_json("flashcards.json")
        return data.get("flashcards", [])
    
    def get_youtube_cards(self) -> List[Dict[str, Any]]:
        """Get all YouTube cards"""
        data = self.read_json("youtube_cards.json")
        return data.get("youtube_cards", [])
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Get user profile"""
        data = self.read_json("user_profile.json")
        return data.get("user_profile", {})

# Global database instance
db = JSONDatabase() 