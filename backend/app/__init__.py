from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
import logging
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure logging
    if os.environ.get('WEBSITE_HOSTNAME'):  # Running on Azure
        # More verbose logging for Azure
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s: %(message)s'
        )
        app.logger.setLevel(logging.INFO)
        app.logger.info("Application starting on Azure")
        app.logger.info(f"OpenAI API Key configured: {bool(app.config.get('OPENAI_API_KEY'))}")
    else:
        # Local development logging
        logging.basicConfig(level=logging.INFO)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Create database tables
    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from app.models import User, ChatSession, ChatMessage, Order
        db.create_all()
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/users')
    
    from app.chat import bp as chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')
    
    from app.orders import bp as orders_bp
    app.register_blueprint(orders_bp, url_prefix='/orders')
    
    # Register debug blueprint
    from app.debug_routes import debug_bp
    app.register_blueprint(debug_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app
