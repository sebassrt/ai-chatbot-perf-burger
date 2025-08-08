import pytest
from app.models import MenuItem, Category
import json

class TestMenu:
    """Test menu-related endpoints"""
    
    @pytest.fixture
    def sample_menu(self, app):
        """Create sample menu items"""
        with app.app_context():
            # Create categories
            burger_cat = Category(name='Burgers', description='Our signature burgers')
            sides_cat = Category(name='Sides', description='Perfect companions')
            
            # Create menu items
            classic = MenuItem(
                name='Classic Burger',
                description='Our signature burger with premium beef',
                price=10.99,
                category=burger_cat,
                ingredients=['beef patty', 'lettuce', 'tomato', 'cheese'],
                allergens=['dairy', 'gluten']
            )
            
            fries = MenuItem(
                name='French Fries',
                description='Crispy golden fries',
                price=3.99,
                category=sides_cat,
                ingredients=['potatoes', 'salt'],
                allergens=[]
            )
            
            app.db.session.add_all([burger_cat, sides_cat, classic, fries])
            app.db.session.commit()
            
            return [classic, fries]

    def test_get_menu_success(self, client):
        """Test getting full menu"""
        response = client.get('/menu')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'categories' in data
        assert 'items' in data

    def test_get_menu_by_category(self, client, sample_menu):
        """Test filtering menu by category"""
        response = client.get('/menu/Burgers')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['items']) == 1
        assert data['items'][0]['name'] == 'Classic Burger'

    def test_get_menu_invalid_category(self, client):
        """Test getting menu with invalid category"""
        response = client.get('/menu/InvalidCategory')
        
        assert response.status_code == 404

    def test_get_item_details(self, client, sample_menu):
        """Test getting detailed item information"""
        item_id = sample_menu[0].id
        response = client.get(f'/menu/items/{item_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'ingredients' in data
        assert 'allergens' in data

    def test_get_item_not_found(self, client):
        """Test getting non-existent item"""
        response = client.get('/menu/items/999')
        
        assert response.status_code == 404

    def test_search_menu(self, client, sample_menu):
        """Test searching menu items"""
        response = client.get('/menu/search?q=burger')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['items']) == 1
        assert 'Classic Burger' in data['items'][0]['name']

    def test_filter_by_allergen(self, client, sample_menu):
        """Test filtering items by allergen"""
        response = client.get('/menu/filter?allergen=dairy')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['items']) == 1  # Only the fries should be returned
