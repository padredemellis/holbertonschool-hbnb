#!/usr/bin/python3
"""
Place API endpoints
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

owner_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Añadir modelo de review para la respuesta de place
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user': fields.Nested(owner_model, description='User who wrote the review')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})

place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(owner_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})

place_list_model = api.model('PlaceListItem', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place')
})


@api.route('/')
class PlaceList(Resource):
    @api.doc('create_place')
    @api.expect(place_model)
    @api.response(201, 'Place successfully created', place_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner or amenity not found')
    def post(self):
        """Register a new place"""
        place_data = request.json
        
        try:
            new_place = facade.create_place(place_data)
            
            place_details = facade.get_place(new_place.id)
            return place_details, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('list_places')
    @api.response(200, 'List of places retrieved successfully', [place_list_model])
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return places


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
        return place

    @api.doc('update_place')
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully', place_response_model)
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place with ID {place_id} not found")
        
        data = request.json
        
        try:
            updated_place = facade.update_place(place_id, data)
            
            place_details = facade.get_place(place_id)
            if place_details:
                return place_details
            else:
                api.abort(404, f"Failed to retrieve place with ID {place_id} after update")
        except ValueError as e:
            api.abort(400, str(e))
