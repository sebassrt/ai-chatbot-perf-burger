import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    # Use temp directory for SQLite on Azure, or instance directory locally
    if os.environ.get('WEBSITE_HOSTNAME'):  # Running on Azure
        db_path = os.path.join('/tmp', 'chatbot.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/chatbot.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # OpenAI configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Knowledge base configuration
    KNOWLEDGE_BASE_PATH = os.environ.get('KNOWLEDGE_BASE_PATH') or 'knowledge_base/'
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
