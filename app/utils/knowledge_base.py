import os
import json
import yaml
from typing import List, Dict, Any
from flask import current_app
import logging

class KnowledgeBase:
    """RAG knowledge base for retrieving relevant context"""
    
    def __init__(self):
        self.knowledge_data = None
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load knowledge base from files"""
        try:
            kb_path = current_app.config.get('KNOWLEDGE_BASE_PATH', 'knowledge_base/')
            
            # Load all knowledge base files
            self.knowledge_data = {
                'menu': self._load_file(os.path.join(kb_path, 'menu.json')),
                'faqs': self._load_file(os.path.join(kb_path, 'faqs.yaml')),
                'policies': self._load_file(os.path.join(kb_path, 'policies.json'))
            }
            
            logging.info("Knowledge base loaded successfully")
            
        except Exception as e:
            logging.error(f"Failed to load knowledge base: {str(e)}")
            self.knowledge_data = self._get_default_knowledge()
    
    def _load_file(self, filepath):
        """Load individual knowledge base file"""
        if not os.path.exists(filepath):
            logging.warning(f"Knowledge base file not found: {filepath}")
            return {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                if filepath.endswith('.json'):
                    return json.load(f)
                elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
                    return yaml.safe_load(f)
                else:
                    return {'content': f.read()}
        except Exception as e:
            logging.error(f"Failed to load {filepath}: {str(e)}")
            return {}
    
    def retrieve(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant knowledge base entries for a query
        
        Args:
            query (str): User's query
            max_results (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of relevant knowledge base entries
        """
        if not self.knowledge_data:
            return []
        
        try:
            query_lower = query.lower()
            relevant_items = []
            
            # Search menu items
            menu_items = self._search_menu(query_lower)
            relevant_items.extend(menu_items)
            
            # Search FAQs
            faq_items = self._search_faqs(query_lower)
            relevant_items.extend(faq_items)
            
            # Search policies
            policy_items = self._search_policies(query_lower)
            relevant_items.extend(policy_items)
            
            # Sort by relevance score and return top results
            relevant_items.sort(key=lambda x: x.get('score', 0), reverse=True)
            return relevant_items[:max_results]
            
        except Exception as e:
            logging.error(f"Knowledge retrieval error: {str(e)}")
            return []
    
    def _search_menu(self, query: str) -> List[Dict[str, Any]]:
        """Search menu items"""
        results = []
        menu_data = self.knowledge_data.get('menu', {})
        
        # Search burgers
        burgers = menu_data.get('burgers', [])
        for burger in burgers:
            score = self._calculate_relevance(query, burger)
            if score > 0:
                results.append({
                    'type': 'menu_item',
                    'category': 'burger',
                    'title': burger.get('name', 'Unknown Burger'),
                    'content': self._format_menu_item(burger),
                    'score': score
                })
        
        # Search sides and drinks
        for category in ['sides', 'drinks']:
            items = menu_data.get(category, [])
            for item in items:
                score = self._calculate_relevance(query, item)
                if score > 0:
                    results.append({
                        'type': 'menu_item',
                        'category': category,
                        'title': item.get('name', f'Unknown {category}'),
                        'content': self._format_menu_item(item),
                        'score': score
                    })
        
        return results
    
    def _search_faqs(self, query: str) -> List[Dict[str, Any]]:
        """Search FAQ entries"""
        results = []
        faqs = self.knowledge_data.get('faqs', {}).get('faqs', [])
        
        for faq in faqs:
            # Check both question and answer
            text_to_search = f"{faq.get('question', '')} {faq.get('answer', '')}"
            score = self._calculate_text_relevance(query, text_to_search.lower())
            
            if score > 0:
                results.append({
                    'type': 'faq',
                    'title': faq.get('question', 'FAQ'),
                    'content': faq.get('answer', ''),
                    'score': score
                })
        
        return results
    
    def _search_policies(self, query: str) -> List[Dict[str, Any]]:
        """Search policy documents"""
        results = []
        policies = self.knowledge_data.get('policies', {})
        
        for policy_key, policy_content in policies.items():
            if isinstance(policy_content, str):
                score = self._calculate_text_relevance(query, policy_content.lower())
                if score > 0:
                    results.append({
                        'type': 'policy',
                        'title': policy_key.replace('_', ' ').title(),
                        'content': policy_content,
                        'score': score
                    })
        
        return results
    
    def _calculate_relevance(self, query: str, item: Dict) -> float:
        """Calculate relevance score for a menu item"""
        score = 0.0
        
        # Check name
        name = item.get('name', '').lower()
        if query in name:
            score += 2.0
        
        # Check description
        description = item.get('description', '').lower()
        if query in description:
            score += 1.5
        
        # Check ingredients
        ingredients = item.get('ingredients', [])
        if isinstance(ingredients, list):
            for ingredient in ingredients:
                if query in ingredient.lower():
                    score += 1.0
        
        # Check categories/tags
        category = item.get('category', '').lower()
        if query in category:
            score += 1.0
        
        return score
    
    def _calculate_text_relevance(self, query: str, text: str) -> float:
        """Calculate relevance score for text content"""
        if not text or not query:
            return 0.0
        
        # Simple keyword matching - can be enhanced with more sophisticated methods
        query_words = query.split()
        score = 0.0
        
        for word in query_words:
            if len(word) > 2:  # Skip very short words
                if word in text:
                    score += 1.0
        
        return score / len(query_words) if query_words else 0.0
    
    def _format_menu_item(self, item: Dict) -> str:
        """Format menu item for display"""
        parts = []
        
        if 'name' in item:
            parts.append(f"**{item['name']}**")
        
        if 'price' in item:
            parts.append(f"Price: ${item['price']}")
        
        if 'description' in item:
            parts.append(f"Description: {item['description']}")
        
        if 'ingredients' in item and isinstance(item['ingredients'], list):
            parts.append(f"Ingredients: {', '.join(item['ingredients'])}")
        
        if 'nutritional_info' in item:
            nutrition = item['nutritional_info']
            parts.append(f"Calories: {nutrition.get('calories', 'N/A')}")
        
        return '\n'.join(parts)
    
    def _get_default_knowledge(self):
        """Provide default knowledge base when files are not available"""
        return {
            'menu': {
                'burgers': [
                    {
                        'name': 'Classic PerfBurger',
                        'price': '12.99',
                        'description': 'Our signature burger with premium beef patty, lettuce, tomato, onion, and our special sauce',
                        'ingredients': ['beef patty', 'lettuce', 'tomato', 'onion', 'special sauce', 'brioche bun']
                    }
                ]
            },
            'faqs': {
                'faqs': [
                    {
                        'question': 'What are your delivery hours?',
                        'answer': 'We deliver Monday through Sunday from 11 AM to 10 PM.'
                    },
                    {
                        'question': 'How long does delivery take?',
                        'answer': 'Typical delivery time is 25-35 minutes, depending on your location and current order volume.'
                    }
                ]
            },
            'policies': {
                'refund_policy': 'We offer full refunds for orders that are significantly delayed or incorrect.'
            }
        }
