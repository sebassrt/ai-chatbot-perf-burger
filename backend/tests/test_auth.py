import json
import pytest
from app.models import User

class TestAuth:
    """Test authentication endpoints"""
    
    def test_user_registration_success(self, client):
        """Test successful user registration"""
        response = client.post('/users/register', json={
            'email': 'newuser@example.com',
            'password': 'password123',
            'first_name': 'New',
            'last_name': 'User'
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'access_token' in data
        assert data['user']['email'] == 'newuser@example.com'
    
    def test_user_registration_duplicate_email(self, client):
        """Test registration with duplicate email"""
        # First registration
        client.post('/users/register', json={
            'email': 'duplicate@example.com',
            'password': 'password123',
            'first_name': 'First',
            'last_name': 'User'
        })
        
        # Second registration with same email
        response = client.post('/users/register', json={
            'email': 'duplicate@example.com',
            'password': 'password456',
            'first_name': 'Second',
            'last_name': 'User'
        })
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'already registered' in data['error']
    
    def test_user_registration_invalid_data(self, client):
        """Test registration with invalid data"""
        # Missing required fields
        response = client.post('/users/register', json={
            'email': 'incomplete@example.com'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'required' in data['error']
    
    def test_user_login_success(self, client):
        """Test successful login"""
        # Register user first
        client.post('/users/register', json={
            'email': 'login@example.com',
            'password': 'password123',
            'first_name': 'Login',
            'last_name': 'User'
        })
        
        # Login
        response = client.post('/users/login', json={
            'email': 'login@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        assert data['user']['email'] == 'login@example.com'
    
    def test_user_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post('/users/login', json={
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid email or password' in data['error']
    
    def test_get_profile_authenticated(self, client, auth_headers):
        """Test getting profile with valid token"""
        response = client.get('/users/profile', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'user' in data
        assert data['user']['email'] == 'test@example.com'
    
    def test_get_profile_unauthenticated(self, client):
        """Test getting profile without token"""
        response = client.get('/users/profile')
        
        assert response.status_code == 401
