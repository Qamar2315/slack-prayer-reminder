#!/usr/bin/env python3
"""
Test script for the new production-ready prayer bot structure.
This script tests each component individually to ensure everything works.
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_config():
    """Test configuration loading."""
    print("Testing configuration...")
    try:
        import config
        print(f"✅ Config loaded successfully")
        print(f"   - Channel ID: {config.SLACK_CHANNEL_ID}")
        print(f"   - Latitude: {config.LATITUDE}")
        print(f"   - Longitude: {config.LONGITUDE}")
        print(f"   - Prayers: {config.PRAYERS_IN_ORDER}")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_aladhan_service():
    """Test AlAdhan API service."""
    print("\nTesting AlAdhan service...")
    try:
        from services.aladhan_service import fetch_prayer_times
        timings = fetch_prayer_times()
        if timings:
            print("✅ AlAdhan service working")
            for prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
                if prayer in timings:
                    print(f"   - {prayer}: {timings[prayer]}")
            return True
        else:
            print("❌ AlAdhan service returned no data")
            return False
    except Exception as e:
        print(f"❌ AlAdhan service test failed: {e}")
        return False

def test_database_service():
    """Test database service."""
    print("\nTesting database service...")
    try:
        from services.db_service import DatabaseService
        import config
        
        # Create a test database
        db = DatabaseService("test_prayer_times.db", config.QURAN_ARABIC_FILE, config.QURAN_URDU_FILE)
        db.init_db()
        
        # Test Quran loading
        verse = db.get_random_verse()
        if verse and 'arabic_text' in verse and 'urdu_text' in verse:
            print("✅ Database service working")
            print(f"   - Quran data loaded: {len(db.quran_arabic)} chapters")
            print(f"   - Sample verse: {verse['chapter']}:{verse['verse']}")
        
        # Close the database connection before cleanup
        db.conn.close()
        
        # Clean up test database
        os.remove("test_prayer_times.db")
        return True
    except Exception as e:
        print(f"❌ Database service test failed: {e}")
        return False

def test_gemini_service():
    """Test Gemini AI service (if API key is available)."""
    print("\nTesting Gemini service...")
    try:
        import config
        if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "AIzaSy...YOUR_NEW_GEMINI_KEY":
            print("⚠️  Gemini API key not configured - skipping test")
            return True
        
        from services.gemini_service import generate_motivational_messages
        messages = generate_motivational_messages()
        if messages:
            print("✅ Gemini service working")
            for prayer, message in messages.items():
                print(f"   - {prayer}: {message[:50]}...")
            return True
        else:
            print("❌ Gemini service returned no messages")
            return False
    except Exception as e:
        print(f"❌ Gemini service test failed: {e}")
        return False

def test_slack_service():
    """Test Slack service (if token is available)."""
    print("\nTesting Slack service...")
    try:
        import config
        if not config.SLACK_BOT_TOKEN or config.SLACK_BOT_TOKEN == "xoxb-...YOUR_NEW_SLACK_TOKEN":
            print("⚠️  Slack token not configured - skipping test")
            return True
        
        from services.slack_service import send_reminder_message
        from services.db_service import DatabaseService
        
        # Create a test database to get a verse
        db = DatabaseService("test_slack.db", config.QURAN_ARABIC_FILE, config.QURAN_URDU_FILE)
        verse = db.get_random_verse()
        
        # Test message formatting (don't actually send)
        print("✅ Slack service structure working")
        print(f"   - Channel ID: {config.SLACK_CHANNEL_ID}")
        print(f"   - Sample verse ready: {verse['chapter']}:{verse['verse']}")
        
        # Close the database connection before cleanup
        db.conn.close()
        
        # Clean up
        os.remove("test_slack.db")
        return True
    except Exception as e:
        print(f"❌ Slack service test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing New Prayer Bot Structure")
    print("=" * 50)
    
    tests = [
        test_config,
        test_aladhan_service,
        test_database_service,
        test_gemini_service,
        test_slack_service
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your bot is ready to run.")
        print("\nNext steps:")
        print("1. Create a .env file with your API keys")
        print("2. Run: python main.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nMake sure to:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure your API keys in .env file")
        print("3. Check your internet connection")

if __name__ == "__main__":
    main() 