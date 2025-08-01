from openai import OpenAI
from flask import current_app
import logging

class LLMClient:
    """Client for interacting with OpenAI's language models"""
    
    def __init__(self):
        self.client = None
        self.system_prompt = """
        You are PerfBot, a friendly and professional customer service assistant for PerfBurger, 
        a premium burger delivery service. Your role is to help customers with:
        
        - Order status inquiries
        - Menu questions and recommendations
        - Delivery information
        - General customer support
        
        Always be polite, helpful, and focused on providing excellent customer service.
        If you don't know something specific about an order or menu item, ask for more details
        or suggest they contact customer service directly.
        
        Keep responses concise but informative. Use a warm, friendly tone that reflects 
        PerfBurger's commitment to quality and customer satisfaction.
        """
    
    def _initialize_client(self):
        """Initialize OpenAI client if not already done"""
        if self.client is None:
            api_key = current_app.config.get('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key not configured")
            
            self.client = OpenAI(api_key=api_key)
    
    def generate_response(self, user_message, context=None, chat_history=None):
        """
        Generate AI response to user message
        
        Args:
            user_message (str): The user's message
            context (list): Retrieved knowledge base context
            chat_history (list): Previous messages in the conversation
            
        Returns:
            str: AI-generated response
        """
        try:
            self._initialize_client()
            
            # Build the conversation context
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add retrieved context if available
            if context:
                context_text = self._format_context(context)
                context_message = f"Here's some relevant information that might help answer the user's question:\n\n{context_text}"
                messages.append({"role": "system", "content": context_message})
            
            # Add chat history
            if chat_history:
                messages.extend(chat_history[-10:])  # Last 10 messages for context
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else "I apologize, but I'm having trouble generating a response right now."
            
        except Exception as e:
            logging.error(f"LLM generation error: {str(e)}")
            return self._get_fallback_response(user_message)
    
    def _format_context(self, context):
        """Format retrieved context for the AI prompt"""
        if not context:
            return ""
        
        formatted = []
        for item in context:
            if isinstance(item, dict):
                if 'title' in item and 'content' in item:
                    formatted.append(f"**{item['title']}**\n{item['content']}")
                else:
                    formatted.append(str(item))
            else:
                formatted.append(str(item))
        
        return "\n\n".join(formatted)
    
    def _get_fallback_response(self, user_message):
        """Provide fallback response when AI is unavailable"""
        fallback_responses = {
            'order': "I'd be happy to help you with your order! Could you please provide your order ID so I can look up the details for you?",
            'menu': "I'd love to help you with our menu! We have a variety of delicious burgers, sides, and beverages. What specific information are you looking for?",
            'delivery': "For delivery information, I'll need a bit more details. Are you asking about delivery times, tracking an existing order, or our delivery areas?",
            'default': "Thank you for contacting PerfBurger! I'm here to help you with any questions about your orders, our menu, or delivery. How can I assist you today?"
        }
        
        # Simple keyword matching for fallback
        message_lower = user_message.lower()
        if any(word in message_lower for word in ['order', 'status', 'track']):
            return fallback_responses['order']
        elif any(word in message_lower for word in ['menu', 'burger', 'food', 'eat']):
            return fallback_responses['menu']
        elif any(word in message_lower for word in ['delivery', 'deliver', 'time']):
            return fallback_responses['delivery']
        else:
            return fallback_responses['default']
