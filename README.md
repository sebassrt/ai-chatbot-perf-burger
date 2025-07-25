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

- **Backend**: Python 3.9+, Flask, SQLAlchemy
- **Authentication**: JWT tokens
- **AI/LLM**: OpenAI GPT integration
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Testing**: pytest
- **Deployment**: Docker, Kubernetes
- **CI/CD**: GitHub Actions

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
flask db upgrade
```

6. Run the application:
```bash
python run.py
```

## API Endpoints

- `POST /users/register` - User registration
- `POST /users/login` - User authentication
- `POST /chat` - Chat with the AI assistant (authenticated)
- `GET /orders/{id}` - Get order status
- `GET /health` - Health check endpoint

## Project Structure

```
ai-chatbot-perf-burger/
├── app/                    # Main application package
├── tests/                  # Test suite
├── knowledge_base/         # RAG knowledge base
├── deployment/             # Deployment configurations
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
└── README.md              # This file
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
