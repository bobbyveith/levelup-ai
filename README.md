# 🚀 LevelUp AI

Smart Learning Platform with AI-Powered Flashcards and Quizzes

## 🏗️ Project Structure

```
LevelUp/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── core/           # Configuration & database
│   │   ├── api/            # API routes & endpoints
│   │   ├── models/         # Data models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI application
│   └── requirements.txt    # Backend dependencies
├── frontend/               # Frontend assets
│   ├── static/            # CSS, JS, images
│   └── templates/         # HTML templates
├── ai_committer/          # AI automation scripts
├── data/                  # JSON data storage
├── tests/                 # Test files
├── run.py                # Application runner
└── requirements.txt      # Root requirements
```

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Application**
   ```bash
   python run.py
   ```

3. **Access the Application**
   - Web App: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 🔧 Development

### Backend Development

The backend follows FastAPI best practices with:
- **Routers**: Organized by feature (flashcards, quiz, youtube)
- **Schemas**: Pydantic models for validation
- **Services**: Business logic layer
- **Models**: Data models
- **Config**: Centralized configuration

### Frontend Development

The frontend is a modern single-page application with:
- **Responsive Design**: Mobile-first CSS
- **Modern JavaScript**: ES6+ classes and async/await
- **Component-based**: Modular JavaScript classes
- **Real-time Updates**: Live interaction with FastAPI backend

### API Endpoints

- `GET /` - Main application
- `GET /health` - Health check
- `GET /api/v1/flashcards/` - Get all flashcards
- `POST /api/v1/flashcards/` - Create flashcard
- `POST /api/v1/quiz/generate` - Generate quiz
- `GET /api/v1/youtube/` - Get YouTube cards
- `POST /api/v1/youtube/extract` - Extract from YouTube

## 🎯 Features

### ✅ Implemented
- Modern FastAPI structure
- Flashcard management
- Quiz generation
- Responsive UI
- API documentation
- Health monitoring

### 🚧 In Progress
- YouTube content extraction
- AI-powered flashcard generation
- User authentication
- Progress tracking

### 📋 Planned
- Real-time collaboration
- Mobile app
- Advanced analytics
- Multi-language support

## 🛠️ Configuration

Create a `.env` file in the root directory:

```env
# App Configuration
APP_NAME="LevelUp AI"
DEBUG=true

# API Configuration
API_V1_PREFIX="/api/v1"

# OpenAI (optional)
OPENAI_API_KEY="your-api-key-here"

# Server Configuration
HOST="0.0.0.0"
PORT=8000
```

## 📊 Database

Currently using JSON files for data storage:
- `data/flashcards.json` - Flashcard data
- `data/youtube_cards.json` - YouTube video data
- `data/user_profile.json` - User preferences

## 🧪 Testing

```bash
cd backend
pytest
```

## 📖 Documentation

- API Documentation: Available at `/docs` when running
- Interactive API: Available at `/redoc` when running

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- OpenAI for AI capabilities
- Modern web technologies for the frontend

---

**Happy Learning! 🎓** 