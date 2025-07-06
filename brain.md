# 🧠 Brain – Long-Term Project Memory

This file contains the long-term memory and high-level understanding of the project. It should be updated when:
- A major architectural decision is made
- A philosophical or design principle is established
- The direction of the app changes
- Important technical constraints are discovered

---

## 🎯 Purpose

LevelUp is a self-evolving, AI-built learning app for junior software engineers.  
It teaches one new concept per day, quizzes the user on past content using spaced repetition, and tracks user performance to adapt future lessons.  
All progress is committed and logged daily via an autonomous AI workflow.

---

## 🔍 Key Principles

- Simple, mobile-friendly, web-based UI
- Focus on **learning quality**, not feature bloat
- Minimalism: avoid turning into a full Notion-style second brain
- Always teach, review, or evolve with purpose
- Every day should produce value for the user and a commit trail

---

## 🧩 App Modules (So Far)

- **Flashcard Engine** – Handles spaced repetition logic
- **Chat Quiz Interface** – Simulates tutor-like interaction via OpenAI
- **YouTube Sync** – Pulls learning content from recently watched videos
- **Memory System** – Tracks user history, progress, and performance
- **Self-Developer Loop** – Updates itself, commits work, and logs intent

---

## 🛠 Architectural Notes

- Backend: Flask (or FastAPI) for simplicity and speed
- Frontend: Vanilla HTML + Tailwind + JS (mobile-first)
- Data: Start with JSON files; upgrade to SQLite if needed
- Tests: All logic should be accompanied by a test when applicable

---

## 🔮 Future Ideas

- Export flashcards to Anki
- Review mode with visual progress bars
- Dashboard to show memory stats and topic mastery
- Daily email reminders
- Chrome extension or PWA wrapper

---

## 🧠 Current Assumptions

- The user watches YouTube videos related to software engineering
- They want to retain and reinforce what they learn
- They engage with the app daily or regularly
- They’re early-career engineers aiming to become mid- or senior-level

