#!/usr/bin/python3
"""
Validation utilities for HBnB API
"""
import re
from functools import wraps


def email_is_valid(email):
    """Check if email has a valid format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_user(func):
    """Decorator to validate user data"""
    @wraps(func)
    def wrapper(self, user_data):
        if 'first_name' not in user_data or not user_data['first_name']:
            raise ValueError("First name cannot be empty")
        
        if 'last_name' not in user_data or not user_data['last_name']:
            raise ValueError("Last name cannot be empty")
        
        if 'email' not in user_data or not user_data['email']:
            raise ValueError("Email cannot be empty")
        
        if not email_is_valid(user_data['email']):
            raise ValueError("Invalid email format")
        
        return func(self, user_data)
    return wrapper


def validate_place(func):
    """Decorator to validate place data"""
    @wraps(func)
    def wrapper(self, place_data):
        if 'title' not in place_data or not place_data['title']:
            raise ValueError("Title cannot be empty")
        
        if 'price' in place_data:
            try:
                price = float(place_data['price'])
                if price <= 0:
                    raise ValueError("Price must be a positive number")
            except (ValueError, TypeError):
                raise ValueError("Price must be a valid number")
        
        if 'latitude' in place_data:
            try:
                latitude = float(place_data['latitude'])
                if latitude < -90 or latitude > 90:
                    raise ValueError("Latitude must be between -90 and 90")
            except (ValueError, TypeError):
                raise ValueError("Latitude must be a valid number")
        
        if 'longitude' in place_data:
            try:
                longitude = float(place_data['longitude'])
                if longitude < -180 or longitude > 180:
                    raise ValueError("Longitude must be between -180 and 180")
            except (ValueError, TypeError):
                raise ValueError("Longitude must be a valid number")
        
        return func(self, place_data)
    return wrapper


def validate_review(func):
    """Decorator to validate review data"""
    @wraps(func)
    def wrapper(self, review_data):
        if 'text' not in review_data or not review_data['text']:
            raise ValueError("Review text cannot be empty")
        
        if 'rating' in review_data:
            try:
                rating = int(review_data['rating'])
                if rating < 1 or rating > 5:
                    raise ValueError("Rating must be between 1 and 5")
            except (ValueError, TypeError):
                raise ValueError("Rating must be a valid integer between 1 and 5")
        
        return func(self, review_data)
    return wrapper


def validate_amenity(func):
    """Decorator to validate amenity data"""
    @wraps(func)
    def wrapper(self, amenity_data):
        if 'name' not in amenity_data or not amenity_data['name']:
            raise ValueError("Amenity name cannot be empty")
        
        return func(self, amenity_data)
    return wrapper
