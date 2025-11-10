"""
Quick API test script
Run this while your FastAPI server is running
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*50)
    print("TEST 1: Health Check")
    print("="*50)

    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ Health check passed!")


def test_get_all_menu():
    """Test get all menu items"""
    print("\n" + "="*50)
    print("TEST 2: Get All Menu Items")
    print("="*50)

    response = requests.get(f"{BASE_URL}/api/v1/menu")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Total items: {data['total']}")
    print(f"First item: {data['items'][0]['name']} - ${data['items'][0]['price']}")
    assert response.status_code == 200
    assert data['total'] == 14
    print("✅ Get all menu passed!")


def test_get_by_category():
    """Test get menu by category"""
    print("\n" + "="*50)
    print("TEST 3: Get Menu by Category (Main)")
    print("="*50)

    response = requests.get(f"{BASE_URL}/api/v1/menu/category/main")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Total main items: {data['total']}")
    for item in data['items']:
        print(f"  - {item['name']}: ${item['price']}")
    assert response.status_code == 200
    print("✅ Get by category passed!")


def test_search_menu():
    """Test search menu"""
    print("\n" + "="*50)
    print("TEST 4: Search Menu (pizza)")
    print("="*50)

    response = requests.get(f"{BASE_URL}/api/v1/menu/search/pizza")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Found {data['total']} items:")
    for item in data['items']:
        print(f"  - {item['name']}: ${item['price']}")
    assert response.status_code == 200
    print("✅ Search passed!")


def test_get_single_item():
    """Test get single menu item"""
    print("\n" + "="*50)
    print("TEST 5: Get Single Item (ID: 4)")
    print("="*50)

    response = requests.get(f"{BASE_URL}/api/v1/menu/4")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Item: {data['name']}")
    print(f"Description: {data['description']}")
    print(f"Price: ${data['price']}")
    assert response.status_code == 200
    print("✅ Get single item passed!")


def test_invalid_category():
    """Test invalid category"""
    print("\n" + "="*50)
    print("TEST 6: Invalid Category (should fail)")
    print("="*50)

    response = requests.get(f"{BASE_URL}/api/v1/menu/category/invalid")
    print(f"Status Code: {response.status_code}")
    print(f"Error: {response.json()['detail']}")
    assert response.status_code == 400
    print("✅ Error handling passed!")


def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪 "*25)
    print("STARTING API TESTS")
    print("🧪 "*25)

    try:
        test_health()
        test_get_all_menu()
        test_get_by_category()
        test_search_menu()
        test_get_single_item()
        test_invalid_category()

        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("Make sure the server is running:")
        print("  uvicorn app.main:app --reload")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")

    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")


if __name__ == "__main__":
    run_all_tests()
