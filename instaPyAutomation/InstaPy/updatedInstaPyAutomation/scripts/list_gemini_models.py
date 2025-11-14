"""
List available Gemini models
"""
import requests
from config import Config

api_key = Config.GEMINI_API_KEY

# List models endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Available models:")
        for model in result.get('models', []):
            name = model.get('name', '')
            display_name = model.get('displayName', '')
            methods = model.get('supportedGenerationMethods', [])
            
            if 'generateContent' in methods:
                print(f"\n📦 {name}")
                print(f"   Display Name: {display_name}")
                print(f"   Methods: {', '.join(methods)}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
