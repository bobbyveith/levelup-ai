// LevelUp AI - Main Application JavaScript

class LevelUpApp {
    constructor() {
        this.apiBaseUrl = '/api/v1';
        this.currentSection = 'home';
        this.stats = {
            totalFlashcards: 0,
            quizzesTaken: 0,
            averageScore: 0
        };
        
        this.initialize();
    }

    initialize() {
        this.loadStats();
        this.setupEventListeners();
        this.checkAPIHealth();
    }

    setupEventListeners() {
        // Flashcard form submission
        const flashcardForm = document.getElementById('flashcard-form');
        if (flashcardForm) {
            flashcardForm.addEventListener('submit', this.handleFlashcardSubmit.bind(this));
        }

        // Navigation
        document.addEventListener('keydown', this.handleKeyboardNavigation.bind(this));
    }

    async checkAPIHealth() {
        try {
            const response = await fetch('/health');
            if (response.ok) {
                console.log('API is healthy');
            }
        } catch (error) {
            console.error('API health check failed:', error);
            this.showNotification('API connection issues detected', 'warning');
        }
    }

    async loadStats() {
        try {
            // Load flashcards count
            const flashcardsResponse = await fetch(`${this.apiBaseUrl}/flashcards/`);
            if (flashcardsResponse.ok) {
                const flashcards = await flashcardsResponse.json();
                this.stats.totalFlashcards = flashcards.length;
            }

            this.updateStatsDisplay();
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    updateStatsDisplay() {
        const totalFlashcardsEl = document.getElementById('total-flashcards');
        const quizzesTakenEl = document.getElementById('quizzes-taken');
        const averageScoreEl = document.getElementById('average-score');

        if (totalFlashcardsEl) totalFlashcardsEl.textContent = this.stats.totalFlashcards;
        if (quizzesTakenEl) quizzesTakenEl.textContent = this.stats.quizzesTaken;
        if (averageScoreEl) averageScoreEl.textContent = `${this.stats.averageScore}%`;
    }

    showSection(sectionId) {
        // Hide all sections
        const sections = document.querySelectorAll('.content-sections > div');
        sections.forEach(section => {
            section.style.display = 'none';
        });

        // Show target section
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.style.display = 'block';
            this.currentSection = sectionId;
        }
    }

    hideAllSections() {
        const sections = document.querySelectorAll('.content-sections > div');
        sections.forEach(section => {
            section.style.display = 'none';
        });
        this.currentSection = 'home';
    }

    async handleFlashcardSubmit(event) {
        event.preventDefault();
        
        const formData = {
            question: document.getElementById('flashcard-question').value,
            answer: document.getElementById('flashcard-answer').value,
            category: document.getElementById('flashcard-category').value || null,
            difficulty: document.getElementById('flashcard-difficulty').value,
            tags: document.getElementById('flashcard-tags').value.split(',').map(tag => tag.trim()).filter(tag => tag)
        };

        try {
            const response = await fetch(`${this.apiBaseUrl}/flashcards/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            this.showNotification('Flashcard created successfully!', 'success');
            this.resetFlashcardForm();
            this.loadStats(); // Refresh stats
            
        } catch (error) {
            console.error('Error creating flashcard:', error);
            this.showNotification('Failed to create flashcard. Please try again.', 'error');
        }
    }

    resetFlashcardForm() {
        const form = document.getElementById('flashcard-form');
        if (form) {
            form.reset();
        }
    }

    handleKeyboardNavigation(event) {
        // ESC key to close sections
        if (event.key === 'Escape') {
            this.hideAllSections();
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        // Add to page
        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }
}

// Global functions for HTML onclick handlers
function loadFlashcards() {
    app.showSection('flashcard-section');
    if (window.flashcardManager) {
        flashcardManager.loadFlashcards();
    }
}

function showCreateFlashcardForm() {
    app.showSection('create-flashcard-section');
}

function hideCreateFlashcardForm() {
    app.hideAllSections();
}

async function extractFromYouTube() {
    const url = document.getElementById('youtube-url').value;
    if (!url) {
        app.showNotification('Please enter a YouTube URL', 'warning');
        return;
    }

    try {
        app.showNotification('Extracting content from YouTube...', 'info');
        
        const response = await fetch(`${app.apiBaseUrl}/youtube/extract`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        app.showNotification('Content extracted successfully!', 'success');
        
        // Clear the input
        document.getElementById('youtube-url').value = '';
        
        // Refresh flashcards
        app.loadStats();
        
    } catch (error) {
        console.error('Error extracting YouTube content:', error);
        app.showNotification('Failed to extract YouTube content. Feature coming soon!', 'error');
    }
}

// Initialize the app when DOM is loaded
let app;
document.addEventListener('DOMContentLoaded', function() {
    app = new LevelUpApp();
});

// Add notification styles dynamically
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            max-width: 400px;
            animation: slideIn 0.3s ease-out;
        }

        .notification-info {
            background-color: #3b82f6;
            color: white;
        }

        .notification-success {
            background-color: #10b981;
            color: white;
        }

        .notification-warning {
            background-color: #f59e0b;
            color: white;
        }

        .notification-error {
            background-color: #ef4444;
            color: white;
        }

        .notification-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .notification-close {
            background: none;
            border: none;
            color: inherit;
            font-size: 1.5rem;
            cursor: pointer;
            margin-left: 1rem;
        }

        .stat-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        }

        .stat-number {
            font-size: 2rem;
            font-weight: 700;
            color: #2563eb;
            margin-bottom: 0.5rem;
        }

        .stat-label {
            color: #64748b;
            font-weight: 500;
        }

        .footer {
            margin-top: 4rem;
            padding: 2rem 0;
            border-top: 1px solid #e2e8f0;
            text-align: center;
            color: #64748b;
        }

        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @media (max-width: 768px) {
            .notification {
                top: 10px;
                right: 10px;
                left: 10px;
                max-width: none;
            }
        }
    `;
    document.head.appendChild(style);
}); 