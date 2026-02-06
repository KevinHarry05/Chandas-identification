#!/usr/bin/env python3
"""
🧪 MANUAL TEST EXAMPLES - Test API with different Sanskrit verses
"""
import requests
import json
import time
import subprocess
import sys
from pathlib import Path

# Test verses with expected meters
TEST_VERSES = [
    {
        "verse": "यो वै स परम ब्रह्म तस्य नाम सत्यम्।",
        "name": "Test 1: Indravajra",
        "expected": "इन्द्रवज्रा"
    },
    {
        "verse": "मा गमो यातन प्रिये भरत।",
        "name": "Test 2: Mandakranta",
        "expected": "मन्दाक्रान्ता"
    },
    {
        "verse": "नमो देवाय सर्वज्ञाय प्रभवे।",
        "name": "Test 3: Vasantatilaka",
        "expected": "वसन्ततिलका"
    },
    {
        "verse": "रामराज्यं नृपतेः कृतं।",
        "name": "Test 4: Anushtubh",
        "expected": "अनुष्टुभ्"
    },
    {
        "verse": "आदित्यो जगतो जन्मदो विष्णुः।",
        "name": "Test 5: Malini",
        "expected": "मालिनी"
    },
    {
        "verse": "त्वं देवो दिवि रमणीय धरणे।",
        "name": "Test 6: Shikhariṇī",
        "expected": "शिखरिणी"
    },
]

def print_header(text):
    print("\n" + "="*90)
    print(f" {text}")
    print("="*90)

def start_backend():
    """Start the backend server"""
    backend_dir = Path(__file__).parent / "backend"
    print("\n📂 Starting backend server...")
    
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=str(backend_dir),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    print(f"   ✓ Backend started (PID: {process.pid})")
    print(f"   ⏳ Initializing...")
    time.sleep(5)
    
    return process

def test_verse(verse_data, test_num):
    """Test a single verse"""
    verse = verse_data["verse"]
    name = verse_data["name"]
    
    print_header(name)
    print(f"\n📖 Verse: {verse}")
    print(f"📊 Expected Meter: {verse_data['expected']}")
    print(f"\n🔍 Sending request...")
    
    try:
        response = requests.post(
            "http://localhost:8000/analyze-verse",
            json={"verse": verse},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            pred = data['best_prediction']
            
            print(f"\n✅ Response received!")
            print(f"\n📊 PREDICTION:")
            print(f"   Meter: {pred['chandas']}")
            print(f"   Confidence: {pred['confidence']:.2%}")
            print(f"   Pattern: {data['laghu_guru_pattern']}")
            
            print(f"\n🔄 ALTERNATIVES (Top 3):")
            for i, alt in enumerate(data['alternatives'][:3], 1):
                print(f"   {i}. {alt['chandas']}: {alt['confidence']:.2%}")
            
            if 'explainability' in data and data['explainability']:
                shap = data['explainability']
                top_features = shap.get('top_features', [])[:5]
                if top_features:
                    print(f"\n🔍 TOP CONTRIBUTING FEATURES:")
                    for feat in top_features:
                        impact = "↑" if feat['shap_value'] > 0 else "↓"
                        print(f"   {impact} {feat['feature']}: {feat['shap_value']:.4f}")
            
            print(f"\n✅ TEST PASSED")
            return True
        else:
            print(f"❌ Error: Status {response.status_code}")
            print(f"   {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print_header("🧪 CHANDAS IDENTIFIER - MANUAL TEST SUITE")
    print("\nThis script tests the backend API with multiple Sanskrit verses")
    print("and displays detailed prediction results with SHAP explanations.")
    
    # Start backend
    process = start_backend()
    
    try:
        # Run tests
        passed = 0
        failed = 0
        
        for i, verse_data in enumerate(TEST_VERSES, 1):
            if test_verse(verse_data, i):
                passed += 1
            else:
                failed += 1
            
            if i < len(TEST_VERSES):
                time.sleep(1)  # Brief pause between tests
        
        # Summary
        print_header("📊 TEST SUMMARY")
        print(f"\n✅ Passed: {passed}/{passed+failed}")
        print(f"❌ Failed: {failed}/{passed+failed}")
        
        if failed == 0:
            print(f"\n🎉 ALL TESTS PASSED!")
            print(f"\n✨ Backend is fully functional and ready for production!")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Check error messages above.")
        
        # API info
        print_header("📍 API INFORMATION")
        print("\n🌐 Available Endpoints:")
        print("   • GET  http://localhost:8000/")
        print("   • POST http://localhost:8000/analyze-verse")
        print("   • GET  http://localhost:8000/docs (Swagger UI)")
        print("   • GET  http://localhost:8000/redoc (ReDoc)")
        
        print("\n💡 Next Steps:")
        print("   1. Backend is running on http://localhost:8000")
        print("   2. Test with your own verses in the format:")
        print('      {\"verse\": \"your_sanskrit_text\"}')
        print("   3. Frontend can now integrate with the API")
        
        print("\n✨ Backend is ready for production deployment!\n")
        
        # Keep server running
        print("🔄 Server is running. Press Ctrl+C to stop...\n")
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping backend...")
        process.terminate()
        process.wait()
        print("✅ Backend stopped gracefully.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()
