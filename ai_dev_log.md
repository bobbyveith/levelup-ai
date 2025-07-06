
# AI Development Log Entry - 2025-07-05T21:27:32.880603

## Task: Build flashcard review UI (HTML + JS)
**Status**: next
**Notes**: Allow user to flip flashcards, self-score, and mark for spaced repetition

## AI Context:
Fallback: Improve documentation and code comments

## Actions Taken:
- Executed daily development loop
- Updated project memory
- Committed progress

---

# AI Development Log Entry - 2025-07-05T21:28:10.464283

## Task: Integrate YouTube transcript parser
**Status**: next
**Notes**: Use youtube-transcript-api and OpenAI to generate flashcards from videos

## AI Context:
To integrate the YouTube transcript parser using the youtube-transcript-api in the LevelUp AI project, you can follow these steps:

1. Install the youtube-transcript-api package:
```bash
pip install youtube-transcript-api
```

2. Import the necessary modules in your FastAPI backend code where you want to parse the YouTube transcript:
```python
from youtube_transcript_api import YouTubeTranscriptApi
```

3. Use the YouTubeTranscriptApi to fetch the transcript for a given YouTube video ID:
```python
video_id = "YOUR_YOUTUBE_VIDEO_ID"
transcript = YouTubeTranscriptApi.get_transcript(video_id)
```

4. You can then process the transcript data as needed, for example, extract text from each transcript entry:
```python
transcript_text = ' '.join([entry['text'] for entry in transcript])
```

5. You can now use the extracted transcript text with OpenAI or any other tool to generate flashcards.

Make sure to handle exceptions and errors gracefully in your code, and consider adding appropriate error handling for cases where the transcript retrieval fails.

By following these steps and integrating the YouTube transcript parser into your LevelUp AI project, you will be able to generate flashcards from YouTube videos efficiently.

## Actions Taken:
- Executed daily development loop
- Updated project memory
- Committed progress

---

# AI Development Log Entry - 2025-07-05T21:33:11.148776

## Task: Add spaced repetition algorithm to backend
**Status**: next
**Notes**: Implement logic to score answers and schedule next reviews

## AI Context:
To add a spaced repetition algorithm to the backend of the LevelUp AI app, you can follow these specific code changes:

1. **Add a new model in SQLAlchemy for tracking flashcard reviews**:
    ```python
    from sqlalchemy import Column, Integer, DateTime
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class FlashcardReview(Base):
        __tablename__ = 'flashcard_review'
        id = Column(Integer, primary_key=True)
        flashcard_id = Column(Integer, ForeignKey('flashcard.id'))
        user_id = Column(Integer, ForeignKey('user.id'))
        review_date = Column(DateTime)
        next_review_date = Column(DateTime)
        score = Column(Integer)
    ```

2. **Update your existing Flashcard model** to include an attribute for the difficulty level:
    ```python
    class Flashcard(Base):
        __tablename__ = 'flashcard'
        id = Column(Integer, primary_key=True)
        question = Column(String)
        answer = Column(String)
        difficulty = Column(Integer)  # Add difficulty level for spaced repetition
    ```

3. **Implement a function to schedule next review date based on the user's score**:
    ```python
    from datetime import timedelta

    def schedule_next_review(score, last_review_date):
        if score >= 3:
            return last_review_date + timedelta(days=1)
        elif score == 2:
            return last_review_date + timedelta(days=3)
        else:
            return last_review_date + timedelta(days=7)
    ```

4. **Update your API endpoint for submitting flashcard reviews**:
    ```python
    @app.post('/flashcards/{flashcard_id}/review')
    def submit_flashcard_review(flashcard_id: int, score: int):
        # Logic to fetch flashcard, calculate next review date, and update database
        flashcard = session.query(Flashcard).filter_by(id=flashcard_id).first()
        next_review_date = schedule_next_review(score, flashcard.last_review_date)
        flashcard_review = FlashcardReview(flashcard_id=flashcard_id, user_id=current_user.id, review_date=datetime.now(), next_review_date=next_review_date, score=score)
        session.add(flashcard_review)
        session.commit()
        return {'message': 'Review submitted successfully'}
    ```

5. **Update your frontend to display flashcards based on the next review date**:
    - Modify frontend logic to fetch flashcards that are due for review based on the next review date stored in the database.

By implementing these code changes, you will be able to integrate a spaced repetition algorithm into your LevelUp AI app's backend for efficient flashcard review scheduling.

## Actions Taken:
- Executed daily development loop
- Updated project memory
- Committed progress

---
