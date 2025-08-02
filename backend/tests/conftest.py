import pytest
from app import create_app, db
from app.models import User, Order, ChatSession
from config import TestingConfig
import json

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return auth headers"""
    # Register a test user
    response = client.post('/users/register', json={
        'email': 'test@example.com',
        'password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User'
    })
    
    data = json.loads(response.data)
    token = data['access_token']
    
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def sample_user(app):
    """Create a sample user"""
    with app.app_context():
        user = User(
            email='sample@example.com',
            first_name='Sample',
            last_name='User'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def sample_order(app, sample_user):
    """Create a sample order"""
    with app.app_context():
        order = Order(
            id='PB001234',
            user_id=sample_user.id,
            status='preparing',
            items='[{"name": "Classic PerfBurger", "quantity": 1, "price": 12.99}]',
            total_amount=12.99,
            delivery_address='123 Test St, Test City, TC 12345'
        )
        db.session.add(order)
        db.session.commit()
        return order
