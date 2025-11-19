"""
Comprehensive Chatbot Testing Script
Run this to test all chatbot features
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_chat(message, response, intent):
    """Print chat interaction"""
    print(f"\n👤 User: {message}")
    print(f"🤖 Bot: {response}")
    print(f"📊 Intent: {intent}")

def test_gemini_connection():
    """Test 1: Check if Gemini API is working"""
    print_section("TEST 1: Gemini API Connection")

    try:
        response = requests.get(f"{BASE_URL}/chat/test")
        data = response.json()

        if data['status'] == 'success':
            print("✅ Gemini API is connected!")
            print(f"Test response: {data['test_response'][:100]}...")
            return True
        else:
            print(f"❌ Gemini API error: {data.get('error')}")
            return False

    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def test_create_session():
    """Test 2: Create new chat session"""
    print_section("TEST 2: Create Chat Session")

    try:
        response = requests.post(f"{BASE_URL}/chat/session/new")
        data = response.json()
        session_id = data['session_id']

        print(f"✅ Session created: {session_id}")
        return session_id

    except Exception as e:
        print(f"❌ Session creation failed: {str(e)}")
        return None

def test_chat_conversation(session_id):
    """Test 3: Full conversation flow"""
    print_section("TEST 3: Chat Conversation")

    # Conversation test cases
    test_messages = [
        "Hi there!",
        "Show me your menu",
        "What pizzas do you have?",
        "Tell me about the Margherita Pizza",
        "What are your hours?",
        "Do you deliver?"
    ]

    for message in test_messages:
        try:
            payload = {
                "message": message,
                "session_id": session_id,
                "phone_number": "+1234567890"
            }

            response = requests.post(f"{BASE_URL}/chat", json=payload)
            data = response.json()

            print_chat(message, data['response'], data['intent'])
            time.sleep(1)  # Rate limiting

        except Exception as e:
            print(f"❌ Chat failed: {str(e)}")

def test_intent_detection(session_id):
    """Test 4: Intent Detection"""
    print_section("TEST 4: Intent Detection")

    intent_tests = {
        "Hi!": "greeting",
        "Show me the menu": "menu_query",
        "I want to order pizza": "order_intent",
        "Book a table for 4": "reservation_intent",
        "What time do you close?": "faq"
    }

    for message, expected_intent in intent_tests.items():
        try:
            payload = {
                "message": message,
                "session_id": f"{session_id}-intent",
                "phone_number": "+9876543210"
            }

            response = requests.post(f"{BASE_URL}/chat", json=payload)
            data = response.json()
            detected_intent = data['intent']

            match = "✅" if detected_intent == expected_intent else "⚠️"
            print(f"{match} Message: '{message}'")
            print(f"   Expected: {expected_intent}, Detected: {detected_intent}")

        except Exception as e:
            print(f"❌ Intent test failed: {str(e)}")

def test_chat_history(session_id):
    """Test 5: Chat History Retrieval"""
    print_section("TEST 5: Chat History")

    try:
        response = requests.get(f"{BASE_URL}/chat/history/{session_id}")
        history = response.json()

        print(f"✅ Retrieved {len(history)} messages from history")

        if history:
            print("\nFirst 3 messages:")
            for i, msg in enumerate(history[:3], 1):
                print(f"\n{i}. User: {msg['user_message'][:50]}...")
                print(f"   Bot: {msg['bot_response'][:50]}...")
                print(f"   Intent: {msg['intent']}")

    except Exception as e:
        print(f"❌ History retrieval failed: {str(e)}")

def test_menu_integration(session_id):
    """Test 6: Menu Items in Response"""
    print_section("TEST 6: Menu Integration")

    messages = [
        "Show me pizzas",
        "What desserts do you have?",
        "Any drinks?"
    ]

    for message in messages:
        try:
            payload = {
                "message": message,
                "session_id": f"{session_id}-menu",
                "phone_number": "+5555555555"
            }

            response = requests.post(f"{BASE_URL}/chat", json=payload)
            data = response.json()

            menu_items = data.get('data', {})
            if menu_items and 'menu_items' in menu_items:
                menu_items = menu_items.get('menu_items', [])
            else:
                menu_items = []

            print(f"\n📝 Query: {message}")
            print(f"✅ Found {len(menu_items)} relevant items")

            if menu_items:
                print("Items returned:")
                for item in menu_items[:3]:
                    print(f"  - {item['name']}: ${item['price']}")
            else:
                print("  ⚠️ No items returned (check menu query logic)")

        except Exception as e:
            print(f"❌ Menu integration test failed: {str(e)}")
            import traceback
            traceback.print_exc()

def test_error_handling():
    """Test 7: Error Handling"""
    print_section("TEST 7: Error Handling")

    # Test invalid session
    try:
        payload = {
            "message": "Test",
            "session_id": "",  # Empty session ID
            "phone_number": "+1111111111"
        }

        response = requests.post(f"{BASE_URL}/chat", json=payload)

        if response.status_code == 422:
            print("✅ Validation error handled correctly")
        else:
            print("⚠️ Unexpected response for invalid input")

    except Exception as e:
        print(f"Error test: {str(e)}")

def run_all_tests():
    """Run complete test suite"""
    print("\n" + "🧪 "*30)
    print("RESTAURANT CHATBOT - COMPREHENSIVE TEST SUITE")
    print("🧪 "*30)

    # Test 1: Gemini Connection
    if not test_gemini_connection():
        print("\n❌ Cannot proceed - Gemini API not working!")
        print("Check your GEMINI_API_KEY in .env file")
        return

    # Test 2: Create Session
    session_id = test_create_session()
    if not session_id:
        print("\n❌ Cannot proceed - Session creation failed!")
        return

    # Test 3: Conversation
    test_chat_conversation(session_id)

    # Test 4: Intent Detection
    test_intent_detection(session_id)

    # Test 5: Chat History
    test_chat_history(session_id)

    # Test 6: Menu Integration
    test_menu_integration(session_id)

    # Test 7: Error Handling
    test_error_handling()

    # Summary
    print("\n" + "="*60)
    print("✅ TEST SUITE COMPLETED!")
    print("="*60)
    print("\nNext steps:")
    print("1. Try the chatbot at: http://localhost:8000/docs")
    print("2. Test with different queries")
    print("3. Check chat logs in database:")
    print("   SELECT * FROM chat_logs ORDER BY timestamp DESC LIMIT 10;")
    print("\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite error: {str(e)}")
