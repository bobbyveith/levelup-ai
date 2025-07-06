# LevelUp – AI-Powered Spaced Repetition Tutor for Aspiring Engineers

---

## 🧠 Project Theme

LevelUp is a lightweight, evolving web app that helps junior software engineers grow into mid/senior developers. It uses spaced repetition, YouTube video analysis, and AI-generated lessons to teach and quiz users daily.

The app is designed to be simple, mobile-friendly, and serve as a self-directed tutor. It learns the user’s knowledge gaps and adapts its teaching accordingly.

---

## 🎯 Core Goals

1. Teach 1 new software engineering concept each day
2. Quiz the user on multiple past concepts each day using spaced repetition
3. Provide an in-app flashcard experience
4. Provide an interactive quizzing chat game powered by OpenAI's API
5. Track user performance and adapt future lessons based on memory retention and quiz behavior
6. Pull learning content from YouTube watch history and AI-generated material
7. Automatically evolve its own codebase and knowledge daily via a self-guided AI loop

---

## 📚 Learning Sources

### 1. AI-Generated Content
- Auto-select a new topic daily
- Provide clear explanations and simple examples
- Generate flashcards and quiz content

### 2. YouTube Learning Sync
- Integrate with the user’s YouTube account
- Fetch recently watched videos
- Extract transcript and summarize concepts using OpenAI
- Generate flashcards based on video content
- Tag flashcards by video source

---

## 🧩 Learning Methods

### 🃏 Flashcard Mode (Native UI)
- User flips through flashcards daily
- “Show Answer” → Self-score → Schedule next review
- Supports spaced repetition logic

### 💬 Quizzing Chat Game (AI-Powered)
- Uses OpenAI API to simulate tutor-style conversation
- Introduces topics, asks questions, explains answers
- Remembers how the user answered
- Adjusts difficulty and review based on memory score

---

## 🧠 Adaptive Learning

The app should:
- Learn which topics the user struggles with
- Schedule weak cards more frequently
- Recommend new content based on learning history
- Personalize quizzes and teaching examples over time

---

## 🛠️ System Features

- Web-based and mobile-friendly
- Dashboard view with:
  - “📘 Learn Today’s Concept”
  - “🧠 Review Flashcards”
  - “🕹️ Quiz Me (Chat Game)”
- Flashcard review interface
- Chat quiz interface using OpenAI
- Daily build-and-commit automation loop
- Local or cloud JSON storage (later: SQLite)
- Auto-updated memory and progress tracking files

---

## 🔌 Integrations

- YouTube Data API (OAuth2) for watch history
- `youtube-transcript-api` to extract transcripts
- OpenAI API to:
  - Generate concepts and explanations
  - Summarize videos
  - Create flashcards
  - Run interactive quiz sessions

---

## 📚 Example Topics to Cover

- REST vs GraphQL
- SQL joins and indexes
- Big-O Notation
- Load Balancing
- Docker & containers
- Event-Driven Architecture
- Message Queues
- Design Patterns (Factory, Singleton, etc.)
- Testing strategies
- Git workflows

---

## 🔁 Daily Loop Workflow

1. **Teach**
   - Pick new concept (AI-generated or YouTube)
   - Display content to user
   - Store flashcard(s)

2. **Quiz**
   - Show due flashcards
   - Use spaced repetition scoring
   - Start a chat quiz session (optional)

3. **Track**
   - Log user answers
   - Update memory scores and next review dates
   - Write results to `flashcards.json` and `user_profile.json`

4. **Self-Evolve**
   - Follow `instructions.md`
   - Commit meaningful work
   - Update task, brain, and progress logs
   - Push to GitHub

---

## 🧪 Dev Guidelines

- AI should follow the loop in `instructions.md`
- Only stop work after a complete and testable unit of progress
- Generate tests when necessary
- Commit work in meaningful chunks (5–15 commits/day)
- Maintain project history and memory across runs

---

## 📁 Support Files

- `progress.md` – Daily changelog
- `task_log.json` – Task state tracker
- `brain.md` – Long-term goals and assumptions
- `topics.md` – Topics already covered
- `user_profile.json` – Performance data and quiz history

