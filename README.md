# PerfBurger AI Chatbot - Monorepo

A modern, full-stack AI-powered chatbot service for PerfBurger - a premium burger delivery service. Built with a clean monorepo structure separating backend and frontend concerns.

## Project Overview

This application provides a complete chatbot solution with:
- **Backend**: Python/Flask API with OpenAI integration and RAG (Retrieval-Augmented Generation)
- **Frontend**: Modern React TypeScript application with beautiful UI
- **AI Features**: Intelligent responses using knowledge base and chat memory
- **Production Ready**: Azure deployment, CI/CD pipelines, and comprehensive testing

## Monorepo Structure

```
├── backend/           # Python Flask API
│   ├── app/          # Application modules
│   ├── knowledge_base/  # RAG knowledge files
│   ├── tests/        # Backend tests
│   └── requirements.txt
├── frontend/         # React TypeScript UI
│   ├── src/         # React components and services
│   ├── public/      # Static assets
│   └── package.json
├── .github/workflows/  # CI/CD pipelines
└── deployment/       # Docker and K8s configs
```

## Features

### Backend Features
- 🔐 JWT-based authentication
- 🤖 OpenAI GPT integration with enhanced error handling
- 📚 RAG with knowledge base (menu, FAQs, policies)
- 💾 SQLite database with chat session management
- 🩺 Health checks and debug endpoints
- 📊 Comprehensive logging for Azure troubleshooting

### Frontend Features
- ⚡ Vite + React + TypeScript
- 🎨 Modern glassmorphism design with pure CSS
- 📝 Markdown rendering for chat messages
- 📱 Responsive design
- 🔌 Axios API integration
- 🎯 Lucide React icons

## Tech Stack

### Backend
- **Runtime**: Python 3.10+
- **Framework**: Flask 3.0+, SQLAlchemy 2.0+
- **AI/LLM**: OpenAI GPT-3.5-turbo with RAG
- **Auth**: JWT tokens (Flask-JWT-Extended)
- **Database**: SQLite (development/Azure), PostgreSQL ready
- **Testing**: pytest
- **Deployment**: Gunicorn, Azure Web Apps

### Frontend
- **Framework**: React 19.1+ with TypeScript
- **Build Tool**: Vite 7.0+
- **Styling**: Pure CSS with modern design patterns
- **HTTP Client**: Axios
- **Markdown**: react-markdown with rehype-raw
- **Icons**: Lucide React

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
py -3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize database:
```bash
python init_db.py
```

6. Run the application:
```bash
python run.py
```

## API Endpoints

### Authentication
- `POST /users/register` - User registration
- `POST /users/login` - User authentication
- `GET /users/profile` - Get user profile (authenticated)

### Chat
- `POST /chat/` - Chat with the AI assistant (authenticated)
- `GET /chat/sessions` - Get user's chat sessions (authenticated)

### Orders
- `GET /orders` - Get all user orders (authenticated)
- `GET /orders/{id}` - Get specific order status (authenticated)
- `GET /orders/{id}/tracking` - Get order tracking details (authenticated)
- `POST /orders/{id}/issues` - Report order issue (authenticated)

### System
- `GET /health` - Health check endpoint

## Project Structure

```
ai-chatbot-perf-burger/
├── app/                                    # Main application package
│   ├── auth/                              # Authentication blueprint
│   ├── chat/                              # Chat functionality
│   ├── orders/                            # Order management
│   ├── models/                            # Database models
│   └── utils/                             # Utilities (LLM, knowledge base)
├── tests/                                 # Test suite
├── knowledge_base/                        # RAG knowledge base files
│   ├── menu.json                         # Restaurant menu data
│   ├── faqs.yaml                         # Frequently asked questions
│   └── policies.json                     # Company policies
├── deployment/                            # Deployment configurations
│   └── k8s/                              # Kubernetes manifests
├── instance/                              # Database files (gitignored)
├── init_db.py                            # Database initialization script
├── requirements.txt                      # Python dependencies
├── Dockerfile                           # Container configuration
├── .env.example                         # Environment variables template
└── README.md                            # This file
```

## Development

### Running Tests

```bash
pytest
```

### Code Style

```bash
black app/
flake8 app/
```

## Troubleshooting

### Common Issues

**404 Error on API endpoints**
- Ensure the server is running: `python run.py`
- Check that blueprint routes are properly imported in `app/*/__init__.py` files

**Database errors**
- Run database initialization: `python init_db.py`
- Check `.env` file configuration

**JWT Authentication errors**
- Verify JWT_SECRET_KEY is set in `.env`
- Check that Authorization header format is: `Bearer <token>`

**Knowledge base not loading**
- Ensure knowledge base files exist in `knowledge_base/` directory
- Check file permissions and JSON/YAML syntax

## Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# Database
DATABASE_URL=sqlite:///instance/chatbot.db

# OpenAI (optional)
OPENAI_API_KEY=your-openai-api-key

# Knowledge Base
KNOWLEDGE_BASE_PATH=knowledge_base/
```

## Deployment

### 🚀 Live Demo
The PerfBurger AI Chatbot is live on Azure:
- **URL**: https://perfburger-chatbot-a6eph3fsavbwc5bm.westeurope-01.azurewebsites.net
- **Health Check**: https://perfburger-chatbot-a6eph3fsavbwc5bm.westeurope-01.azurewebsites.net/health

### Azure Web App
Deployed using Azure Web App with automatic deployment from GitHub. Every push to `main` branch automatically updates the live application.

### Other Options
See the `deployment/` directory for Kubernetes manifests and other cloud deployment configurations.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
