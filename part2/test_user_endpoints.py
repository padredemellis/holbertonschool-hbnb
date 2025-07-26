#!/usr/bin/python3
"""
Test script for User API endpoints in the HBnB application
"""
import requests
import json
import sys
import time
from termcolor import colored

BASE_URL = "http://localhost:5000/api/v1"

test_users = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "is_admin": False
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "is_admin": True
    },
    {
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice.johnson@example.com",
        "is_admin": False
    }
]

created_users = []

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


def test_create_user():
    """Test creating a user (POST /api/v1/users/)"""
    print_header("TESTING USER CREATION (POST)")
    
    for user_data in test_users:
        print(f"Creating user: {user_data['first_name']} {user_data['last_name']}")
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        
        success = response.status_code == 201
        print_result(success, f"Create user with status {response.status_code}")
        print_response(response)
        
        if success:
            user_id = response.json().get('id')
            if user_id:
                created_users.append(user_id)
                print(f"User created with ID: {user_id}")
    
    print("\nTesting duplicate email (should fail):")
    response = requests.post(f"{BASE_URL}/users/", json=test_users[0])
    success = response.status_code == 400
    print_result(success, f"Duplicate email rejected with status {response.status_code}")
    print_response(response)
    
    print("\nTesting invalid data (should fail):")
    invalid_data = {
        "first_name": "",
        "last_name": "Test",
        "email": "invalid-email"
    }
    response = requests.post(f"{BASE_URL}/users/", json=invalid_data)
    success = response.status_code == 400
    print_result(success, f"Invalid data rejected with status {response.status_code}")
    print_response(response)


def test_get_all_users():
    """Test getting all users (GET /api/v1/users/)"""
    print_header("TESTING GET ALL USERS")
    
    response = requests.get(f"{BASE_URL}/users/")
    success = response.status_code == 200
    print_result(success, f"Get all users with status {response.status_code}")
    print_response(response)
    
    users = response.json()
    expected_count = len(created_users)
    actual_count = len(users)
    count_match = actual_count >= expected_count
    print_result(count_match, f"Found {actual_count} users (expected at least {expected_count})")


def test_get_user_by_id():
    """Test getting a user by ID (GET /api/v1/users/<user_id>)"""
    print_header("TESTING GET USER BY ID")
    
    if not created_users:
        print_result(False, "No users created to test with")
        return
    
    user_id = created_users[0]
    print(f"Testing with valid user ID: {user_id}")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    success = response.status_code == 200
    print_result(success, f"Get user by ID with status {response.status_code}")
    print_response(response)
    
    invalid_id = "non-existent-id"
    print(f"\nTesting with invalid user ID: {invalid_id}")
    response = requests.get(f"{BASE_URL}/users/{invalid_id}")
    success = response.status_code == 404
    print_result(success, f"Invalid ID rejected with status {response.status_code}")
    print_response(response)


def test_update_user():
    """Test updating a user (PUT /api/v1/users/<user_id>)"""
    print_header("TESTING UPDATE USER")
    
    if not created_users:
        print_result(False, "No users created to test with")
        return
    
    user_id = created_users[0]
    update_data = {
        "first_name": "Updated",
        "last_name": "User",
        "email": "updated.user@example.com"
    }
    
    print(f"Updating user with ID: {user_id}")
    print(f"Update data: {json.dumps(update_data, indent=2)}")
    
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    success = response.status_code == 200
    print_result(success, f"Update user with status {response.status_code}")
    print_response(response)
    
    if success:
        get_response = requests.get(f"{BASE_URL}/users/{user_id}")
        user_data = get_response.json()
        update_applied = (
            user_data.get('first_name') == update_data['first_name'] and
            user_data.get('last_name') == update_data['last_name'] and
            user_data.get('email') == update_data['email']
        )
        print_result(update_applied, "Update was correctly applied to the user")
        if not update_applied:
            print_response(get_response, "Updated User")
    
    if len(created_users) > 1:
        second_user_response = requests.get(f"{BASE_URL}/users/{created_users[1]}")
        second_user_email = second_user_response.json().get('email')
        
        print(f"\nTesting update with duplicate email: {second_user_email}")
        
        update_data = {"email": second_user_email}
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
        success = response.status_code == 400
        print_result(success, f"Duplicate email rejected with status {response.status_code}")
        print_response(response)
    
    invalid_id = "non-existent-id"
    print(f"\nTesting update with invalid user ID: {invalid_id}")
    response = requests.put(f"{BASE_URL}/users/{invalid_id}", json=update_data)
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
    print_header("STARTING USER API ENDPOINT TESTS")
    print(f"Testing against API at: {BASE_URL}")
    print(f"Author: alearecuest")
    print(f"Last updated: 2025-06-21 13:48:25")
    
    try:
        requests.get(BASE_URL, timeout=2)
        
        test_create_user()
        test_get_all_users()
        test_get_user_by_id()
        test_update_user()
        
        print_header("ALL TESTS COMPLETED")
        print("User IDs created during testing:", created_users)
        
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
