# test_backend.py - Updated version
try:
    import requests
except ImportError:
    print("❌ 'requests' module not installed. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

import json

def test_backend():
    BASE_URL = "http://localhost:8000"
    
    print("🧪 Testing FastAPI Backend...")
    print("="*50)
    
    try:
        # Test root endpoint
        print("1. Testing root endpoint...")
        response = requests.get(f"{BASE_URL}/")
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📝 Response: {response.json()}")
        
        # Test health endpoint
        print("\n2. Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"   ✅ Status: {response.status_code}")
        health_data = response.json()
        print(f"   💚 Health: {health_data}")
        
        # Test analytics
        print("\n3. Testing analytics endpoint...")
        response = requests.get(f"{BASE_URL}/analytics")
        if response.status_code == 200:
            analytics = response.json()
            print(f"   ✅ Analytics: {analytics['total_products']} total products")
            print(f"   📊 Price stats: {analytics['price_stats']}")
        else:
            print(f"   ❌ Analytics failed: {response.status_code}")
        
        # Test recommendations
        print("\n4. Testing recommendations endpoint...")
        test_data = {
            "query": "office chair",
            "n_recommendations": 2
        }
        response = requests.post(f"{BASE_URL}/recommend", json=test_data)
        if response.status_code == 200:
            recommendations = response.json()
            print(f"   ✅ Recommendations: Found {len(recommendations)} products")
            for i, rec in enumerate(recommendations):
                print(f"      {i+1}. {rec['title'][:50]}...")
                print(f"         AI Description: {rec['ai_description'][:60]}...")
                print(f"         Score: {rec['similarity_score']}")
        else:
            print(f"   ❌ Recommendations failed: {response.status_code} - {response.text}")
        
        print("\n🎉 ALL TESTS COMPLETED!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
        print("💡 Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_backend()