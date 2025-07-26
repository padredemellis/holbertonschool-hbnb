#!/usr/bin/python3
"""
Review API endpoints
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

user_model = api.model('ReviewUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

place_model = api.model('ReviewPlace', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place')
})

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)')
})

review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user': fields.Nested(user_model, description='User who wrote the review'),
    'place': fields.Nested(place_model, description='Place being reviewed'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})

review_list_model = api.model('ReviewListItem', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)')
})


@api.route('/')
class ReviewList(Resource):
    @api.doc('create_review')
    @api.expect(review_model)
    @api.response(201, 'Review successfully created', review_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or place not found')
    def post(self):
        """Register a new review"""
        review_data = request.json
        
        try:
            new_review = facade.create_review(review_data)
            
            response = new_review.to_dict()
            
            response['user'] = {
                'id': new_review.user.id,
                'first_name': new_review.user.first_name,
                'last_name': new_review.user.last_name,
                'email': new_review.user.email
            }
            
            response['place'] = {
                'id': new_review.place.id,
                'title': new_review.place.title
            }
            
            return response, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('list_reviews')
    @api.response(200, 'List of reviews retrieved successfully', [review_list_model])
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        
        result = []
        for review in reviews:
            result.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            })
        return result


@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.doc('get_review')
    @api.response(200, 'Review details retrieved successfully', review_response_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Review with ID {review_id} not found")
        
        response = review.to_dict()
        
        response['user'] = {
            'id': review.user.id,
            'first_name': review.user.first_name,
            'last_name': review.user.last_name,
            'email': review.user.email
        }
        
        response['place'] = {
            'id': review.place.id,
            'title': review.place.title
        }
        
        return response

    @api.doc('update_review')
    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully', review_response_model)
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Review with ID {review_id} not found")
        
        data = request.json
        
        try:
            facade.update_review(review_id, data)
            
            review = facade.get_review(review_id)
            if not review:
                api.abort(404, f"Failed to retrieve review with ID {review_id} after update")
            
            response = review.to_dict()
            
            response['user'] = {
                'id': review.user.id,
                'first_name': review.user.first_name,
                'last_name': review.user.last_name,
                'email': review.user.email
            }
            
            response['place'] = {
                'id': review.place.id,
                'title': review.place.title
            }
            
            return response
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_review')
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        success = facade.delete_review(review_id)
        if not success:
            api.abort(404, f"Review with ID {review_id} not found")
        
        return {"message": "Review deleted successfully"}


@api.route('/places/<string:place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    @api.doc('get_place_reviews')
    @api.response(200, 'List of reviews for the place retrieved successfully', [review_list_model])
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            api.abort(404, f"Place with ID {place_id} not found")
        
        result = []
        for review in reviews:
            result.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            })
        return result
