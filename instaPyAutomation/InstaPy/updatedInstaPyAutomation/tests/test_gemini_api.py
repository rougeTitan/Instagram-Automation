"""
Quick test to verify Gemini API key is working
"""
import requests
import base64
from config import Config

def test_gemini_api():
    """Test Gemini API with a simple text-only request"""
    
    api_key = Config.GEMINI_API_KEY
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in config")
        return False
    
    print(f"🔑 Testing API Key: {api_key[:20]}...")
    
    # Test with v1beta endpoint (for vision models)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [
                {
                    "text": "Say 'Hello, I am working!' in JSON format: {\"message\": \"your response\"}"
                }
            ]
        }]
    }
    
    try:
        print(f"📡 Testing endpoint: {url[:80]}...")
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ API IS WORKING!")
            print(f"📝 Response: {text[:100]}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"📝 Response: {response.text[:200]}")
            
            # Try v1 endpoint as fallback
            print(f"\n🔄 Trying v1 endpoint...")
            url_v1 = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            response_v1 = requests.post(url_v1, json=payload, timeout=10)
            print(f"📊 V1 Status Code: {response_v1.status_code}")
            
            if response_v1.status_code == 200:
                print(f"✅ V1 endpoint works! Update code to use v1")
                return True
            else:
                print(f"❌ V1 also failed: {response_v1.text[:200]}")
            
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("GEMINI API TEST")
    print("="*60)
    success = test_gemini_api()
    print("="*60)
    if success:
        print("✅ Gemini API is configured correctly!")
    else:
        print("❌ Gemini API is NOT working. Check:")
        print("   1. API key is valid")
        print("   2. API key has Generative Language API enabled")
        print("   3. Visit: https://aistudio.google.com/app/apikey")
