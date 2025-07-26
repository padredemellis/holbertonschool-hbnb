#!/usr/bin/python3
"""
Test script for Amenity API endpoints in the HBnB application
"""
import requests
import json
import sys
from termcolor import colored

BASE_URL = "http://localhost:5000/api/v1"

test_amenities = [
    {
        "name": "Wi-Fi",
        "description": "High-speed wireless internet"
    },
    {
        "name": "Swimming Pool",
        "description": "Outdoor swimming pool with heating"
    },
    {
        "name": "Air Conditioning",
        "description": "Central air conditioning system"
    }
]

created_amenities = []

test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "errors": []
}


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(colored(f" {title} ".center(80, "="), "yellow", attrs=["bold"]))
    print("=" * 80)


def print_result(success, message):
    """Print a test result and track it"""
    test_results["total"] += 1
    
    if success:
        test_results["passed"] += 1
        print(colored(f"✅ {message}", "green"))
    else:
        test_results["failed"] += 1
        test_results["errors"].append(message)
        print(colored(f"❌ {message}", "red"))


def print_response(response, prefix="Response"):
    """Print the response data in a formatted way"""
    try:
        print(f"{prefix} Status: {response.status_code}")
        json_data = response.json()
        print(f"{prefix} Body: {json.dumps(json_data, indent=2)}")
    except ValueError:
        print(f"{prefix} Body: {response.text}")
    print("-" * 40)


def test_create_amenity():
    """Test creating an amenity (POST /api/v1/amenities/)"""
    print_header("TESTING AMENITY CREATION (POST)")
    
    for amenity_data in test_amenities:
        print(f"Creating amenity: {amenity_data['name']}")
        response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data)
        
        success = response.status_code == 201
        print_result(success, f"Create amenity with status {response.status_code}")
        print_response(response)
        
        if success:
            amenity_id = response.json().get('id')
            if amenity_id:
                created_amenities.append(amenity_id)
                print(f"Amenity created with ID: {amenity_id}")
    
    print("\nTesting invalid data (should fail):")
    invalid_data = {
        "name": "",
        "description": "Invalid amenity"
    }
    response = requests.post(f"{BASE_URL}/amenities/", json=invalid_data)
    success = response.status_code == 400
    print_result(success, f"Invalid data rejected with status {response.status_code}")
    print_response(response)


def test_get_all_amenities():
    """Test getting all amenities (GET /api/v1/amenities/)"""
    print_header("TESTING GET ALL AMENITIES")
    
    response = requests.get(f"{BASE_URL}/amenities/")
    success = response.status_code == 200
    print_result(success, f"Get all amenities with status {response.status_code}")
    print_response(response)
    
    amenities = response.json()
    expected_count = len(created_amenities)
    actual_count = len(amenities)
    count_match = actual_count >= expected_count
    print_result(count_match, f"Found {actual_count} amenities (expected at least {expected_count})")


def test_get_amenity_by_id():
    """Test getting an amenity by ID (GET /api/v1/amenities/<amenity_id>)"""
    print_header("TESTING GET AMENITY BY ID")
    
    if not created_amenities:
        print_result(False, "No amenities created to test with")
        return
    
    amenity_id = created_amenities[0]
    print(f"Testing with valid amenity ID: {amenity_id}")
    response = requests.get(f"{BASE_URL}/amenities/{amenity_id}")
    success = response.status_code == 200
    print_result(success, f"Get amenity by ID with status {response.status_code}")
    print_response(response)
    
    invalid_id = "non-existent-id"
    print(f"\nTesting with invalid amenity ID: {invalid_id}")
    response = requests.get(f"{BASE_URL}/amenities/{invalid_id}")
    success = response.status_code == 404
    print_result(success, f"Invalid ID rejected with status {response.status_code}")
    print_response(response)


def test_update_amenity():
    """Test updating an amenity (PUT /api/v1/amenities/<amenity_id>)"""
    print_header("TESTING UPDATE AMENITY")
    
    if not created_amenities:
        print_result(False, "No amenities created to test with")
        return
    
    amenity_id = created_amenities[0]
    update_data = {
        "name": "Updated Amenity",
        "description": "This amenity has been updated"
    }
    
    print(f"Updating amenity with ID: {amenity_id}")
    print(f"Update data: {json.dumps(update_data, indent=2)}")
    
    response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json=update_data)
    success = response.status_code == 200
    print_result(success, f"Update amenity with status {response.status_code}")
    print_response(response)
    
    if success:
        get_response = requests.get(f"{BASE_URL}/amenities/{amenity_id}")
        amenity_data = get_response.json()
        update_applied = (
            amenity_data.get('name') == update_data['name'] and
            amenity_data.get('description') == update_data['description']
        )
        print_result(update_applied, "Update was correctly applied to the amenity")
        if not update_applied:
            print_response(get_response, "Updated Amenity")
    
    invalid_id = "non-existent-id"
    print(f"\nTesting update with invalid amenity ID: {invalid_id}")
    response = requests.put(f"{BASE_URL}/amenities/{invalid_id}", json=update_data)
    success = response.status_code == 404
    print_result(success, f"Invalid ID rejected with status {response.status_code}")
    print_response(response)


def print_summary():
    """Print a summary of the test results"""
    print_header("TEST RESULTS SUMMARY")
    
    if test_results["total"] > 0:
        pass_percentage = (test_results["passed"] / test_results["total"]) * 100
    else:
        pass_percentage = 0
    
    print(f"Total Tests:  {test_results['total']}")
    print(colored(f"Tests Passed: {test_results['passed']} ({pass_percentage:.1f}%)", "green"))
    print(colored(f"Tests Failed: {test_results['failed']}", "red" if test_results["failed"] > 0 else "green"))
    
    if test_results["errors"]:
        print("\nFailed Tests:")
        for i, error in enumerate(test_results["errors"], 1):
            print(colored(f"  {i}. {error}", "red"))
    
    if test_results["failed"] == 0:
        print(colored("\n✅ ALL TESTS PASSED SUCCESSFULLY! ✅", "green", attrs=["bold"]))
        return True
    else:
        print(colored(f"\n❌ {test_results['failed']} TESTS FAILED! ❌", "red", attrs=["bold"]))
        return False


def run_tests():
    """Run all the tests"""
    print_header("STARTING AMENITY API ENDPOINT TESTS")
    print(f"Testing against API at: {BASE_URL}")
    print(f"Author: alearecuest")
    print(f"Last updated: 2025-06-21 17:32:45")
    
    try:
        requests.get(BASE_URL, timeout=2)
        
        test_create_amenity()
        test_get_all_amenities()
        test_get_amenity_by_id()
        test_update_amenity()
        
        print_header("ALL TESTS COMPLETED")
        print("Amenity IDs created during testing:", created_amenities)
        
        all_passed = print_summary()
        sys.exit(0 if all_passed else 1)
        
    except requests.exceptions.ConnectionError:
        print_result(False, f"Cannot connect to the API at {BASE_URL}")
        print("Make sure the server is running and the URL is correct.")
        sys.exit(1)
    except Exception as e:
        print_result(False, f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()