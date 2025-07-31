from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
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
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app
