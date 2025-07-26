#!/usr/bin/python3
"""
Test script for Amenity API endpoints
"""
import requests
import json
import sys
import time

BASE_URL = "http://localhost:5000/api/v1"

def print_response(response):
    """Print the response in a formatted way"""
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    print("Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except json.JSONDecodeError:
        print(response.text)
    print("-" * 80)

def test_api_root():
    """Test the API root endpoint"""
    print("\n=== Testing API Root ===")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    return response.status_code == 200

def test_create_amenity():
    """Test creating an amenity"""
    print("\n=== Testing Create Amenity ===")

    amenity_data = {
        "name": "WiFi",
        "description": "High-speed wireless internet"
    }

    response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data)

    print_response(response)

    if response.status_code == 201:
        return response.json().get("id")
    return None

def test_get_all_amenities():
    """Test getting all amenities"""
    print("\n=== Testing Get All Amenities ===")

    response = requests.get(f"{BASE_URL}/amenities/")

    print_response(response)
    return response.status_code == 200

def test_get_amenity_by_id(amenity_id):
    """Test getting an amenity by ID"""
    print(f"\n=== Testing Get Amenity by ID: {amenity_id} ===")

    response = requests.get(f"{BASE_URL}/amenities/{amenity_id}")

    print_response(response)
    return response.status_code == 200

def test_update_amenity(amenity_id):
    """Test updating an amenity"""
    print(f"\n=== Testing Update Amenity: {amenity_id} ===")

    update_data = {
        "description": "Ultra-fast wireless internet with unlimited data"
    }

    response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json=update_data)

    print_response(response)
    return response.status_code == 200

def test_invalid_update(amenity_id):
    """Test updating an amenity with invalid data"""
    print(f"\n=== Testing Invalid Update: {amenity_id} ===")

    invalid_data = {
        "name": ""
    }

    response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json=invalid_data)

    print_response(response)
    return response.status_code == 400

def test_nonexistent_amenity():
    """Test getting a nonexistent amenity"""
    print("\n=== Testing Nonexistent Amenity ===")

    response = requests.get(f"{BASE_URL}/amenities/nonexistent-id")

    print_response(response)
    return response.status_code == 404

def main():
    """Main function to run the tests"""
    print("Starting Amenity API Tests")
    print(f"API base URL: {BASE_URL}")
    print("Author: alearecuest")
    print("Last updated: 2025-06-20 21:56:48")

    try:
        requests.get(f"{BASE_URL}/")
    except requests.exceptions.ConnectionError:
        print("\nERROR: Cannot connect to the server.")
        print("Make sure the server is running on http://localhost:5000/")
        print("Run the server with: python3 amenity_endpoints.py")
        sys.exit(1)

    print("\nWaiting for server to initialize...")
    time.sleep(1)

    if not test_api_root():
        print("\nWarning: API root endpoint test failed.")
        print("Some tests may still work, continuing...")

    amenity_id = test_create_amenity()
    
    if not amenity_id:
        print("Failed to create amenity. Aborting tests.")
        sys.exit(1)

    test_get_all_amenities()
    test_get_amenity_by_id(amenity_id)
    test_update_amenity(amenity_id)
    test_invalid_update(amenity_id)
    test_nonexistent_amenity()
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    main()
