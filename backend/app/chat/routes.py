from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.chat import bp
from app import db
from app.models import User, ChatSession, ChatMessage
from app.utils.llm_client import LLMClient
from app.utils.knowledge_base import KnowledgeBase
import uuid
import logging
from datetime import datetime

llm_client = LLMClient()
knowledge_base = KnowledgeBase()

@bp.route('/', methods=['POST'])
@jwt_required()
def chat():
    """Main chat endpoint - handles user messages and returns AI responses"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        logging.info(f"Chat endpoint called by user {user_id}")
        
        if not data.get('message'):
            logging.warning("Chat request missing message")
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        session_id = data.get('session_id')
        
        logging.info(f"User message: {user_message[:50]}...")
        
        # Get or create chat session
        if session_id:
            chat_session = ChatSession.query.filter_by(
                session_id=session_id, 
                user_id=user_id
            ).first()
            logging.info(f"Found existing session: {session_id}")
        else:
            chat_session = None
            logging.info("No session ID provided")
        
        if not chat_session:
            # Create new session
            chat_session = ChatSession()
            chat_session.user_id = user_id
            chat_session.session_id = str(uuid.uuid4())
            db.session.add(chat_session)
            db.session.commit()
            logging.info(f"Created new session: {chat_session.session_id}")
        
        # Save user message
        user_msg = ChatMessage()
        user_msg.session_id = chat_session.id
        user_msg.message_type = 'user'
        user_msg.content = user_message
        db.session.add(user_msg)
        
        # Retrieve relevant knowledge base content
        logging.info("Retrieving knowledge base context...")
        retrieved_context = knowledge_base.retrieve(user_message)
        logging.info(f"Retrieved {len(retrieved_context) if retrieved_context else 0} knowledge base items")
        
        # Generate AI response
        logging.info("Calling LLM client to generate response...")
        ai_response = llm_client.generate_response(
            user_message=user_message,
            context=retrieved_context,
            chat_history=get_chat_history(chat_session.id)
        )
        logging.info(f"LLM response generated: {ai_response[:50]}...")
        
        # Check if we should suggest order creation (only for authenticated users)
        # NOTE: Disabled automatic suggestions since LLM already handles this intelligently
        # should_suggest = llm_client.should_suggest_order_creation(user_message)
        # user_id = get_jwt_identity() if hasattr(get_jwt_identity, '__call__') else None
        
        # if should_suggest and user_id:
        #     logging.info("LLM detected order intent, adding suggestion to response")
        #     ai_response += "\n\n🛒 **Would you like to create an order?**\n\nI see that you mentioned some products from our menu. I can analyze our conversation and create an order for you. Just click the shopping cart button (🛒) in the top right corner of the chat."
        
        # Save AI response
        ai_msg = ChatMessage()
        ai_msg.session_id = chat_session.id
        ai_msg.message_type = 'assistant'
        ai_msg.content = ai_response
        ai_msg.retrieved_context = str(retrieved_context) if retrieved_context else None
        db.session.add(ai_msg)
        db.session.commit()
        
        logging.info("Chat response completed successfully")
        
        return jsonify({
            'message': ai_response,
            'session_id': chat_session.session_id,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Chat endpoint error: {str(e)}")
        logging.error(f"Error type: {type(e).__name__}")
        return jsonify({'error': 'Chat failed', 'details': str(e)}), 500

def get_chat_history(session_id, limit=10):
    """Helper function to get recent chat history for context"""
    messages = ChatMessage.query.filter_by(session_id=session_id).order_by(
        ChatMessage.timestamp.desc()
    ).limit(limit).all()
    
    history = []
    for msg in reversed(messages):
        history.append({
            'role': 'user' if msg.message_type == 'user' else 'assistant',
            'content': msg.content
        })
    
    return history
