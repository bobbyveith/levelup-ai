"""AI service for OpenAI integration"""
import openai
from typing import List, Dict, Any, Optional
from backend.app.core.config import settings

class AIService:
    """Service class for AI operations"""
    
    def __init__(self):
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
    
    def generate_flashcards_from_text(self, text: str, max_cards: int = 5) -> List[Dict[str, Any]]:
        """Generate flashcards from text using OpenAI"""
        if not settings.openai_api_key:
            raise Exception("OpenAI API key not configured")
        
        try:
            prompt = f"""
            Create {max_cards} flashcards from the following text. 
            Each flashcard should have a question and answer.
            Format as JSON with this structure:
            {{
                "flashcards": [
                    {{
                        "question": "Question text",
                        "answer": "Answer text",
                        "category": "Category name",
                        "difficulty": "easy|medium|hard"
                    }}
                ]
            }}
            
            Text: {text}
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates educational flashcards."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Parse the JSON response
            import json
            try:
                result = json.loads(content)
                return result.get("flashcards", [])
            except json.JSONDecodeError:
                # Fallback: try to extract flashcards from text
                return self._extract_flashcards_from_text(content)
                
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            return []
    
    def _extract_flashcards_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Fallback method to extract flashcards from text"""
        # Simple extraction - could be improved
        flashcards = []
        lines = text.strip().split('\n')
        
        current_card = {}
        for line in lines:
            line = line.strip()
            if line.startswith("Question:") or line.startswith("Q:"):
                current_card["question"] = line.split(":", 1)[1].strip()
            elif line.startswith("Answer:") or line.startswith("A:"):
                current_card["answer"] = line.split(":", 1)[1].strip()
                if "question" in current_card:
                    current_card["category"] = "Generated"
                    current_card["difficulty"] = "medium"
                    flashcards.append(current_card.copy())
                    current_card = {}
        
        return flashcards
    
    def generate_quiz_questions(self, flashcards: List[Dict[str, Any]], num_questions: int = 5) -> List[Dict[str, Any]]:
        """Generate quiz questions from flashcards"""
        import random
        
        if not flashcards:
            return []
        
        # Select random flashcards
        selected_cards = random.sample(flashcards, min(num_questions, len(flashcards)))
        
        quiz_questions = []
        for card in selected_cards:
            question = {
                "question": card.get("question", ""),
                "answer": card.get("answer", ""),
                "type": "multiple_choice",
                "options": self._generate_multiple_choice_options(card.get("answer", ""))
            }
            quiz_questions.append(question)
        
        return quiz_questions
    
    def _generate_multiple_choice_options(self, correct_answer: str) -> List[str]:
        """Generate multiple choice options for a question"""
        # Simple implementation - could be improved with AI
        options = [correct_answer]
        
        # Add some dummy options
        dummy_options = [
            "Option A",
            "Option B", 
            "Option C",
            "None of the above"
        ]
        
        import random
        options.extend(random.sample(dummy_options, 3))
        random.shuffle(options)
        
        return options 