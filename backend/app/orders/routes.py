from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.orders import bp
from app import db
from app.models import Order, User, ChatSession, ChatMessage
from app.utils.llm_client import LLMClient
import json
import uuid
import random
import string
from datetime import datetime, timedelta
import os
import logging

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
    """Analyze chat messages to extract order items using LLM"""
    try:
        # Get the chat session
        session = ChatSession.query.filter_by(session_id=session_id, user_id=user_id).first()
        if not session:
            return {"error": "Chat session not found"}, 404
        
        # Get all messages from the session
        messages = ChatMessage.query.filter_by(session_id=session.id).order_by(ChatMessage.timestamp).all()
        
        # Combine all user messages for analysis
        conversation_text = " ".join([msg.content for msg in messages if msg.message_type == 'user'])
        
        if not conversation_text.strip():
            return {"error": "No user messages found in conversation"}, 400
        
        # Load menu for validation
        menu = load_menu()
        
        if not menu:
            return {"error": "Menu data not available"}, 500
        
        # Use LLM for intelligent order extraction
        llm_client = LLMClient()
        try:
            llm_result = llm_client.analyze_conversation_for_order(conversation_text, menu)
        except Exception as llm_error:
            logging.warning(f"LLM analysis failed: {str(llm_error)}, falling back to keyword matching")
            llm_result = {"items": [], "confidence": 0.0, "reasoning": f"LLM failed: {str(llm_error)}"}
        
        # Process LLM results
        detected_items = []
        total_amount = 0.0
        
        if llm_result.get('items'):
            for item in llm_result['items']:
                # Validate that the item exists in our menu and prices match
                item_found = False
                for category in ['burgers', 'sides', 'drinks', 'desserts']:
                    if category in menu:
                        for menu_item in menu[category]:
                            if menu_item['name'].lower() == item['name'].lower():
                                # Use actual menu price for security
                                actual_price = float(menu_item['price'])
                                quantity = max(1, int(item.get('quantity', 1)))  # Ensure positive quantity
                                
                                validated_item = {
                                    "name": menu_item['name'],  # Use exact menu name
                                    "price": actual_price,
                                    "quantity": quantity,
                                    "customizations": item.get('customizations', []),
                                    "category": category
                                }
                                
                                detected_items.append(validated_item)
                                total_amount += actual_price * quantity
                                item_found = True
                                break
                    if item_found:
                        break
        
        # Fallback to simple keyword matching if LLM fails or finds nothing
        if not detected_items:
            logging.info("LLM found no items, falling back to simple keyword matching")
            detected_items, total_amount = _simple_keyword_extraction(conversation_text, menu)
        
        if not detected_items:
            return {"error": "No menu items detected in conversation. Please mention specific items from our menu."}, 400
        
        return {
            "items": detected_items,
            "total_amount": round(total_amount, 2),
            "conversation_summary": conversation_text[:200] + "..." if len(conversation_text) > 200 else conversation_text,
            "analysis_method": "LLM" if llm_result.get('items') else "keyword_matching",
            "llm_confidence": llm_result.get('confidence', 0.0),
            "llm_reasoning": llm_result.get('reasoning', 'No LLM analysis available'),
            "unavailable_items": llm_result.get('unavailable_items', [])
        }, 200
        
    except Exception as e:
        logging.error(f"Error in analyze_chat_for_order: {str(e)}")
        return {"error": f"Failed to analyze chat: {str(e)}"}, 500

def _simple_keyword_extraction(conversation_text, menu):
    """Fallback simple keyword matching for order extraction"""
    detected_items = []
    total_amount = 0.0
    conversation_lower = conversation_text.lower()
    
    # Check each menu category for mentioned items
    for category in ['burgers', 'sides', 'drinks', 'desserts']:
        if category in menu:
            for item in menu[category]:
                item_name = item['name'].lower()
                
                # Simple keyword matching
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
    
    return detected_items, total_amount

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
        try:
            analysis_result, status_code = analyze_chat_for_order(session_id, user_id)
        except Exception as analysis_error:
            logging.error(f"Error in analyze_chat_for_order: {str(analysis_error)}")
            return jsonify({'error': 'Failed to analyze chat for order creation', 'details': str(analysis_error)}), 500
        
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
            delivery_address=None,  # Address not required per user feedback
            estimated_delivery=datetime.utcnow() + timedelta(minutes=30)  # 30 min estimate
        )
        
        db.session.add(order)
        db.session.commit()
        
        # Prepare response
        order_response = order.to_dict()
        order_response['items'] = analysis_result['items']
        order_response['conversation_summary'] = analysis_result['conversation_summary']
        
        # Include analysis metadata for better user feedback
        response_data = {
            'message': 'Order created successfully',
            'order': order_response,
            'analysis_method': analysis_result.get('analysis_method', 'unknown'),
            'llm_confidence': analysis_result.get('llm_confidence', 0.0),
            'unavailable_items': analysis_result.get('unavailable_items', []),
            'llm_reasoning': analysis_result.get('llm_reasoning', '')
        }
        
        return jsonify(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create order', 'details': str(e)}), 500

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
