# HBnB API Testing Report

## 1. Introduction

This document details the testing process for the HBnB API, including validation mechanisms, test cases, and results. The testing covers all implemented endpoints and focuses on both successful scenarios and error handling.

## 2. Validation Implementation

### 2.1 User Model Validation
- **First Name**: Cannot be empty
- **Last Name**: Cannot be empty
- **Email**: Cannot be empty and must have a valid format (example@domain.com)

### 2.2 Place Model Validation
- **Title**: Cannot be empty
- **Price**: Must be a positive number
- **Latitude**: Must be between -90 and 90
- **Longitude**: Must be between -180 and 180
- **Owner ID**: Must reference an existing user

### 2.3 Review Model Validation
- **Text**: Cannot be empty
- **Rating**: Must be an integer between 1 and 5
- **User ID**: Must reference an existing user
- **Place ID**: Must reference an existing place

### 2.4 Amenity Model Validation
- **Name**: Cannot be empty

## 3. Endpoint Testing Results

### 3.1 User Endpoints

#### POST /api/v1/users/
- **Success Case**: Creates a new user with valid data
  - Status Code: 201
  - Response includes user ID and provided data
- **Error Case 1**: Attempt to create user with invalid email
  - Status Code: 400
  - Error message: "Invalid email format"
- **Error Case 2**: Attempt to create user with missing fields
  - Status Code: 400
  - Error message: "[field name] cannot be empty"

#### GET /api/v1/users/
- **Success Case**: Returns a list of all users
  - Status Code: 200
  - Response is an array of user objects

#### GET /api/v1/users/{user_id}
- **Success Case**: Returns details of a specific user
  - Status Code: 200
  - Response includes full user data
- **Error Case**: Attempt to get a nonexistent user
  - Status Code: 404
  - Error message: "User with ID [id] not found"

#### PUT /api/v1/users/{user_id}
- **Success Case**: Updates a user's information
  - Status Code: 200
  - Response includes updated user data
- **Error Case 1**: Attempt to update nonexistent user
  - Status Code: 404
  - Error message: "User with ID [id] not found"
- **Error Case 2**: Attempt to update with invalid data
  - Status Code: 400
  - Error message depends on the validation failure

### 3.2 Amenity Endpoints

#### POST /api/v1/amenities/
- **Success Case**: Creates a new amenity with valid data
  - Status Code: 201
  - Response includes amenity ID and name
- **Error Case**: Attempt to create amenity with empty name
  - Status Code: 400
  - Error message: "Amenity name cannot be empty"

#### GET /api/v1/amenities/
- **Success Case**: Returns a list of all amenities
  - Status Code: 200
  - Response is an array of amenity objects

#### GET /api/v1/amenities/{amenity_id}
- **Success Case**: Returns details of a specific amenity
  - Status Code: 200
  - Response includes full amenity data
- **Error Case**: Attempt to get a nonexistent amenity
  - Status Code: 404
  - Error message: "Amenity with ID [id] not found"

#### PUT /api/v1/amenities/{amenity_id}
- **Success Case**: Updates an amenity's information
  - Status Code: 200
  - Response includes updated amenity data
- **Error Case 1**: Attempt to update nonexistent amenity
  - Status Code: 404
  - Error message: "Amenity with ID [id] not found"
- **Error Case 2**: Attempt to update with empty name
  - Status Code: 400
  - Error message: "Amenity name cannot be empty"

### 3.3 Place Endpoints

#### POST /api/v1/places/
- **Success Case**: Creates a new place with valid data
  - Status Code: 201
  - Response includes place ID and provided data
- **Error Case 1**: Attempt to create place with invalid latitude
  - Status Code: 400
  - Error message: "Latitude must be between -90 and 90"
- **Error Case 2**: Attempt to create place with invalid price
  - Status Code: 400
  - Error message: "Price must be a positive number"
- **Error Case 3**: Attempt to create place with nonexistent owner
  - Status Code: 400
  - Error message: "Owner with ID [id] not found"

#### GET /api/v1/places/
- **Success Case**: Returns a list of all places
  - Status Code: 200
  - Response is an array of place objects with basic information

#### GET /api/v1/places/{place_id}
- **Success Case**: Returns details of a specific place
  - Status Code: 200
  - Response includes full place data with owner and amenities
- **Error Case**: Attempt to get a nonexistent place
  - Status Code: 404
  - Error message: "Place with ID [id] not found"

#### PUT /api/v1/places/{place_id}
- **Success Case**: Updates a place's information
  - Status Code: 200
  - Response includes updated place data
- **Error Case 1**: Attempt to update nonexistent place
  - Status Code: 404
  - Error message: "Place with ID [id] not found"
- **Error Case 2**: Attempt to update with invalid data
  - Status Code: 400
  - Error message depends on the validation failure

### 3.4 Review Endpoints

#### POST /api/v1/reviews/
- **Success Case**: Creates a new review with valid data
  - Status Code: 201
  - Response includes review ID and provided data
- **Error Case 1**: Attempt to create review with invalid rating
  - Status Code: 400
  - Error message: "Rating must be between 1 and 5"
- **Error Case 2**: Attempt to create review with empty text
  - Status Code: 400
  - Error message: "Review text cannot be empty"
- **Error Case 3**: Attempt to create review with nonexistent user/place
  - Status Code: 400
  - Error message: "User/Place with ID [id] not found"

#### GET /api/v1/reviews/
- **Success Case**: Returns a list of all reviews
  - Status Code: 200
  - Response is an array of review objects with basic information

#### GET /api/v1/reviews/{review_id}
- **Success Case**: Returns details of a specific review
  - Status Code: 200
  - Response includes full review data with user and place info
- **Error Case**: Attempt to get a nonexistent review
  - Status Code: 404
  - Error message: "Review with ID [id] not found"

#### GET /api/v1/reviews/places/{place_id}/reviews
- **Success Case**: Returns all reviews for a specific place
  - Status Code: 200
  - Response is an array of review objects
- **Error Case**: Attempt to get reviews for nonexistent place
  - Status Code: 404
  - Error message: "Place with ID [id] not found"

#### PUT /api/v1/reviews/{review_id}
- **Success Case**: Updates a review's information
  - Status Code: 200
  - Response includes updated review data
- **Error Case 1**: Attempt to update nonexistent review
  - Status Code: 404
  - Error message: "Review with ID [id] not found"
- **Error Case 2**: Attempt to update with invalid data
  - Status Code: 400
  - Error message depends on the validation failure

#### DELETE /api/v1/reviews/{review_id}
- **Success Case**: Deletes a review
  - Status Code: 200
  - Response contains success message
- **Error Case**: Attempt to delete nonexistent review
  - Status Code: 404
  - Error message: "Review with ID [id] not found"

## 4. Test Coverage

The testing process covered:
- All API endpoints (GET, POST, PUT, DELETE)
- Both successful and error scenarios
- Validation of input data
- Proper error handling
- Relationships between entities (users owning places, places having reviews, etc.)

## 5. Swagger Documentation

The API is fully documented using Swagger, which can be accessed at:
`http://localhost:5000/api/v1/`

This documentation provides:
- Complete list of all endpoints
- Request and response models
- Required and optional fields
- Description of each endpoint's purpose

## 6. Conclusion

The HBnB API has been thoroughly tested and validated. All endpoints are functioning as expected, with proper validation and error handling. The API provides a robust foundation for building client applications that interact with the HBnB service.
