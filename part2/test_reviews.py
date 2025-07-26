#!/usr/bin/python3
"""
Script to test Review endpoints
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
        "last_name": "Reviewer",
        "email": f"reviewer{uuid.uuid4()}@example.com",
        "is_admin": False
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    
    if response.status_code != 201:
        print(f"Error creating test user: {response.text}")
        return None
    
    return response.json()['id']

def create_test_place(owner_id):
    """Create a test place and return its ID"""
    place_data = {
        "title": f"Test Place {uuid.uuid4()}",
        "description": "A place for testing reviews",
        "price": 100.0,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": owner_id,
        "amenities": []
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=place_data)
    
    if response.status_code != 201:
        print(f"Error creating test place: {response.text}")
        return None
    
    return response.json()['id']

def test_review_endpoints():
    """Test all Review endpoints"""
    print("\nPreparing test data...")
    
    user_id = create_test_user()
    if not user_id:
        print("Error: Failed to create test user.")
        return False
    print(f"Created test user with ID: {user_id}")
    
    place_id = create_test_place(user_id)
    if not place_id:
        print("Error: Failed to create test place.")
        return False
    print(f"Created test place with ID: {place_id}")
    
    print("\nStarting Review endpoint tests...")
    
    review_data = {
        "text": "This is a test review",
        "rating": 4,
        "user_id": user_id,
        "place_id": place_id
    }
    
    create_response = requests.post(
        f"{BASE_URL}/reviews/",
        json=review_data
    )
    
    print("\n1. Create Review Test:")
    print(f"Status Code: {create_response.status_code}")
    if create_response.status_code == 201:
        print(f"Response: {json.dumps(create_response.json(), indent=2)}")
        review_id = create_response.json()['id']
        print(f"Created review with ID: {review_id}")
    else:
        print(f"Error: {create_response.text}")
        return False
    
    list_response = requests.get(f"{BASE_URL}/reviews/")
    
    print("\n2. List Reviews Test:")
    print(f"Status Code: {list_response.status_code}")
    if list_response.status_code == 200:
        print(f"Response: {json.dumps(list_response.json(), indent=2)}")
    else:
        print(f"Error: {list_response.text}")
        return False
    
    get_response = requests.get(f"{BASE_URL}/reviews/{review_id}")
    
    print("\n3. Get Review Details Test:")
    print(f"Status Code: {get_response.status_code}")
    if get_response.status_code == 200:
        print(f"Response: {json.dumps(get_response.json(), indent=2)}")
    else:
        print(f"Error: {get_response.text}")
        return False
    
    place_reviews_response = requests.get(f"{BASE_URL}/reviews/places/{place_id}/reviews")
    
    print("\n4. Get Reviews by Place Test:")
    print(f"Status Code: {place_reviews_response.status_code}")
    if place_reviews_response.status_code == 200:
        print(f"Response: {json.dumps(place_reviews_response.json(), indent=2)}")
    else:
        print(f"Error: {place_reviews_response.text}")
        return False
    
    update_data = {
        "text": "Updated review text",
        "rating": 5
    }
    
    update_response = requests.put(
        f"{BASE_URL}/reviews/{review_id}",
        json=update_data
    )
    
    print("\n5. Update Review Test:")
    print(f"Status Code: {update_response.status_code}")
    if update_response.status_code == 200:
        print(f"Response: {json.dumps(update_response.json(), indent=2)}")
    else:
        print(f"Error: {update_response.text}")
        return False
    
    delete_response = requests.delete(f"{BASE_URL}/reviews/{review_id}")
    
    print("\n6. Delete Review Test:")
    print(f"Status Code: {delete_response.status_code}")
    if delete_response.status_code == 200:
        print(f"Response: {json.dumps(delete_response.json(), indent=2)}")
    else:
        print(f"Error: {delete_response.text}")
        return False
    
    verify_delete = requests.get(f"{BASE_URL}/reviews/{review_id}")
    if verify_delete.status_code == 404:
        print("Verified review was successfully deleted")
    else:
        print("Error: Review was not properly deleted")
        return False
    
    print("\nAll tests passed successfully!")
    return True

if __name__ == "__main__":
    print("Starting Review API tests...")
    
    try:
        requests.get(f"{BASE_URL}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure it's running.")
        sys.exit(1)
    
    success = test_review_endpoints()
    
    if not success:
        print("\nSome tests failed. Check the output above for details.")
        sys.exit(1)
