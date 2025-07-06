# 🔁 Daily Run Instructions – AI Dev Loop

This file defines the step-by-step process the AI should follow every time it runs.  
It ensures consistency, structure, and forward progress.  
This loop should be followed *exactly*, in order, and should not be skipped or prematurely stopped.

---

## 1. 🧠 Load Project Memory

Read and internalize the following files:

- `brain.md`: Overall vision, goals, values, and project philosophy
- `task_log.json`: Current, upcoming, and completed tasks
- `topics.md`: Concepts already taught or reviewed (to avoid duplicates)
- `progress.md`: Recent work log and context
- `user_profile.json`: User memory and quiz accuracy (for adaptive behavior)

---

## 2. 🤔 Decide What to Work On

- If there is an "in_progress" task in `task_log.json`, continue working on that.
- If no task is in progress, prompt yourself:
  > "What is the next logical, self-contained unit of work I can complete based on the current state of the project?"

- Break the next goal into substeps and select one that can be:
  - Clearly defined
  - Fully implemented in one session
  - Tested (if needed)
  - Meaningful in isolation

---

## 3. 🛠️ Execute the Work

### A. Code Generation
- Write the required code for the task
- Use good naming, comments, and modularity
- If the task introduces logic or models, generate **unit tests**
- Save test files under `tests/`

### B. Testing
- If a test was written, run it
- If it fails, fix the bug and re-run
- Do not continue unless the tests pass

### C. Commit Frequently
- Create 5–15 commits with clear messages
- Group commits logically: setup, feature, test, refactor, etc.

---

## 4. 🔄 Update Memory Files

- `task_log.json`:  
  - Mark completed tasks as `done`  
  - Add new tasks (if discovered during execution)  
  - Mark next step as `in_progress`

- `progress.md`:  
  - Log what was accomplished today and what changed

- `brain.md`:  
  - Update if your architecture, assumptions, or direction shifted

- `topics.md`:  
  - If a new concept was taught, add it to the list with today’s date

- `user_profile.json`:  
  - Log quiz answers and scores if a quiz or flashcard review occurred

---

## 5. 🧠 Ensure Completion

**Only end the run when:**
- A clear unit of work was completed
- All relevant tests pass
- The change is committed and pushed
- All memory files are updated
- A summary of progress is recorded in `progress.md`

If the task is too big to finish, break it down and complete the first piece, then log the next step as `in_progress`.

---

## 6. 🚀 Push Changes

- Push all commits to GitHub
- Ensure the commit history reflects clear, human-readable progress

---

## 🧪 Final Note

This is not a suggestion — it is the **rulebook**.  
Do not skip or reorder steps.  
Build carefully. Log clearly. Learn continuously.
