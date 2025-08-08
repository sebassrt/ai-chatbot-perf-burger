import pytest
from unittest.mock import patch, MagicMock
from app.utils.llm_client import LLMClient
from app.utils.knowledge_base import KnowledgeBase

class TestChat:
    """Test chat functionality with mocked LLM"""
    
    @pytest.fixture
    def mock_llm(self):
        """Mock LLM responses"""
        with patch('app.utils.llm_client.LLMClient') as mock:
            mock_instance = MagicMock()
            mock.return_value = mock_instance
            mock_instance.generate_response.return_value = {
                'response': 'I can help you with your order.',
                'context_used': True
            }
            yield mock_instance

    def test_chat_endpoint_success(self, client, auth_headers, mock_llm):
        """Test successful chat interaction"""
        response = client.post('/chat', 
            headers=auth_headers,
            json={'message': 'What are your burger options?'})
        
        assert response.status_code == 200
        data = response.json
        assert 'response' in data
        assert 'context_used' in data
        mock_llm.generate_response.assert_called_once()

    def test_chat_unauthorized(self, client):
        """Test chat without authentication"""
        response = client.post('/chat', 
            json={'message': 'Hello'})
        
        assert response.status_code == 401

    def test_chat_invalid_request(self, client, auth_headers):
        """Test chat with invalid request format"""
        response = client.post('/chat', 
            headers=auth_headers,
            json={})
        
        assert response.status_code == 400
        assert 'error' in response.json

    def test_context_retrieval(self, client, auth_headers):
        """Test knowledge base context retrieval"""
        with patch('app.utils.knowledge_base.KnowledgeBase') as mock_kb:
            mock_kb_instance = MagicMock()
            mock_kb.return_value = mock_kb_instance
            mock_kb_instance.get_relevant_context.return_value = [
                {'source': 'menu', 'content': 'Classic burger details'}
            ]

            response = client.post('/chat',
                headers=auth_headers,
                json={'message': 'Tell me about the classic burger'})
            
            assert response.status_code == 200
            mock_kb_instance.get_relevant_context.assert_called_once()

    @pytest.mark.parametrize('query,expected_sources', [
        ('menu prices', ['menu']),
        ('opening hours', ['policies']),
        ('delivery areas', ['policies']),
        ('ingredients', ['menu']),
    ])
    def test_knowledge_base_retrieval(self, query, expected_sources):
        """Test knowledge base retrieval for different query types"""
        kb = KnowledgeBase()
        context = kb.get_relevant_context(query)
        
        assert any(doc['source'] in expected_sources for doc in context)
