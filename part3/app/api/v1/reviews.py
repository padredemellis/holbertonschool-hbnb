#!/usr/bin/python3
"""
Review API endpoints
"""
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services.facade import _facade as facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'id':         fields.String(description='Review ID'),
    'text':       fields.String(required=True, description='Text of the review'),
    'rating':     fields.Integer(required=True, description='Rating (1-5)'),
    'user_id':    fields.String(description='User ID'),
    'place_id':   fields.String(description='Place ID'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})

new_review_model = api.model('NewReview', {
    'text':   fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})

@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.response(200, 'Reviews retrieved', [review_model])
    def get(self):
        """List all reviews"""
        return facade.get_all_reviews(), 200

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.doc('get_review')
    @api.response(200, 'Review retrieved', review_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a single review by ID"""
        rev = facade.get_review(review_id)
        if not rev:
            api.abort(404, f"Review with ID {review_id} not found")
        return rev, 200

    @api.doc('update_review')
    @api.expect(new_review_model)
    @api.response(200, 'Review updated', review_model)
    @api.response(400, 'Invalid input')
    @api.response(404, 'Review not found')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        try:
            updated = facade.update_review(review_id, request.json or {})
            if not updated:
                api.abort(404, f"Review with ID {review_id} not found")
            return updated, 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_review')
    @api.response(204, 'Review deleted')
    @api.response(404, 'Review not found')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        success = facade.delete_review(review_id)
        if not success:
            api.abort(404, f"Review with ID {review_id} not found")
        return '', 204
