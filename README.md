# AI-Powered Chatbot Order Status Service

A polite, customer-focused chatbot service built with Python/Flask that provides accurate information about burger orders and restaurant services.

## Project Overview

This chatbot specializes in **PerfBurger** - a premium burger delivery service. The bot assists customers with:
- Order status inquiries
- Menu information
- Delivery tracking
- Customer support

## Features

- 🔐 JWT-based authentication
- 💬 AI-powered chat responses
- 📚 RAG (Retrieval-Augmented Generation) with knowledge base
- 🧪 Comprehensive testing suite
- 🚀 CI/CD pipeline ready
- ☁️ Cloud deployment configurations

## Tech Stack

- **Backend**: Python 3.9+, Flask 3.0+, SQLAlchemy 2.0+
- **Authentication**: JWT tokens (Flask-JWT-Extended)
- **AI/LLM**: OpenAI GPT integration with RAG
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Testing**: pytest, Postman, VS Code REST Client
- **Security**: bcrypt password hashing, CORS support
- **Deployment**: Docker, Kubernetes
- **CI/CD**: GitHub Actions ready

## Getting Started

### Prerequisites

- Python 3.9+
- pip
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-chatbot-perf-burger
```

2. Create virtual environment:
```bash
python -m venv venv
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

See the `deployment/` directory for Kubernetes manifests and cloud deployment configurations.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
