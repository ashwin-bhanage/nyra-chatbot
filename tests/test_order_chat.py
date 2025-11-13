"""
Test AI-Powered Order & Reservation through Chat
"""

import requests
import json
import uuid

BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_chat(user_msg, bot_response, intent, action=None):
    print(f"\n👤 USER: {user_msg}")
    print(f"🤖 BOT: {bot_response[:200]}...")
    print(f"📊 Intent: {intent}")
    if action:
        print(f"✨ Action: {action}")

def test_order_via_chat():
    """Test placing order through natural conversation"""
    print_section("TEST 1: Order Placement via Chat")

    session_id = str(uuid.uuid4())

    test_orders = [
        "I want to order 2 Margherita pizzas",
        "I'd like 1 Pepperoni Pizza and 2 Cokes",
        "Order 3 Chicken Wings and 1 Caesar Salad please"
    ]

    for order_msg in test_orders:
        try:
            payload = {
                "message": order_msg,
                "session_id": session_id,
                "phone_number": "+1111111111"
            }

            response = requests.post(f"{BASE_URL}/chat", json=payload)
            data = response.json()

            print_chat(
                order_msg,
                data['response'],
                data['intent'],
                data.get('action')
            )

            if data.get('order_id'):
                print(f"   ✅ Order ID: {data['order_id']}")

                # Verify order was created
                order_response = requests.get(f"{BASE_URL}/order/{data['order_id']}")
                order_data = order_response.json()
                print(f"   💰 Total: ${order_data['total_amount']}")
                print(f"   📦 Items: {len(order_data['items'])}")

            print()

        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_reservation_via_chat():
    """Test making reservation through natural conversation"""
    print_section("TEST 2: Reservation via Chat")

    session_id = str(uuid.uuid4())

    test_reservations = [
        "Book a table for 4 on November 20 at 7 PM",
        "I'd like to reserve a table for 2 on November 25 at 6:30 PM",
        "Table for 6 on December 1st at 8 PM please"
    ]

    for res_msg in test_reservations:
        try:
            payload = {
                "message": res_msg,
                "session_id": session_id,
                "phone_number": "+2222222222"
            }

            response = requests.post(f"{BASE_URL}/chat", json=payload)
            data = response.json()

            print_chat(
                res_msg,
                data['response'],
                data['intent'],
                data.get('action')
            )

            if data.get('reservation_id'):
                print(f"   ✅ Reservation ID: {data['reservation_id']}")

                # Verify reservation was created
                res_response = requests.get(f"{BASE_URL}/reservation/{data['reservation_id']}")
                res_data = res_response.json()
                print(f"   📅 Date: {res_data['reservation_date']}")
                print(f"   👥 Party: {res_data['party_size']} people")

            print()

        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_full_conversation_flow():
    """Test complete user journey"""
    print_section("TEST 3: Complete Conversation Flow")

    session_id = str(uuid.uuid4())
    phone = "+3333333333"

    conversation = [
        "Hi there!",
        "Show me your pizzas",
        "Tell me about the Margherita",
        "I want to order 2 Margherita pizzas",
        "What are your hours?",
        "Thanks!"
    ]

    for msg in conversation:
        try:
            payload = {
                "message": msg,
                "session_id": session_id,
                "phone_number": phone
            }

            response = requests.post(f"{BASE_URL}/chat", json=payload)
            data = response.json()

            print_chat(msg, data['response'], data['intent'], data.get('action'))

        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_order_summary():
    """Test order summary generation"""
    print_section("TEST 4: Order Summary")

    # First, create an order via API
    order_payload = {
        "phone_number": "+4444444444",
        "items": [
            {"menu_item_id": 4, "quantity": 2},
            {"menu_item_id": 5, "quantity": 1},
            {"menu_item_id": 12, "quantity": 3}
        ],
        "delivery_address": "123 Test Street",
        "special_instructions": "Ring bell twice"
    }

    try:
        # Create order
        response = requests.post(f"{BASE_URL}/order", json=order_payload)
        order_data = response.json()
        order_id = order_data['id']

        print(f"✅ Created Order #{order_id}")

        # Get summary
        summary_response = requests.get(f"{BASE_URL}/order/{order_id}/summary")
        summary_data = summary_response.json()

        print("\n📄 Order Summary:")
        print(summary_data['summary'])

    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_edge_cases():
    """Test edge cases and error handling"""
    print_section("TEST 5: Edge Cases")

    session_id = str(uuid.uuid4())

    edge_cases = [
        "I want to order something",  # Vague order
        "Book a table",  # Missing details
        "Order 100 pizzas",  # Large quantity
    ]

    for msg in edge_cases:
        try:
            payload = {
                "message": msg,
                "session_id": session_id,
                "phone_number": "+5555555555"
            }

            response = requests.post(f"{BASE_URL}/chat", json=payload)
            data = response.json()

            print_chat(msg, data['response'], data['intent'], data.get('action'))

        except Exception as e:
            print(f"❌ Error: {str(e)}")

def run_all_tests():
    """Run complete test suite"""
    print("\n" + "🧪 "*35)
    print("AI-POWERED ORDER & RESERVATION - TEST SUITE")
    print("🧪 "*35)

    try:
        test_order_via_chat()
        test_reservation_via_chat()
        test_full_conversation_flow()
        test_order_summary()
        test_edge_cases()

        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED!")
        print("="*70)

        print("\nVerify in database:")
        print("  SELECT * FROM orders ORDER BY id DESC;")
        print("  SELECT * FROM reservations ORDER BY id DESC;")
        print("  SELECT * FROM chat_logs ORDER BY timestamp DESC LIMIT 20;")

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("Make sure the server is running:")
        print("  uvicorn app.main:app --reload")

    except Exception as e:
        print(f"\n❌ TEST ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
