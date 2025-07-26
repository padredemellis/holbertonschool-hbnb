#!/usr/bin/python3
"""
Test script for the HBnB models
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def test_user_creation():
    """Test User class creation and validation"""
    print("\n=== Testing User Creation ===")
    
    try:
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )
        print(f"User created successfully: {user.to_dict()}")
    except ValueError as e:
        print(f"Error creating user: {e}")
    
    try:
        user = User(
            first_name="Jane",
            last_name="Doe",
            email="invalid-email"
        )
        print("Should not reach here - invalid email")
    except ValueError as e:
        print(f"Expected error with invalid email: {e}")
    
    return user


def test_place_creation(owner):
    """Test Place class creation and validation"""
    print("\n=== Testing Place Creation ===")
    
    try:
        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100.0,
            latitude=37.7749,
            longitude=-122.4194,
            owner=owner
        )
        print(f"Place created successfully: {place.to_dict()}")
    except ValueError as e:
        print(f"Error creating place: {e}")
    
    # Test invalid price
    try:
        place = Place(
            title="Invalid Place",
            description="This place has a negative price",
            price=-50.0,
            latitude=37.7749,
            longitude=-122.4194,
            owner=owner
        )
        print("Should not reach here - negative price")
    except ValueError as e:
        print(f"Expected error with negative price: {e}")
    
    return place


def test_amenity_creation():
    """Test Amenity class creation and validation"""
    print("\n=== Testing Amenity Creation ===")
    
    amenities = []
    
    for name in ["WiFi", "Pool", "Air Conditioning", "Gym"]:
        try:
            amenity = Amenity(name=name)
            amenities.append(amenity)
            print(f"Amenity '{name}' created successfully: {amenity.to_dict()}")
        except ValueError as e:
            print(f"Error creating amenity: {e}")
    
    try:
        amenity = Amenity(name="A" * 51)
        print("Should not reach here - name too long")
    except ValueError as e:
        print(f"Expected error with long name: {e}")
    
    return amenities


def test_review_creation(place, user):
    """Test Review class creation and validation"""
    print("\n=== Testing Review Creation ===")
    
    try:
        review = Review(
            text="Great place to stay!",
            rating=5,
            place=place,
            user=user
        )
        print(f"Review created successfully: {review.to_dict()}")
    except ValueError as e:
        print(f"Error creating review: {e}")
    
    try:
        review = Review(
            text="Invalid rating",
            rating=6,  # Should be 1-5
            place=place,
            user=user
        )
        print("Should not reach here - rating out of range")
    except ValueError as e:
        print(f"Expected error with invalid rating: {e}")
    
    return review


def test_relationships(place, amenities):
    """Test relationships between models"""
    print("\n=== Testing Relationships ===")

    for amenity in amenities:
        place.add_amenity(amenity)
    
    place_amenities = place.get_amenities()
    print(f"Place has {len(place_amenities)} amenities:")
    for amenity in place_amenities:
        print(f"  - {amenity.name}")
    
    place_reviews = place.get_reviews()
    print(f"Place has {len(place_reviews)} reviews:")
    for review in place_reviews:
        print(f"  - Rating: {review.rating}, Text: {review.text}")


def main():
    """Main function to run all tests"""
    print("Starting tests for HBnB models")
    print("Author: alearecuest")
    print("Last updated: 2025-06-21 02:52:13")
    
    user = test_user_creation()
    
    place = test_place_creation(user)
    
    amenities = test_amenity_creation()
    
    review = test_review_creation(place, user)
    
    test_relationships(place, amenities)
    
    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    main()
