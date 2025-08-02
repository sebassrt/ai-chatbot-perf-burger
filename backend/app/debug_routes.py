from flask import Blueprint, jsonify, current_app
import os
import logging

# Create a debug blueprint
debug_bp = Blueprint('debug', __name__)

@debug_bp.route('/debug/llm-status', methods=['GET'])
def llm_status():
    """Debug endpoint to check LLM configuration and status"""
    try:
        status = {
            'timestamp': os.popen('date').read().strip(),
            'environment': {},
            'openai_config': {},
            'llm_test': {}
        }
        
        # Check environment variables
        status['environment'] = {
            'OPENAI_API_KEY_set': bool(os.environ.get('OPENAI_API_KEY')),
            'OPENAI_API_KEY_length': len(os.environ.get('OPENAI_API_KEY', '')),
            'WEBSITE_HOSTNAME': os.environ.get('WEBSITE_HOSTNAME'),
            'is_azure': bool(os.environ.get('WEBSITE_HOSTNAME'))
        }
        
        # Check Flask app config
        api_key = current_app.config.get('OPENAI_API_KEY')
        status['openai_config'] = {
            'config_api_key_set': bool(api_key),
            'config_api_key_length': len(api_key) if api_key else 0,
            'config_api_key_prefix': api_key[:8] + '...' if api_key and len(api_key) > 8 else api_key
        }
        
        # Test OpenAI client initialization
        try:
            from openai import OpenAI
            
            if api_key:
                client = OpenAI(api_key=api_key)
                
                # Test simple API call
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Reply with 'LLM test successful!'"}],
                    max_tokens=20
                )
                
                status['llm_test'] = {
                    'client_init': True,
                    'api_call': True,
                    'response': response.choices[0].message.content,
                    'error': None
                }
            else:
                status['llm_test'] = {
                    'client_init': False,
                    'api_call': False,
                    'response': None,
                    'error': 'No API key available'
                }
                
        except Exception as e:
            status['llm_test'] = {
                'client_init': False,
                'api_call': False,
                'response': None,
                'error': str(e)
            }
        
        return jsonify(status), 200
        
    except Exception as e:
        logging.error(f"Debug LLM status endpoint error: {e}")
        return jsonify({
            'error': 'Debug endpoint failed',
            'details': str(e)
        }), 500

@debug_bp.route('/debug/environment', methods=['GET'])
def environment_info():
    """Debug endpoint to check environment variables"""
    try:
        # Safe environment variables to show (no secrets)
        safe_env_vars = [
            'WEBSITE_HOSTNAME',
            'WEBSITE_SITE_NAME', 
            'PYTHONPATH',
            'HOME',
            'WEBSITE_SKU',
            'WEBSITE_RESOURCE_GROUP'
        ]
        
        env_info = {}
        for var in safe_env_vars:
            env_info[var] = os.environ.get(var, 'Not set')
        
        # Add OpenAI key status (without revealing the key)
        openai_key = os.environ.get('OPENAI_API_KEY')
        env_info['OPENAI_API_KEY_status'] = {
            'set': bool(openai_key),
            'length': len(openai_key) if openai_key else 0,
            'starts_with': openai_key[:8] + '...' if openai_key and len(openai_key) > 8 else None
        }
        
        return jsonify({
            'environment_variables': env_info,
            'is_azure': bool(os.environ.get('WEBSITE_HOSTNAME')),
            'python_version': os.popen('python --version').read().strip()
        }), 200
        
    except Exception as e:
        logging.error(f"Debug environment endpoint error: {e}")
        return jsonify({
            'error': 'Debug environment endpoint failed',
            'details': str(e)
        }), 500
