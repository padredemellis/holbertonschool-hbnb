#!/usr/bin/python3
"""
Script to test Places endpoints
"""
import requests
import json
import sys
import uuid

BASE_URL = "http://localhost:5000/api/v1"

def create_test_user():
    """Create a test user and return its ID"""
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": f"test{uuid.uuid4()}@example.com",
        "is_admin": False
    }
    
    # Nota la barra al final de la URL
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    
    if response.status_code != 201:
        print(f"Error creating test user: {response.text}")
        return None
    
    return response.json()['id']

def create_test_amenity():
    """Create a test amenity and return its ID"""
    amenity_data = {
        "name": f"Test Amenity {uuid.uuid4()}"
    }
    
    # Nota la barra al final de la URL
    response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data)
    
    if response.status_code != 201:
        print(f"Error creating test amenity: {response.text}")
        return None
    
    return response.json()['id']

def test_places_endpoints():
    """Test all Place endpoints"""
    print("\nPreparing test data...")
    
    owner_id = create_test_user()
    if not owner_id:
        print("Error: Failed to create test user.")
        return False
    print(f"Created test user with ID: {owner_id}")
    
    amenity_ids = []
    for _ in range(2):
        amenity_id = create_test_amenity()
        if amenity_id:
            amenity_ids.append(amenity_id)
            print(f"Created test amenity with ID: {amenity_id}")
    
    print("\nStarting Places endpoint tests...")
    
    new_place_data = {
        "title": "Test Place",
        "description": "A place for testing",
        "price": 100.0,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": owner_id,
        "amenities": amenity_ids
    }
    
    # Nota la barra al final de la URL
    create_response = requests.post(
        f"{BASE_URL}/places/",
        json=new_place_data
    )
    
    print("\n1. Create Place Test:")
    print(f"Status Code: {create_response.status_code}")
    if create_response.status_code == 201:
        print(f"Response: {json.dumps(create_response.json(), indent=2)}")
        place_id = create_response.json()['id']
        print(f"Created place with ID: {place_id}")
    else:
        print(f"Error: {create_response.text}")
        return False
    
    # Nota la barra al final de la URL
    list_response = requests.get(f"{BASE_URL}/places/")
    
    print("\n2. List Places Test:")
    print(f"Status Code: {list_response.status_code}")
    if list_response.status_code == 200:
        print(f"Response: {json.dumps(list_response.json(), indent=2)}")
    else:
        print(f"Error: {list_response.text}")
        return False
    
    get_response = requests.get(f"{BASE_URL}/places/{place_id}")
    
    print("\n3. Get Place Details Test:")
    print(f"Status Code: {get_response.status_code}")
    if get_response.status_code == 200:
        print(f"Response: {json.dumps(get_response.json(), indent=2)}")
    else:
        print(f"Error: {get_response.text}")
        return False
    
    update_data = {
        "title": "Updated Test Place",
        "price": 150.0
    }
    
    update_response = requests.put(
        f"{BASE_URL}/places/{place_id}",
        json=update_data
    )
    
    print("\n4. Update Place Test:")
    print(f"Status Code: {update_response.status_code}")
    if update_response.status_code == 200:
        print(f"Response: {json.dumps(update_response.json(), indent=2)}")
    else:
        print(f"Error: {update_response.text}")
        return False
    
    print("\nAll tests passed successfully!")
    return True

if __name__ == "__main__":
    print("Starting Places API tests...")
    
    try:
        requests.get(f"{BASE_URL}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure it's running.")
        sys.exit(1)
    
    success = test_places_endpoints()
    
    if not success:
        print("\nSome tests failed. Check the output above for details.")
        sys.exit(1)
