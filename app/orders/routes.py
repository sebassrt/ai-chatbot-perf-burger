from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.orders import bp
from app import db
from app.models import Order, User
import json

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
