#!/usr/bin/python3
"""
Place API endpoints
"""
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restx import Namespace, Resource, fields
from app.services.facade import _facade as facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id':   fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

owner_model = api.model('PlaceUser', {
    'id':         fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name':  fields.String(description='Last name of the owner'),
    'email':      fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id':     fields.String(description='Review ID'),
    'text':   fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user':   fields.Nested(owner_model, description='User who wrote the review')
})

place_model = api.model('Place', {
    'title':       fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price':       fields.Float(required=True, description='Price per night'),
    'latitude':    fields.Float(required=True, description='Latitude of the place'),
    'longitude':   fields.Float(required=True, description='Longitude of the place'),
    'owner_id':    fields.String(description='ID of the owner'),
    'amenities':   fields.List(fields.String, description="List of amenities ID's")
})

place_response_model = api.model('PlaceResponse', {
    'id':         fields.String(description='Place ID'),
    'title':      fields.String(description='Title of the place'),
    'description':fields.String(description='Description of the place'),
    'price':      fields.Float(description='Price per night'),
    'latitude':   fields.Float(description='Latitude of the place'),
    'longitude':  fields.Float(description='Longitude of the place'),
    'owner':      fields.Nested(owner_model, description='Owner of the place'),
    'amenities':  fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews':    fields.List(fields.Nested(review_model), description='List of reviews'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})

place_list_model = api.model('PlaceListItem', {
    'id':        fields.String(description='Place ID'),
    'title':     fields.String(description='Title of the place'),
    'latitude':  fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place')
})

new_review_model = api.model('NewReview', {
    'text':   fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('create_place')
    @api.expect(place_model)
    @api.response(201, 'Place successfully created', place_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner or amenity not found')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def post(self):
        """Register a new place"""
        place_data = request.json or {}
        place_data['price'] = float(place_data.get('price', 0))
        place_data['latitude'] = float(place_data.get('latitude', 0))
        place_data['longitude']= float(place_data.get('longitude', 0))
        place_data['owner_id'] = get_jwt_identity()
        place_data.setdefault('amenities', [])

        try:
            new_place = facade.create_place(place_data)
            return facade.get_place(new_place['id']), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('list_places')
    @api.response(200, 'List of places retrieved successfully', [place_list_model])
    def get(self):
        """Retrieve a list of all places"""
        return facade.get_all_places(), 200

@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.response(200, 'Place details retrieved successfully', place_response_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place with ID {place_id} not found")
        return place, 200

    @api.doc('update_place')
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully', place_response_model)
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place with ID {place_id} not found")

        claims = get_jwt()
        current_user = get_jwt_identity()
        is_admin = claims.get('is_admin', False)
        if not is_admin and place['owner']['id'] != current_user:
            api.abort(403, "Unauthorized action")

        try:
            facade.update_place(place_id, request.json or {})
            return facade.get_place(place_id), 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_place')
    @api.response(204, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place with ID {place_id} not found")

        claims = get_jwt()
        current_user = get_jwt_identity()
        is_admin = claims.get('is_admin', False)
        if not is_admin and place['owner']['id'] != current_user:
            api.abort(403, "Unauthorized action")

        facade.delete_place(place_id)
        return '', 204

@api.route('/<string:place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    @api.doc('list_reviews_for_place')
    @api.response(200, 'List of reviews retrieved', [review_model])
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """List all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place with ID {place_id} not found")
        return facade.get_reviews_by_place(place_id), 200

    @api.doc('create_review')
    @api.expect(new_review_model)
    @api.response(201, 'Review created successfully', review_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def post(self, place_id):
        """Create a new review for a place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place with ID {place_id} not found")

        data = request.json or {}
        data['place_id'] = place_id
        data['user_id']  = get_jwt_identity()
        try:
            new_rev = facade.create_review(data)
            return facade.get_review(new_rev.id), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:place_id>/amenities/')
@api.param('place_id', 'The place identifier')
class PlaceAmenityList(Resource):
    @api.doc('list_amenities_for_place')
    @api.response(200, 'List of amenities retrieved', [amenity_model])
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """List all amenities linked to a place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place with ID {place_id} not found")
        return facade.get_amenities_by_place(place_id), 200

@api.route('/<string:place_id>/amenities/<string:amenity_id>')
@api.param('place_id', 'The place identifier')
@api.param('amenity_id', 'The amenity identifier')
class PlaceAmenity(Resource):
    @api.doc('link_amenity_to_place')
    @api.response(201, 'Amenity linked to place', amenity_model)
    @api.response(404, 'Place or amenity not found')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def post(self, place_id, amenity_id):
        """Link an amenity to a place"""
        linked = facade.add_amenity_to_place(place_id, amenity_id)
        if not linked:
            api.abort(404, "Place or amenity not found")
        return linked, 201

    @api.doc('unlink_amenity_from_place')
    @api.response(204, 'Amenity unlinked successfully')
    @api.response(404, 'Place or amenity not found')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def delete(self, place_id, amenity_id):
        """Unlink an amenity from a place"""
        success = facade.remove_amenity_from_place(place_id, amenity_id)
        if not success:
            api.abort(404, "Place or amenity not found")
        return '', 204
