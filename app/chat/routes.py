from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.chat import bp
from app import db
from app.models import User, ChatSession, ChatMessage
from app.utils.llm_client import LLMClient
from app.utils.knowledge_base import KnowledgeBase
import uuid
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
        
        if not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        session_id = data.get('session_id')
        
        # Get or create chat session
        if session_id:
            chat_session = ChatSession.query.filter_by(
                session_id=session_id, 
                user_id=user_id
            ).first()
        else:
            chat_session = None
        
        if not chat_session:
            # Create new session
            chat_session = ChatSession()
            chat_session.user_id = user_id
            chat_session.session_id = str(uuid.uuid4())
            db.session.add(chat_session)
            db.session.commit()
        
        # Save user message
        user_msg = ChatMessage()
        user_msg.session_id = chat_session.id
        user_msg.message_type = 'user'
        user_msg.content = user_message
        db.session.add(user_msg)
        
        # Retrieve relevant knowledge base content
        retrieved_context = knowledge_base.retrieve(user_message)
        
        # Generate AI response
        ai_response = llm_client.generate_response(
            user_message=user_message,
            context=retrieved_context,
            chat_history=get_chat_history(chat_session.id)
        )
        
        # Save AI response
        ai_msg = ChatMessage()
        ai_msg.session_id = chat_session.id
        ai_msg.message_type = 'assistant'
        ai_msg.content = ai_response
        ai_msg.retrieved_context = str(retrieved_context) if retrieved_context else None
        db.session.add(ai_msg)
        db.session.commit()
        
        return jsonify({
            'message': ai_response,
            'session_id': chat_session.session_id,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Chat failed', 'details': str(e)}), 500

@bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    """Get user's chat sessions"""
    try:
        user_id = get_jwt_identity()
        sessions = ChatSession.query.filter_by(user_id=user_id).order_by(
            ChatSession.updated_at.desc()
        ).all()
        
        sessions_data = []
        for session in sessions:
            last_message = session.messages.order_by(
                ChatMessage.timestamp.desc()
            ).first()
            
            sessions_data.append({
                'session_id': session.session_id,
                'created_at': session.created_at.isoformat(),
                'updated_at': session.updated_at.isoformat(),
                'is_active': session.is_active,
                'last_message': last_message.content[:100] + '...' if last_message and len(last_message.content) > 100 else last_message.content if last_message else None,
                'message_count': session.messages.count()
            })
        
        return jsonify({'sessions': sessions_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch sessions', 'details': str(e)}), 500

@bp.route('/sessions/<session_id>/messages', methods=['GET'])
@jwt_required()
def get_session_messages(session_id):
    """Get messages for a specific session"""
    try:
        user_id = get_jwt_identity()
        session = ChatSession.query.filter_by(
            session_id=session_id,
            user_id=user_id
        ).first()
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        messages = session.messages.order_by(ChatMessage.timestamp.asc()).all()
        messages_data = [msg.to_dict() for msg in messages]
        
        return jsonify({
            'session_id': session_id,
            'messages': messages_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch messages', 'details': str(e)}), 500

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
