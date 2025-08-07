from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.orders import bp
from app import db
from app.models import Order, User, ChatSession, ChatMessage
import json
import uuid
import random
import string
from datetime import datetime, timedelta
import os

def load_menu():
    """Load menu data from JSON file"""
    try:
        menu_path = os.path.join(os.path.dirname(__file__), '..', '..', 'knowledge_base', 'menu.json')
        with open(menu_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading menu: {e}")
        return {}

def generate_order_id():
    """Generate a unique order ID in format PB######"""
    return f"PB{''.join(random.choices(string.digits, k=6))}"

def analyze_chat_for_order(session_id, user_id):
    """Analyze chat messages to extract order items"""
    try:
        # Get the chat session
        session = ChatSession.query.filter_by(session_id=session_id, user_id=user_id).first()
        if not session:
            return {"error": "Chat session not found"}, 404
        
        # Get all messages from the session
        messages = ChatMessage.query.filter_by(session_id=session.id).order_by(ChatMessage.timestamp).all()
        
        # Combine all user messages for analysis
        conversation_text = " ".join([msg.content for msg in messages if msg.message_type == 'user'])
        
        # Load menu for validation
        menu = load_menu()
        
        # Simple item extraction (in production, you'd use more sophisticated LLM analysis)
        detected_items = []
        total_amount = 0.0
        
        # Check each menu category for mentioned items
        for category in ['burgers', 'sides', 'drinks', 'desserts']:
            if category in menu:
                for item in menu[category]:
                    item_name = item['name'].lower()
                    conversation_lower = conversation_text.lower()
                    
                    # Simple keyword matching (can be enhanced with LLM)
                    if any(word in conversation_lower for word in item_name.split()):
                        # Try to extract quantity (default to 1)
                        quantity = 1
                        for word in conversation_text.split():
                            if word.isdigit() and int(word) <= 10:  # Reasonable quantity limit
                                quantity = int(word)
                                break
                        
                        # Extract customizations (simple approach)
                        customizations = []
                        if "no onions" in conversation_lower or "without onions" in conversation_lower:
                            customizations.append("no onions")
                        if "extra cheese" in conversation_lower:
                            customizations.append("extra cheese")
                        if "no tomato" in conversation_lower or "without tomato" in conversation_lower:
                            customizations.append("no tomato")
                        
                        detected_items.append({
                            "name": item['name'],
                            "price": float(item['price']),
                            "quantity": quantity,
                            "customizations": customizations,
                            "category": category
                        })
                        
                        total_amount += float(item['price']) * quantity
        
        if not detected_items:
            return {"error": "No menu items detected in conversation"}, 400
        
        return {
            "items": detected_items,
            "total_amount": round(total_amount, 2),
            "conversation_summary": conversation_text[:200] + "..." if len(conversation_text) > 200 else conversation_text
        }, 200
        
    except Exception as e:
        return {"error": f"Failed to analyze chat: {str(e)}"}, 500

@bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    """Create an order from chat conversation analysis"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('session_id'):
            return jsonify({'error': 'session_id is required'}), 400
        
        session_id = data['session_id']
        
        # Analyze chat for order items
        analysis_result, status_code = analyze_chat_for_order(session_id, user_id)
        
        if status_code != 200:
            return jsonify(analysis_result), status_code
        
        # Generate order ID
        order_id = generate_order_id()
        while Order.query.filter_by(id=order_id).first():  # Ensure uniqueness
            order_id = generate_order_id()
        
        # Create the order
        order = Order(
            id=order_id,
            user_id=user_id,
            status='received',
            items=json.dumps(analysis_result['items']),
            total_amount=analysis_result['total_amount'],
            delivery_address="Default address (to be enhanced)",  # Placeholder
            estimated_delivery=datetime.utcnow() + timedelta(minutes=30)  # 30 min estimate
        )
        
        db.session.add(order)
        db.session.commit()
        
        # Prepare response
        order_response = order.to_dict()
        order_response['items'] = analysis_result['items']
        order_response['conversation_summary'] = analysis_result['conversation_summary']
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order_response
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create order', 'details': str(e)}), 500

@bp.route('/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get order details by ID"""
    try:
        user_id = get_jwt_identity()
        
        # Find order - user can only see their own orders
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Parse items JSON
        try:
            items = json.loads(order.items)
        except:
            items = []
        
        order_data = order.to_dict()
        order_data['items'] = items
        
        # Add status description
        status_descriptions = {
            'received': 'Your order has been received and is being processed.',
            'preparing': 'Our kitchen is preparing your delicious meal.',
            'cooking': 'Your food is being cooked with care.',
            'ready': 'Your order is ready for pickup/delivery.',
            'out_for_delivery': f'Your order is on the way! Driver: {order.driver_name}' if order.driver_name else 'Your order is out for delivery.',
            'delivered': 'Your order has been delivered. Enjoy your meal!',
            'cancelled': 'Your order has been cancelled.'
        }
        
        order_data['status_description'] = status_descriptions.get(order.status, 'Status unknown')
        
        return jsonify({'order': order_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch order', 'details': str(e)}), 500

@bp.route('/<order_id>/tracking', methods=['GET'])
@jwt_required()
def track_order(order_id):
    """Get detailed tracking information for an order"""
    try:
        user_id = get_jwt_identity()
        
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Generate tracking timeline
        timeline = []
        
        timeline.append({
            'status': 'received',
            'description': 'Order received',
            'timestamp': order.created_at.isoformat(),
            'completed': True
        })
        
        # Add other statuses based on current order status
        statuses = ['preparing', 'cooking', 'ready', 'out_for_delivery', 'delivered']
        current_index = statuses.index(order.status) if order.status in statuses else -1
        
        for i, status in enumerate(statuses):
            timeline.append({
                'status': status,
                'description': get_status_description(status),
                'timestamp': order.updated_at.isoformat() if i <= current_index else None,
                'completed': i <= current_index,
                'current': status == order.status
            })
        
        tracking_data = {
            'order_id': order.id,
            'current_status': order.status,
            'estimated_delivery': order.estimated_delivery.isoformat() if order.estimated_delivery else None,
            'timeline': timeline
        }
        
        # Add driver info if available
        if order.driver_name and order.status in ['out_for_delivery']:
            tracking_data['driver'] = {
                'name': order.driver_name,
                'phone': order.driver_phone
            }
        
        return jsonify({'tracking': tracking_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch tracking', 'details': str(e)}), 500

@bp.route('/lookup/<order_id>', methods=['GET'])
@jwt_required()
def lookup_order(order_id):
    """Lookup order by ID for chat queries"""
    try:
        user_id = get_jwt_identity()
        
        # Find order - user can only see their own orders
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': f'Order {order_id} not found or does not belong to you'}), 404
        
        # Parse items JSON
        try:
            items = json.loads(order.items)
        except:
            items = []
        
        order_data = order.to_dict()
        order_data['items'] = items
        
        # Add status description for chat-friendly response
        status_descriptions = {
            'received': 'Your order has been received and is being processed.',
            'preparing': 'Our kitchen is preparing your delicious meal.',
            'cooking': 'Your food is being cooked with care.',
            'ready': 'Your order is ready for pickup/delivery.',
            'out_for_delivery': f'Your order is on the way! Driver: {order.driver_name}' if order.driver_name else 'Your order is out for delivery.',
            'delivered': 'Your order has been delivered. Enjoy your meal!',
            'cancelled': 'Your order has been cancelled.'
        }
        
        order_data['status_description'] = status_descriptions.get(order.status, 'Status unknown')
        order_data['chat_friendly_summary'] = f"Order {order_id}: {len(items)} items, Total: ${order.total_amount:.2f}, Status: {order_data['status_description']}"
        
        return jsonify({'order': order_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to lookup order', 'details': str(e)}), 500

@bp.route('/', methods=['GET'])
@jwt_required()
def get_user_orders():
    """Get all orders for the current user"""
    try:
        user_id = get_jwt_identity()
        
        orders = Order.query.filter_by(user_id=user_id).order_by(
            Order.created_at.desc()
        ).all()
        
        orders_data = []
        for order in orders:
            try:
                items = json.loads(order.items)
            except:
                items = []
            
            order_data = order.to_dict()
            order_data['items'] = items
            orders_data.append(order_data)
        
        return jsonify({'orders': orders_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch orders', 'details': str(e)}), 500

@bp.route('/<order_id>/issues', methods=['POST'])
@jwt_required()
def report_issue(order_id):
    """Report an issue with an order"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('issue_type') or not data.get('description'):
            return jsonify({'error': 'Issue type and description are required'}), 400
        
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Here you would typically save the issue to a database table
        # For now, we'll just return a success response
        
        issue_data = {
            'order_id': order_id,
            'issue_type': data['issue_type'],
            'description': data['description'],
            'status': 'reported',
            'reported_at': 'now'  # In real implementation, use datetime.utcnow()
        }
        
        return jsonify({
            'message': 'Issue reported successfully. Our team will contact you shortly.',
            'issue': issue_data
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to report issue', 'details': str(e)}), 500

def get_status_description(status):
    """Helper function to get user-friendly status descriptions"""
    descriptions = {
        'preparing': 'Kitchen is preparing your order',
        'cooking': 'Your food is being cooked',
        'ready': 'Order is ready',
        'out_for_delivery': 'Out for delivery',
        'delivered': 'Delivered successfully'
    }
    return descriptions.get(status, status.replace('_', ' ').title())
