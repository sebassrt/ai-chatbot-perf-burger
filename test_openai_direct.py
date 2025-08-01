"""
Simple OpenAI API test script to verify the API key is working
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_openai_api():
    api_key = os.getenv('OPENAI_API_KEY')
    
    print("=== OpenAI API Direct Test ===")
    print(f"API Key present: {'Yes' if api_key else 'No'}")
    
    if not api_key:
        print("❌ No OpenAI API key found in environment")
        return
    
    print(f"API Key length: {len(api_key)} characters")
    print(f"API Key starts with: {api_key[:10]}...")
    
    try:
        # Initialize client
        client = OpenAI(api_key=api_key)
        
        # Test simple completion
        print("\nTesting OpenAI API call...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello and confirm you're working."}
            ],
            max_tokens=50
        )
        
        print("✅ OpenAI API call successful!")
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ OpenAI API call failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    test_openai_api()
