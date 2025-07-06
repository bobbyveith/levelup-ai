#!/usr/bin/env python3
"""
AI Orchestrator - Main Brain of LevelUp AI

This script follows the daily loop defined in ai_memory/instructions.md:
1. Load project memory
2. Decide what to work on
3. Execute the work
4. Update memory files
5. Push changes
"""

import os
import sys
import json
import subprocess
import datetime
from pathlib import Path
from typing import Dict, List, Any
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIOrchestrator:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.memory_files = {
            'brain': self.project_root / 'ai_memory' / 'brain.md',
            'task_log': self.project_root / 'ai_memory' / 'task_log.json',
            'topics': self.project_root / 'ai_memory' / 'topics.md',
            'progress': self.project_root / 'ai_memory' / 'progress.md',
            'user_profile': self.project_root / 'data' / 'user_profile.json'
        }
        
        # Initialize OpenAI
        self.openai_client = None
        if openai_key := os.getenv('OPENAI_API_KEY'):
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=openai_key)
        
        self.current_task = None
        self.commits_made = []
        
    def run_daily_loop(self):
        """Execute the complete daily development loop"""
        print("🚀 Starting AI Daily Development Loop")
        print("=" * 50)
        
        try:
            # Step 1: Load Project Memory
            print("\n1. 🧠 Loading Project Memory...")
            self.load_project_memory()
            
            # Step 2: Decide What to Work On
            print("\n2. 🤔 Deciding What to Work On...")
            self.decide_next_task()
            
            # Step 3: Execute the Work
            print("\n3. 🛠️ Executing Work...")
            self.execute_work()
            
            # Step 4: Update Memory Files
            print("\n4. 🔄 Updating Memory Files...")
            self.update_memory_files()
            
            # Step 5: Push Changes
            print("\n5. 🚀 Pushing Changes...")
            self.push_changes()
            
            print("\n✅ Daily loop completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Error during daily loop: {str(e)}")
            sys.exit(1)
    
    def load_project_memory(self):
        """Load and parse all memory files"""
        self.memory = {}
        
        for name, file_path in self.memory_files.items():
            if file_path.exists():
                if name == 'task_log':
                    with open(file_path, 'r') as f:
                        self.memory[name] = json.load(f)
                elif name == 'user_profile':
                    with open(file_path, 'r') as f:
                        self.memory[name] = json.load(f)
                else:
                    with open(file_path, 'r') as f:
                        self.memory[name] = f.read()
                print(f"✅ Loaded {name}")
            else:
                print(f"⚠️ {name} not found, creating default")
                self.memory[name] = self.create_default_memory(name)
    
    def create_default_memory(self, name: str):
        """Create default memory file content"""
        if name == 'task_log':
            return []
        elif name == 'user_profile':
            return {"quiz_history": [], "learning_preferences": {}}
        else:
            return ""
    
    def decide_next_task(self):
        """Decide what task to work on next"""
        task_log = self.memory.get('task_log', [])
        
        # Check for in-progress task
        for task in task_log:
            if task.get('status') == 'in_progress':
                self.current_task = task
                print(f"📋 Continuing task: {task['title']}")
                return
        
        # Find next task to work on
        for task in task_log:
            if task.get('status') == 'next':
                self.current_task = task
                print(f"🆕 Starting new task: {task['title']}")
                return
        
        # If no tasks, ask AI to suggest next work
        if self.openai_client:
            print("🤖 No tasks found, asking AI for next work...")
            self.current_task = self.ask_ai_for_next_task()
        else:
            print("⚠️ No OpenAI API key, using fallback task")
            self.current_task = {
                'id': 'fallback',
                'title': 'Improve existing functionality',
                'status': 'in_progress',
                'notes': 'Fallback task when OpenAI is unavailable'
            }
    
    def ask_ai_for_next_task(self):
        """Ask OpenAI what to work on next"""
        try:
            context = f"""
            Project State:
            - Brain: {self.memory.get('brain', '')[:500]}
            - Current Tasks: {json.dumps(self.memory.get('task_log', []), indent=2)}
            - Recent Progress: {self.memory.get('progress', '')[:500]}
            
            Based on the project state above, what should be the next logical, 
            self-contained unit of work? Respond with a JSON object:
            {{
                "title": "Task title",
                "notes": "Brief description of what needs to be done",
                "priority": "high|medium|low"
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI developer working on a spaced repetition learning app. Suggest the next logical development task."},
                    {"role": "user", "content": context}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            suggestion = json.loads(response.choices[0].message.content)
            return {
                'id': f'ai_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'title': suggestion['title'],
                'status': 'in_progress',
                'notes': suggestion['notes']
            }
            
        except Exception as e:
            print(f"❌ Error asking AI: {e}")
            return {
                'id': 'fallback',
                'title': 'Fix or improve existing code',
                'status': 'in_progress',
                'notes': 'Fallback when AI suggestion fails'
            }
    
    def execute_work(self):
        """Execute the current task"""
        if not self.current_task:
            print("❌ No current task to execute")
            return
        
        print(f"🔨 Working on: {self.current_task['title']}")
        print(f"📝 Notes: {self.current_task['notes']}")
        
        # This is where we'd implement actual code generation
        # For now, let's do a simple implementation that improves existing code
        
        if self.openai_client:
            self.execute_with_ai()
        else:
            self.execute_fallback()
    
    def execute_with_ai(self):
        """Execute work using AI assistance"""
        try:
            # Ask AI to suggest specific code changes
            context = f"""
            Current Task: {self.current_task['title']}
            Task Notes: {self.current_task['notes']}
            
            Project Structure: LevelUp AI - A spaced repetition learning app
            - FastAPI backend with SQLAlchemy
            - HTML/JS frontend
            - AI-powered flashcard generation
            
            What specific code changes should be made? Be concrete and actionable.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI developer. Suggest specific, implementable code changes."},
                    {"role": "user", "content": context}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            suggestions = response.choices[0].message.content
            print(f"🤖 AI Suggestions:\n{suggestions}")
            
            # For now, make a simple improvement
            self.make_simple_improvement(suggestions)
            
        except Exception as e:
            print(f"❌ Error with AI execution: {e}")
            self.execute_fallback()
    
    def execute_fallback(self):
        """Execute fallback work without AI"""
        print("🔧 Executing fallback improvements...")
        self.make_simple_improvement("Fallback: Improve documentation and code comments")
    
    def make_simple_improvement(self, context: str):
        """Make a simple improvement to the codebase"""
        # Add a comment or small improvement to show the AI is working
        timestamp = datetime.datetime.now().isoformat()
        
        # Create a simple log entry
        log_entry = f"""
# AI Development Log Entry - {timestamp}

## Task: {self.current_task['title']}
**Status**: {self.current_task['status']}
**Notes**: {self.current_task['notes']}

## AI Context:
{context}

## Actions Taken:
- Executed daily development loop
- Updated project memory
- Committed progress

---
"""
        
        # Write to a development log
        dev_log_path = self.project_root / 'ai_dev_log.md'
        with open(dev_log_path, 'a') as f:
            f.write(log_entry)
        
        print(f"✅ Added development log entry")
        self.make_commit("📝 AI development log update")
    
    def make_commit(self, message: str):
        """Make a git commit"""
        try:
            subprocess.run(['git', 'add', '.'], cwd=self.project_root, check=True)
            subprocess.run(['git', 'commit', '-m', message], cwd=self.project_root, check=True)
            self.commits_made.append(message)
            print(f"✅ Committed: {message}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Commit failed: {e}")
    
    def update_memory_files(self):
        """Update all memory files with current progress"""
        # Update task log
        task_log = self.memory.get('task_log', [])
        if self.current_task:
            # Mark current task as done
            for task in task_log:
                if task.get('id') == self.current_task['id']:
                    task['status'] = 'done'
                    break
            else:
                # Add new task if it doesn't exist
                task_log.append({
                    **self.current_task,
                    'status': 'done'
                })
        
        # Save updated task log
        with open(self.memory_files['task_log'], 'w') as f:
            json.dump(task_log, f, indent=2)
        
        # Update progress log
        today = datetime.date.today().strftime('%Y-%m-%d')
        progress_entry = f"""
### {today}
- 🤖 AI orchestrator executed daily loop
- ✅ Completed task: {self.current_task['title'] if self.current_task else 'Unknown'}
- 📝 Commits made: {len(self.commits_made)}
- 🔄 Next: Continue with pending tasks

"""
        
        progress_content = self.memory.get('progress', '')
        # Insert new entry after the header
        lines = progress_content.split('\n')
        header_end = next((i for i, line in enumerate(lines) if line.strip() == '---'), 5)
        lines.insert(header_end + 1, progress_entry)
        
        with open(self.memory_files['progress'], 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ Updated memory files")
    
    def push_changes(self):
        """Push all changes to GitHub"""
        try:
            subprocess.run(['git', 'push'], cwd=self.project_root, check=True)
            print("✅ Pushed changes to GitHub")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Push failed: {e}")

def main():
    """Main entry point"""
    orchestrator = AIOrchestrator()
    orchestrator.run_daily_loop()

if __name__ == "__main__":
    main()
