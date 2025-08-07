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
        
        - Order status inquiries and tracking
        - Menu questions and recommendations
        - Order placement assistance and order creation
        - Delivery information
        - General customer support
        
        🚨 CRITICAL MENU INFORMATION RULES:
        - ONLY provide menu information that is explicitly provided in the context/knowledge base
        - NEVER invent, assume, or make up menu items, prices, or descriptions
        - If a customer asks about items not in our menu, clearly state they are not available
        - If you don't have specific menu information in the context, say "Let me check our current menu for you" and ask them to contact us directly
        - DO NOT create fictional menu items like salads, desserts, or other items unless they are explicitly provided in the knowledge base
        
        IMPORTANT INSTRUCTIONS FOR ORDER ASSISTANCE:
        - When customers mention wanting specific food items, provide helpful information about those items ONLY if they exist in our menu
        - If customers express CLEAR interest in ordering items with specific quantities or multiple items (like "I want 2 burgers" or "I want a burger and fries"), suggest order creation
        - ONLY suggest the order creation feature when customers show STRONG ordering intent with specific items
        - Suggestion format: "Perfect! I see you're interested in those items. You can use the shopping cart button (🛒) in the top right corner of the chat to automatically create your order based on our conversation."
        - Don't suggest order creation for general menu questions or single item inquiries
        - Always be helpful with menu questions and provide detailed information about ingredients, prices, and options
        - Only suggest order creation when someone mentions multiple items or specific quantities with clear ordering intent, but try to be not repetitive or pushy
        
        ORDER TRACKING:
        - When customers ask about order status, always ask for their order ID (format: PB######)
        - They can also look up orders by typing commands like "check order PB123456" in the chat
        
        Always be polite, helpful, and focused on providing excellent customer service.
        If you don't know something specific about an order or menu item, ask for more details
        or suggest they contact customer service directly.
        
        Keep responses concise but informative. Use a warm, friendly tone that reflects 
        PerfBurger's commitment to quality and customer satisfaction.
        
        Remember: Your goal is not just to answer questions, but to help customers easily create orders 
        when they show interest in our food items. BUT NEVER INVENT MENU ITEMS THAT DON'T EXIST.
        """
    
    def _initialize_client(self):
        """Initialize OpenAI client if not already done"""
        if self.client is None:
            api_key = current_app.config.get('OPENAI_API_KEY')
            
            # Detailed logging for Azure debugging
            logging.info(f"LLM Client initialization - API key available: {bool(api_key)}")
            if api_key:
                logging.info(f"API key length: {len(api_key)} chars")
                logging.info(f"API key starts with: {api_key[:8]}...")
            
            if not api_key:
                logging.error("OpenAI API key not configured - check environment variables")
                raise ValueError("OpenAI API key not configured")
            
            try:
                self.client = OpenAI(api_key=api_key)
                logging.info("OpenAI client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize OpenAI client: {e}")
                raise
    
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
            logging.info(f"LLM generate_response called with message: {user_message[:50]}...")
            
            self._initialize_client()
            logging.info("LLM client initialized successfully")
            
            # Build the conversation context
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add retrieved context if available
            if context:
                context_text = self._format_context(context)
                context_message = f"Here's some relevant information that might help answer the user's question:\n\n{context_text}"
                messages.append({"role": "system", "content": context_message})
                logging.info(f"Added context: {len(context)} items")
            
            # Add chat history
            if chat_history:
                messages.extend(chat_history[-10:])  # Last 10 messages for context
                logging.info(f"Added chat history: {len(chat_history[-10:])} messages")
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            logging.info(f"Making OpenAI API call with {len(messages)} messages")
            
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
            logging.info(f"OpenAI API call successful, response length: {len(content) if content else 0} chars")
            return content.strip() if content else "I apologize, but I'm having trouble generating a response right now."
            
        except Exception as e:
            logging.error(f"LLM generation error: {str(e)}")
            logging.error(f"Error type: {type(e).__name__}")
            fallback = self._get_fallback_response(user_message)
            logging.info(f"Returning fallback response: {fallback[:50]}...")
            return fallback
    
    def _format_context(self, context):
        """Format retrieved context for the AI prompt"""
        if not context:
            return "⚠️  WARNING: No specific menu information was found for this query. Only provide information about items that exist in PerfBurger's actual menu. Do not invent or assume any menu items."
        
        formatted = ["🍔 PERFBURGER MENU INFORMATION (Only provide information from this data):"]
        for item in context:
            if isinstance(item, dict):
                if 'title' in item and 'content' in item:
                    formatted.append(f"**{item['title']}**\n{item['content']}")
                else:
                    formatted.append(str(item))
            else:
                formatted.append(str(item))
        
        formatted.append("\n⚠️  IMPORTANT: Only provide information about items listed above. If asked about items not shown here, clearly state they are not available in our menu.")
        
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

    def analyze_conversation_for_order(self, conversation_text, menu_data):
        """
        Analyze conversation text to extract order items using LLM
        
        Args:
            conversation_text (str): Combined user messages from chat
            menu_data (dict): Menu data for validation
            
        Returns:
            dict: Extracted order information or error
        """
        try:
            self._initialize_client()
            
            # Create a structured prompt for order extraction
            menu_items_text = self._format_menu_for_llm(menu_data)
            
            system_prompt = f"""You are an expert order analysis assistant for PerfBurger restaurant. 
            Your task is to analyze customer conversations and extract specific order items with high accuracy.
            
            AVAILABLE MENU ITEMS:
            {menu_items_text}
            
            ANALYSIS INSTRUCTIONS:
            1. Identify ONLY items that are explicitly mentioned and available in the menu above
            2. Extract exact quantities (default to 1 if not clearly specified)
            3. Identify customizations like "no onions", "extra cheese", "no tomato", "without X", "add X", etc.
            4. Use exact menu item names and prices as listed above
            5. Look for intent words like "want", "I'll have", "order", "get me", etc.
            6. Be conservative - only include items you're confident about
            7. If someone says "burger" but doesn't specify which one, don't assume - mark as unclear
            
            RESPONSE FORMAT (valid JSON only):
            {{
                "items": [
                    {{
                        "name": "exact menu item name from the list above",
                        "quantity": number,
                        "customizations": ["specific customizations mentioned"],
                        "price": exact_price_from_menu,
                        "category": "menu_category"
                    }}
                ],
                "confidence": 0.0-1.0,
                "reasoning": "brief explanation of what was detected and why",
                "unavailable_items": ["items mentioned but not available in menu"],
                "unclear_items": ["items mentioned but not clearly specified"]
            }}
            """
            
            user_prompt = f"""Analyze this customer conversation and extract order items:

            CUSTOMER CONVERSATION:
            "{conversation_text}"
            
            Focus on finding:
            - Specific menu items mentioned by exact name or clear description
            - Quantities (numbers like "2", "two", "a couple", etc.)
            - Customizations (no onions, extra cheese, medium rare, etc.)
            - Clear ordering intent (want, need, order, I'll take, etc.)
            - Items mentioned that are NOT available in the menu (mark as unavailable_items)
            
            Return only items you're confident the customer wants to order.
            IMPORTANT: If the customer mentions food items that are not in our menu, list them in "unavailable_items"."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.2,  # Very low temperature for consistent parsing
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            if content:
                import json
                try:
                    result = json.loads(content)
                    logging.info(f"LLM order analysis successful: {len(result.get('items', []))} items detected, confidence: {result.get('confidence', 0.0)}")
                    
                    # Validate the extracted items against the menu
                    validated_result = self._validate_extracted_items(result, menu_data)
                    return validated_result
                    
                except json.JSONDecodeError as e:
                    logging.error(f"JSON decode error in LLM response: {e}")
                    return {"items": [], "confidence": 0.0, "reasoning": "Failed to parse LLM response"}
            else:
                return {"items": [], "confidence": 0.0, "reasoning": "Empty LLM response"}
                
        except Exception as e:
            logging.error(f"LLM order analysis error: {str(e)}")
            return {"items": [], "confidence": 0.0, "reasoning": f"Error: {str(e)}"}

    def _validate_extracted_items(self, result, menu_data):
        """Validate extracted items against actual menu data"""
        if not result.get('items'):
            return result
        
        validated_items = []
        for item in result['items']:
            # Find the actual menu item
            found = False
            for category, menu_items in menu_data.items():
                if isinstance(menu_items, list):
                    for menu_item in menu_items:
                        if (isinstance(menu_item, dict) and 
                            menu_item.get('name', '').lower() == item.get('name', '').lower()):
                            
                            # Use actual menu data
                            validated_item = {
                                "name": menu_item['name'],  # Exact menu name
                                "quantity": max(1, int(item.get('quantity', 1))),  # Ensure positive
                                "customizations": item.get('customizations', []),
                                "price": float(menu_item['price']),  # Actual menu price
                                "category": category
                            }
                            validated_items.append(validated_item)
                            found = True
                            break
                if found:
                    break
            
            if not found:
                logging.warning(f"LLM extracted item '{item.get('name')}' not found in menu")
        
        result['items'] = validated_items
        if len(validated_items) < len(result.get('items', [])):
            result['confidence'] = max(0.0, result.get('confidence', 0.0) - 0.2)  # Reduce confidence
            result['reasoning'] += " (Some items were filtered out during validation)"
        
        return result
    
    def _format_menu_for_llm(self, menu_data):
        """Format menu data for LLM consumption"""
        menu_text = []
        
        for category, items in menu_data.items():
            if isinstance(items, list):
                menu_text.append(f"\n{category.upper()}:")
                for item in items:
                    if isinstance(item, dict) and 'name' in item and 'price' in item:
                        name = item['name']
                        price = item['price']
                        description = item.get('description', '')
                        menu_text.append(f"  - {name}: ${price}")
                        if description:
                            menu_text.append(f"    {description}")
        
        return "\n".join(menu_text)

    def should_suggest_order_creation(self, user_message):
        """
        Determine if the user message indicates interest in ordering
        
        Args:
            user_message (str): The user's message
            
        Returns:
            bool: True if order creation should be suggested
        """
        try:
            # Enhanced keyword detection
            order_intent_keywords = [
                'want', 'need', 'i\'ll take', 'i\'ll have', 'i want', 'i need',
                'order', 'buy', 'purchase', 'get me', 'give me', 'can i have',
                'i would like', 'i\'d like', 'looking for', 'interested in'
            ]
            
            food_keywords = [
                'burger', 'hamburger', 'fries', 'drink', 'beverage', 'combo', 
                'meal', 'food', 'classic', 'perfburger', 'bbq', 'bacon', 
                'veggie', 'spicy', 'jalapeño', 'cheese', 'deluxe', 'supreme',
                'shake', 'milkshake', 'soda', 'water', 'onion rings'
            ]
            
            quantity_indicators = [
                'two', 'three', 'four', 'five', 'couple', 'few', 'several',
                '1', '2', '3', '4', '5', '6', '7', '8', '9'
            ]
            
            customization_keywords = [
                'no onions', 'extra cheese', 'no tomato', 'medium rare', 'well done',
                'without', 'add', 'extra'
            ]
            
            message_lower = user_message.lower()
            
            # Check for different types of order signals
            has_order_intent = any(keyword in message_lower for keyword in order_intent_keywords)
            has_food_mention = any(keyword in message_lower for keyword in food_keywords)
            has_quantity = any(keyword in message_lower for keyword in quantity_indicators)
            has_customization = any(keyword in message_lower for keyword in customization_keywords)
            
            # More sophisticated scoring
            score = 0
            if has_order_intent and has_food_mention:
                score += 3  # Strong signal
            elif has_food_mention and has_quantity:
                score += 2  # Medium signal
            elif has_food_mention and has_customization:
                score += 2  # Medium signal  
            elif has_food_mention:
                score += 1  # Weak signal
            
            # Additional context checks
            if 'menu' in message_lower and 'want' in message_lower:
                score += 1
            
            # Threshold for suggestion
            return score >= 2
            
        except Exception as e:
            logging.error(f"Error in should_suggest_order_creation: {str(e)}")
            return False
