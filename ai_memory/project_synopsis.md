# 🧠 Project Synopsis: LevelUp AI

## 🎯 Project Goal

LevelUp AI is a **self-evolving software project** that builds a spaced-repetition learning app for junior software engineers.

It uses a daily automation loop (via GitHub Actions + OpenAI) to:
- Build new features
- Write/refactor backend code
- Add frontend logic (HTML/JS)
- Generate tests
- Log progress and update task/memory files
- Push commits back to GitHub

---

## 🛠 What the App Is

The app is a **web-based spaced repetition system**, built with:

- **FastAPI** for the backend
- **HTML/JS** (and optionally Tailwind) for the frontend
- **JSON or SQLite** for storing flashcards, scores, and review schedules

Users learn 1 new topic daily (from AI or YouTube), and are quizzed on previous topics using spaced repetition. The app also includes a “chat quiz game” using OpenAI.

---

## 🤖 What the AI Dev Loop Does

The project includes an AI orchestrator (`ai_committer/main.py`) that acts as a **developer bot**. Each day it:

1. Loads project memory (`brain.md`, `task_log.json`, `topics.md`, etc.)
2. Asks OpenAI: *"What’s the next meaningful feature to build?"*
3. Generates or edits code files (backend routes, frontend HTML, logic, tests)
4. Runs tests (if created)
5. Commits the changes in logical steps (ideally 5–15 commits)
6. Updates all memory files
7. Pushes to GitHub

This loop runs via GitHub Actions on a daily schedule.

---

## 📂 Key Folders & Files

- `/app/` – FastAPI backend + HTML/JS frontend
- `/ai_committer/` – AI build orchestrator scripts
- `/data/` – Flashcards and user state
- `/tests/` – Unit tests, generated as needed

### Memory + Planning Files:
- `prd.md` – Product goals
- `instructions.md` – Daily AI instructions
- `task_log.json` – Tasks in progress / done
- `progress.md` – Daily changelog
- `brain.md` – Long-term strategy and philosophy
- `topics.md` – Topics already covered

---

## 🧠 Cursor AI Guidelines

When prompted to help with code:
- Always reference `instructions.md` to understand the AI loop
- Treat `ai_committer/main.py` as the autonomous developer
- Build **meaningful features** — not placeholder flashcards
- Ensure new features are:
  - Functional
  - Tested (if logic-heavy)
  - Committed cleanly
  - Tracked in `task_log.json` and `progress.md`
- Avoid redundant changes or aimless code generation

---

## ✅ Future Ideas

- Add a `dashboard` to show review stats
- Convert data layer to SQLite with SQLModel
- Make the frontend PWA-friendly
- Use browser localStorage for offline card tracking
