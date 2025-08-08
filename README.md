# PerfBurger AI Chatbot - Monorepo

A modern, full-stack AI-powered chatbot service for PerfBurger - a premium burger delivery service. Built with a clean monorepo structure separating backend and frontend concerns.

## Live Demo
- Backend API: https://perfburger-chatbot-a6eph3fsavbwc5bm.westeurope-01.azurewebsites.net
- Frontend App: https://delightful-ground-0a878f803.2.azurestaticapps.net/
- Healthcheck: https://perfburger-chatbot-a6eph3fsavbwc5bm.westeurope-01.azurewebsites.net/health

## Project Overview

This project was developed following an 8-part implementation plan:

1. **User Stories & MVP Definition**: Detailed in `user-stories.md`
2. **Project Scaffolding**: Flask/React monorepo structure
3. **Authentication**: JWT-based user authentication
4. **Core Chat API**: OpenAI GPT integration
5. **RAG Implementation**: Knowledge base with menu, FAQs, and policies
6. **Automated Testing**: Comprehensive test suite with mocks
7. **CI/CD Pipeline**: GitHub Actions automation
8. **Cloud Deployment**: Azure Web Apps and Static Web Apps

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
└── deployment/       # Deployment configurations
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
flask db upgrade
```

6. Run tests:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/test_chat.py

# Run with verbose output
pytest -v
```

Test coverage includes:
- Authentication flows
- Chat functionality with mocked LLM
- Menu operations
- Knowledge base retrieval
- Error cases and edge scenarios
python init_db.py

# If you need to recreate schema (after model changes):
python recreate_db.py
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

## CI/CD and Deployment

### CI/CD Pipeline

Our GitHub Actions workflows automate:

Backend (`.github/workflows/backend.yml`):
1. Code checkout
2. Python setup and dependencies installation
3. Linting and testing
4. Deployment to Azure App Service

Frontend (`.github/workflows/azure-static-web-apps.yml`):
1. Code checkout
2. Node.js setup and dependencies installation
3. Build process
4. Deployment to Azure Static Web Apps

### Cloud Deployment

The application is deployed on Azure using:
- Backend: Azure App Service (Python Web App)
- Frontend: Azure Static Web Apps
- Database: SQLite (development/testing)
- Monitoring: Azure Application Insights

### Deployment Configuration

1. Backend deployment:
The backend is deployed as a Python Web App on Azure App Service, which automatically handles:
- Python runtime environment
- Dependencies installation from requirements.txt
- WSGI server configuration
- Environment variables management
- SSL/TLS certificates
- Custom domain configuration (if needed)

2. Frontend deployment:
The frontend is deployed using Azure Static Web Apps, which provides:
```yaml
# .github/workflows/azure-static-web-apps.yml
name: Frontend CI/CD
on:
  push:
    branches:
      - main
jobs:
  build_and_deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: Azure/static-web-apps-deploy@v1
      with:
        azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_TOKEN }}
        # Build configuration
        app_location: "/frontend"    # Location of your frontend code
        api_location: ""             # If using Static Web Apps API
        output_location: "dist"      # Build output directory
```

### Environment Variables

Production environment variables are managed through Azure App Service Configuration:

```bash
# Azure App Service Configuration
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@perfburger-db.postgres.database.azure.com/chatbot
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=production-key
CORS_ORIGINS=https://delightful-ground-0a878f803.azurestaticapps.net
```

### Monitoring and Observability

1. Health Check Endpoint: `GET /health`
2. Azure Application Insights integration
3. Structured logging with correlation IDs
4. Performance metrics dashboard

## Bonus Features Implemented

1. **Enhanced Frontend**:
   - React-based chat widget
   - Real-time message updates
   - Markdown support
   - Responsive design

2. **Observability**:
   - Health check endpoint
   - Azure Application Insights
   - Structured logging
   - Performance monitoring

3. **Security**:
   - JWT authentication
   - CORS configuration
   - Rate limiting
   - Input validation

### 🚀 Live Demo
The PerfBurger AI Chatbot is live on Azure:
- **URL**: https://perfburger-chatbot-a6eph3fsavbwc5bm.westeurope-01.azurewebsites.net
- **Health Check**: https://perfburger-chatbot-a6eph3fsavbwc5bm.westeurope-01.azurewebsites.net/health

### Azure Web App
Deployed using Azure Web App with automatic deployment from GitHub. Every push to `main` branch automatically updates the live application.

### Deployment Options
See the `deployment/` directory for additional deployment configurations and scripts.

### Frontend Deployment
For detailed frontend deployment instructions, see [FRONTEND_DEPLOYMENT.md](./FRONTEND_DEPLOYMENT.md) which covers:
- Azure Static Web Apps setup
- GitHub Actions integration
- Environment configuration
- CORS setup
- Troubleshooting common deployment issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
