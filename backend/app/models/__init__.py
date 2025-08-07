from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy='dynamic')
    chat_sessions = db.relationship('ChatSession', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat()
        }

class Order(db.Model):
    """Order model for tracking customer orders"""
    id = db.Column(db.String(10), primary_key=True)  # Custom order ID like "PB001234"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='received')  # received, preparing, cooking, ready, out_for_delivery, delivered, cancelled
    items = db.Column(db.Text, nullable=False)  # JSON string of ordered items
    total_amount = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.Text, nullable=True)  # Made nullable since addresses not required
    estimated_delivery = db.Column(db.DateTime, nullable=True)
    actual_delivery = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Optional fields for delivery tracking
    driver_name = db.Column(db.String(100), nullable=True)
    driver_phone = db.Column(db.String(20), nullable=True)
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'id': self.id,
            'status': self.status,
            'items': self.items,
            'total_amount': self.total_amount,
            'delivery_address': self.delivery_address,
            'estimated_delivery': self.estimated_delivery.isoformat() if self.estimated_delivery else None,
            'actual_delivery': self.actual_delivery.isoformat() if self.actual_delivery else None,
            'created_at': self.created_at.isoformat(),
            'driver_name': self.driver_name,
            'driver_phone': self.driver_phone
        }

class ChatSession(db.Model):
    """Chat session model for tracking conversations"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.String(36), nullable=False, unique=True)  # UUID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    messages = db.relationship('ChatMessage', backref='session', lazy='dynamic', cascade='all, delete-orphan')

class ChatMessage(db.Model):
    """Individual chat messages"""
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_session.id'), nullable=False)
    message_type = db.Column(db.String(10), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional metadata
    retrieved_context = db.Column(db.Text, nullable=True)  # For RAG context
    
    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'type': self.message_type,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }
