#!/usr/bin/python3
"""
Unit tests for HBnB API
"""
import unittest
import json
from app import create_app


class TestHBnBAPI(unittest.TestCase):
    """Test cases for HBnB API endpoints"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.user_id = None
        self.amenity_id = None
        self.place_id = None
        self.review_id = None

    def test_01_create_user(self):
        """Test user creation"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], "Test")
        self.assertEqual(data['last_name'], "User")
        self.assertEqual(data['email'], "test.user@example.com")
        self.__class__.user_id = data['id']

        response = self.client.post('/api/v1/users/', json={
            "first_name": "Invalid",
            "last_name": "Email",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/api/v1/users/', json={
            "first_name": "Missing",
            "last_name": "Fields"
        })
        self.assertEqual(response.status_code, 400)

    def test_02_get_user(self):
        """Test getting user details"""
        response = self.client.get(f'/api/v1/users/{self.__class__.user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], "Test")
        
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_03_update_user(self):
        """Test updating user information"""
        response = self.client.put(f'/api/v1/users/{self.__class__.user_id}', json={
            "first_name": "Updated",
            "last_name": "User"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], "Updated")
        self.assertEqual(data['last_name'], "User")

    def test_04_create_amenity(self):
        """Test amenity creation"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Test Amenity"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], "Test Amenity")
        self.__class__.amenity_id = data['id']

        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_05_get_amenity(self):
        """Test getting amenity details"""
        response = self.client.get(f'/api/v1/amenities/{self.__class__.amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Test Amenity")
        
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_06_update_amenity(self):
        """Test updating amenity information"""
        response = self.client.put(f'/api/v1/amenities/{self.__class__.amenity_id}', json={
            "name": "Updated Amenity"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Updated Amenity")

    def test_07_create_place(self):
        """Test place creation"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A place for testing",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.__class__.user_id,
            "amenities": [self.__class__.amenity_id]
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], "Test Place")
        self.__class__.place_id = data['id']

        response = self.client.post('/api/v1/places/', json={
            "title": "Invalid Place",
            "description": "A place with invalid latitude",
            "price": 100.0,
            "latitude": 100.0,
            "longitude": -74.0060,
            "owner_id": self.__class__.user_id
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/api/v1/places/', json={
            "title": "Invalid Place",
            "description": "A place with invalid price",
            "price": -50.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.__class__.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_08_get_place(self):
        """Test getting place details"""
        response = self.client.get(f'/api/v1/places/{self.__class__.place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Test Place")
        
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_09_update_place(self):
        """Test updating place information"""
        response = self.client.put(f'/api/v1/places/{self.__class__.place_id}', json={
            "title": "Updated Place",
            "price": 120.0
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Updated Place")
        self.assertEqual(data['price'], 120.0)

    def test_10_create_review(self):
        """Test review creation"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Test review",
            "rating": 4,
            "user_id": self.__class__.user_id,
            "place_id": self.__class__.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['text'], "Test review")
        self.assertEqual(data['rating'], 4)
        self.__class__.review_id = data['id']

        response = self.client.post('/api/v1/reviews/', json={
            "text": "Invalid review",
            "rating": 6,
            "user_id": self.__class__.user_id,
            "place_id": self.__class__.place_id
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 4,
            "user_id": self.__class__.user_id,
            "place_id": self.__class__.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_11_get_review(self):
        """Test getting review details"""
        response = self.client.get(f'/api/v1/reviews/{self.__class__.review_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['text'], "Test review")
        
        response = self.client.get('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_12_get_place_reviews(self):
        """Test getting reviews for a place"""
        response = self.client.get(f'/api/v1/reviews/places/{self.__class__.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)

    def test_13_update_review(self):
        """Test updating review"""
        response = self.client.put(f'/api/v1/reviews/{self.__class__.review_id}', json={
            "text": "Updated review",
            "rating": 5
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['text'], "Updated review")
        self.assertEqual(data['rating'], 5)

    def test_14_delete_review(self):
        """Test deleting review"""
        response = self.client.delete(f'/api/v1/reviews/{self.__class__.review_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        
        response = self.client.delete(f'/api/v1/reviews/{self.__class__.review_id}')
        self.assertEqual(response.status_code, 404)
        
        response = self.client.get(f'/api/v1/reviews/{self.__class__.review_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
