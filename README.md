# PerfBurger AI Chatbot - Monorepo

A modern, full-stack AI-powered chatbot service for PerfBurger - a premium burger delivery service. Built with a clean monorepo structure separating backend and frontend concerns.

## 🚀 Live Demo
- **Frontend**: https://delightful-ground-0a878f803.2.azurestaticapps.net/
- **Backend API**: https://perfburger-chatbot-a6eph3fsavbwc5bm.westeurope-01.azurewebsites.net
- **Health Check**: https://perfburger-chatbot-a6eph3fsavbwc5bm.westeurope-01.azurewebsites.net/health

## Project Overview

This project was developed following an 8-part implementation plan:

1. **User Stories & MVP Definition**: Detailed in `User-Stories.md`
2. **Project Scaffolding**: Flask/React monorepo structure
3. **Authentication**: JWT-based user authentication
4. **Core Chat API**: OpenAI GPT integration
5. **RAG Implementation**: Knowledge base with menu, FAQs, and policies
6. **Automated Testing**: Comprehensive test suite with mocks
7. **CI/CD Pipeline**: GitHub Actions automation
8. **Cloud Deployment**: Azure Web Apps and Static Web Apps

## Features

### 🔙 Backend
- 🔐 JWT-based authentication
- 🤖 OpenAI GPT integration with enhanced error handling
- 📚 RAG with knowledge base (menu, FAQs, policies)
- 💾 SQLite database with chat session management
- 🩺 Health checks and debug endpoints
- 📊 Comprehensive logging for Azure troubleshooting

### 🎨 Frontend
- ⚡ Vite + React + TypeScript
- 🎨 Modern glassmorphism design with pure CSS
- 📝 Markdown rendering for chat messages
- 📱 Responsive design
- 🔌 Axios API integration
- 🎯 Lucide React icons

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend Runtime** | Python 3.10+ |
| **Backend Framework** | Flask 3.0+, SQLAlchemy 2.0+ |
| **AI/LLM** | OpenAI GPT-3.5-turbo with RAG |
| **Authentication** | JWT tokens (Flask-JWT-Extended) |
| **Database** | SQLite (dev/Azure), PostgreSQL ready |
| **Frontend Framework** | React 19.1+ with TypeScript |
| **Build Tool** | Vite 7.0+ |
| **Styling** | Pure CSS with modern patterns |
| **HTTP Client** | Axios |
| **Testing** | pytest (backend) |
| **Deployment** | Azure Web Apps + Static Web Apps |

## Project Structure

```
ai-chatbot-perf-burger/
├── backend/                               # Python Flask API
│   ├── app/                              # Application modules
│   │   ├── auth/                         # Authentication blueprint
│   │   ├── chat/                         # Chat functionality
│   │   ├── orders/                       # Order management
│   │   ├── models/                       # Database models
│   │   └── utils/                        # Utilities (LLM, knowledge base)
│   ├── tests/                            # Backend test suite
│   ├── knowledge_base/                   # RAG knowledge base files
│   │   ├── menu.json                     # Restaurant menu data
│   │   ├── faqs.yaml                     # Frequently asked questions
│   │   └── policies.json                 # Company policies
│   ├── instance/                         # Database files (gitignored)
│   ├── requirements.txt                  # Python dependencies
│   └── run.py                           # Application entry point
├── frontend/                             # React TypeScript UI
│   ├── src/                             # React components and services
│   ├── public/                          # Static assets
│   └── package.json                     # Node.js dependencies
├── .github/workflows/                    # CI/CD pipelines
├── FRONTEND_DEPLOYMENT.md               # Frontend deployment guide
├── User-Stories.md                      # User stories and requirements
└── README.md                           # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- OpenAI API key (optional, for AI features)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
py -3.10 -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python init_db.py

# Run the application
python run.py
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# With coverage
pytest --cov=app tests/
```

## API Reference

### Current Active Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/health` | Health check | No |
| `POST` | `/users/register` | User registration | No |
| `POST` | `/users/login` | User authentication | No |
| `POST` | `/chat/` | Chat with AI assistant | Yes |
| `POST` | `/orders/` | Create order from chat | Yes |
| `GET` | `/orders/lookup/<id>` | Lookup order by ID | Yes |
| `GET` | `/debug/llm-status` | Check LLM configuration | No |
| `GET` | `/debug/environment` | Environment info | No |

## Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# Database
DATABASE_URL=sqlite:///instance/chatbot.db

# OpenAI (optional for AI features)
OPENAI_API_KEY=your-openai-api-key

# Knowledge Base
KNOWLEDGE_BASE_PATH=knowledge_base/
```

## Deployment

### Cloud Infrastructure
- **Backend**: Azure App Service (Python Web App)
- **Frontend**: Azure Static Web Apps
- **Database**: SQLite (development/testing)
- **CI/CD**: GitHub Actions
- **Monitoring**: Azure Application Insights

### Deployment Guides
- **Frontend**: See [FRONTEND_DEPLOYMENT.md](./FRONTEND_DEPLOYMENT.md) for detailed Azure Static Web Apps setup
- **Backend**: Automatically deployed via GitHub Actions to Azure App Service

### Environment Variables (Production)
Production environment variables are managed through Azure App Service Configuration:

```bash
FLASK_ENV=production
DATABASE_URL=sqlite:///instance/chatbot.db  # or PostgreSQL for scale
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=production-key
CORS_ORIGINS=https://delightful-ground-0a878f803.azurestaticapps.net
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **404 on API endpoints** | Ensure server is running: `python run.py` |
| **Database errors** | Run: `python init_db.py` |
| **JWT errors** | Check `JWT_SECRET_KEY` in `.env` |
| **Knowledge base not loading** | Verify files exist in `knowledge_base/` |
| **Frontend build fails** | Check Node.js version (18+) |
| **API calls fail** | Verify backend CORS configuration |

## Testing

### Test Coverage Includes:
- ✅ Authentication flows
- ✅ Chat functionality with mocked LLM
- ✅ Order creation and lookup
- ✅ Knowledge base retrieval
- ✅ Error cases and edge scenarios

### API Testing Options:
1. **Postman Collection**: `PerfBurger_API_Collection.postman_collection.json`
2. **Backend Unit Tests**: `pytest` in `/backend`
3. **Frontend Integration**: Use the deployed frontend app

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Submit a pull request

## License

MIT License
