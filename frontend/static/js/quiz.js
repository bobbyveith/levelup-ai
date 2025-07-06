// LevelUp AI - Quiz JavaScript

class QuizManager {
    constructor() {
        this.currentQuiz = null;
        this.currentQuestionIndex = 0;
        this.score = 0;
        this.userAnswers = [];
        this.apiBaseUrl = '/api/v1';
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Quiz generation form
        const generateBtn = document.getElementById('generate-quiz-btn');
        if (generateBtn) {
            generateBtn.addEventListener('click', this.generateQuiz.bind(this));
        }

        // Navigation buttons
        const nextBtn = document.getElementById('next-question-btn');
        const prevBtn = document.getElementById('prev-question-btn');
        const submitBtn = document.getElementById('submit-quiz-btn');

        if (nextBtn) nextBtn.addEventListener('click', this.nextQuestion.bind(this));
        if (prevBtn) prevBtn.addEventListener('click', this.previousQuestion.bind(this));
        if (submitBtn) submitBtn.addEventListener('click', this.submitQuiz.bind(this));
    }

    async generateQuiz() {
        const numQuestions = document.getElementById('num-questions')?.value || 5;
        const category = document.getElementById('category')?.value || null;
        const difficulty = document.getElementById('difficulty')?.value || null;

        const requestData = {
            num_questions: parseInt(numQuestions),
            title: "Generated Quiz",
            category: category,
            difficulty: difficulty
        };

        try {
            this.showLoading('Generating quiz...');
            
            const response = await fetch(`${this.apiBaseUrl}/quiz/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const quiz = await response.json();
            this.currentQuiz = quiz;
            this.currentQuestionIndex = 0;
            this.score = 0;
            this.userAnswers = [];
            
            this.displayQuiz();
            this.hideLoading();
            
        } catch (error) {
            console.error('Error generating quiz:', error);
            this.showError('Failed to generate quiz. Please try again.');
            this.hideLoading();
        }
    }

    displayQuiz() {
        const quizContainer = document.getElementById('quiz-container');
        if (!quizContainer || !this.currentQuiz) return;

        const question = this.currentQuiz.questions[this.currentQuestionIndex];
        if (!question) return;

        quizContainer.innerHTML = `
            <div class="quiz-header">
                <h2>${this.currentQuiz.title}</h2>
                <p class="question-counter">Question ${this.currentQuestionIndex + 1} of ${this.currentQuiz.questions.length}</p>
            </div>
            
            <div class="question-card">
                <h3 class="question-title">${question.question}</h3>
                
                <div class="options-container">
                    <ul class="options-list">
                        ${question.options.map((option, index) => `
                            <li class="option-item">
                                <button class="option-button" onclick="quizManager.selectAnswer(${index}, '${option}')">
                                    ${option}
                                </button>
                            </li>
                        `).join('')}
                    </ul>
                </div>
                
                <div class="quiz-navigation">
                    <button class="btn btn-secondary" onclick="quizManager.previousQuestion()" 
                            ${this.currentQuestionIndex === 0 ? 'disabled' : ''}>
                        Previous
                    </button>
                    
                    <div class="question-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${((this.currentQuestionIndex + 1) / this.currentQuiz.questions.length) * 100}%"></div>
                        </div>
                    </div>
                    
                    ${this.currentQuestionIndex === this.currentQuiz.questions.length - 1 ? 
                        '<button class="btn btn-success" onclick="quizManager.submitQuiz()">Submit Quiz</button>' :
                        '<button class="btn btn-primary" onclick="quizManager.nextQuestion()">Next</button>'
                    }
                </div>
            </div>
        `;
    }

    selectAnswer(index, answer) {
        // Remove previous selection
        document.querySelectorAll('.option-button').forEach(btn => {
            btn.classList.remove('selected');
        });

        // Add selection to clicked button
        event.target.classList.add('selected');

        // Store answer
        this.userAnswers[this.currentQuestionIndex] = {
            questionIndex: this.currentQuestionIndex,
            selectedAnswer: answer,
            isCorrect: answer === this.currentQuiz.questions[this.currentQuestionIndex].answer
        };
    }

    nextQuestion() {
        if (this.currentQuestionIndex < this.currentQuiz.questions.length - 1) {
            this.currentQuestionIndex++;
            this.displayQuiz();
        }
    }

    previousQuestion() {
        if (this.currentQuestionIndex > 0) {
            this.currentQuestionIndex--;
            this.displayQuiz();
        }
    }

    submitQuiz() {
        if (!this.currentQuiz) return;

        // Calculate score
        this.score = this.userAnswers.filter(answer => answer && answer.isCorrect).length;
        
        this.displayResults();
    }

    displayResults() {
        const quizContainer = document.getElementById('quiz-container');
        if (!quizContainer) return;

        const percentage = Math.round((this.score / this.currentQuiz.questions.length) * 100);
        const passed = percentage >= 70;

        quizContainer.innerHTML = `
            <div class="quiz-results">
                <h2>Quiz Complete!</h2>
                
                <div class="score-summary">
                    <div class="score-circle ${passed ? 'passed' : 'failed'}">
                        <span class="score-percentage">${percentage}%</span>
                    </div>
                    
                    <div class="score-details">
                        <p><strong>Score:</strong> ${this.score} out of ${this.currentQuiz.questions.length}</p>
                        <p><strong>Status:</strong> ${passed ? 'Passed' : 'Failed'}</p>
                    </div>
                </div>
                
                <div class="question-review">
                    <h3>Review Your Answers</h3>
                    ${this.currentQuiz.questions.map((question, index) => {
                        const userAnswer = this.userAnswers[index];
                        const isCorrect = userAnswer && userAnswer.isCorrect;
                        
                        return `
                            <div class="review-item ${isCorrect ? 'correct' : 'incorrect'}">
                                <h4>Question ${index + 1}</h4>
                                <p class="question-text">${question.question}</p>
                                <p class="correct-answer"><strong>Correct Answer:</strong> ${question.answer}</p>
                                ${userAnswer ? 
                                    `<p class="user-answer"><strong>Your Answer:</strong> ${userAnswer.selectedAnswer}</p>` :
                                    '<p class="user-answer"><strong>Your Answer:</strong> <em>Not answered</em></p>'
                                }
                            </div>
                        `;
                    }).join('')}
                </div>
                
                <div class="quiz-actions">
                    <button class="btn btn-primary" onclick="quizManager.resetQuiz()">Take Another Quiz</button>
                    <button class="btn btn-secondary" onclick="quizManager.reviewFlashcards()">Review Flashcards</button>
                </div>
            </div>
        `;
    }

    resetQuiz() {
        this.currentQuiz = null;
        this.currentQuestionIndex = 0;
        this.score = 0;
        this.userAnswers = [];
        
        // Reset to initial state
        const quizContainer = document.getElementById('quiz-container');
        if (quizContainer) {
            quizContainer.innerHTML = '<p>Click "Generate Quiz" to start!</p>';
        }
    }

    async reviewFlashcards() {
        // Redirect to flashcards page or load flashcards
        window.location.href = '/flashcards';
    }

    showLoading(message = 'Loading...') {
        const quizContainer = document.getElementById('quiz-container');
        if (quizContainer) {
            quizContainer.innerHTML = `
                <div class="loading-container">
                    <div class="spinner"></div>
                    <p>${message}</p>
                </div>
            `;
        }
    }

    hideLoading() {
        // Loading will be hidden when content is displayed
    }

    showError(message) {
        const quizContainer = document.getElementById('quiz-container');
        if (quizContainer) {
            quizContainer.innerHTML = `
                <div class="error-container">
                    <div class="error-icon">⚠️</div>
                    <p class="error-message">${message}</p>
                    <button class="btn btn-primary" onclick="quizManager.resetQuiz()">Try Again</button>
                </div>
            `;
        }
    }
}

// Initialize the quiz manager when the page loads
let quizManager;
document.addEventListener('DOMContentLoaded', function() {
    quizManager = new QuizManager();
});

// Flashcard functionality
class FlashcardManager {
    constructor() {
        this.flashcards = [];
        this.currentCardIndex = 0;
        this.isFlipped = false;
        this.apiBaseUrl = '/api/v1';
        
        this.loadFlashcards();
    }

    async loadFlashcards() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/flashcards/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.flashcards = await response.json();
            this.displayCurrentCard();
            
        } catch (error) {
            console.error('Error loading flashcards:', error);
            this.showError('Failed to load flashcards');
        }
    }

    displayCurrentCard() {
        const flashcardContainer = document.getElementById('flashcard-container');
        if (!flashcardContainer || this.flashcards.length === 0) return;

        const card = this.flashcards[this.currentCardIndex];
        if (!card) return;

        flashcardContainer.innerHTML = `
            <div class="flashcard-wrapper">
                <div class="card-counter">
                    <span>${this.currentCardIndex + 1} / ${this.flashcards.length}</span>
                </div>
                
                <div class="flashcard ${this.isFlipped ? 'flipped' : ''}" onclick="flashcardManager.flipCard()">
                    <div class="flashcard-content">
                        ${this.isFlipped ? 
                            `<div class="answer">${card.answer}</div>` : 
                            `<div class="question">${card.question}</div>`
                        }
                    </div>
                </div>
                
                <div class="flashcard-navigation">
                    <button class="btn btn-secondary" onclick="flashcardManager.previousCard()" 
                            ${this.currentCardIndex === 0 ? 'disabled' : ''}>
                        Previous
                    </button>
                    
                    <button class="btn btn-secondary" onclick="flashcardManager.flipCard()">
                        ${this.isFlipped ? 'Show Question' : 'Show Answer'}
                    </button>
                    
                    <button class="btn btn-primary" onclick="flashcardManager.nextCard()" 
                            ${this.currentCardIndex === this.flashcards.length - 1 ? 'disabled' : ''}>
                        Next
                    </button>
                </div>
                
                <div class="card-info">
                    <p class="category">Category: ${card.category || 'General'}</p>
                    <p class="difficulty">Difficulty: ${card.difficulty || 'Medium'}</p>
                </div>
            </div>
        `;
    }

    flipCard() {
        this.isFlipped = !this.isFlipped;
        this.displayCurrentCard();
    }

    nextCard() {
        if (this.currentCardIndex < this.flashcards.length - 1) {
            this.currentCardIndex++;
            this.isFlipped = false;
            this.displayCurrentCard();
        }
    }

    previousCard() {
        if (this.currentCardIndex > 0) {
            this.currentCardIndex--;
            this.isFlipped = false;
            this.displayCurrentCard();
        }
    }

    showError(message) {
        const flashcardContainer = document.getElementById('flashcard-container');
        if (flashcardContainer) {
            flashcardContainer.innerHTML = `
                <div class="error-container">
                    <div class="error-icon">⚠️</div>
                    <p class="error-message">${message}</p>
                    <button class="btn btn-primary" onclick="flashcardManager.loadFlashcards()">Retry</button>
                </div>
            `;
        }
    }
}

// Initialize flashcard manager if on flashcards page
let flashcardManager;
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('flashcard-container')) {
        flashcardManager = new FlashcardManager();
    }
}); 