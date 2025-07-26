#!/usr/bin/python3
"""
Amenity API endpoints for the HBnB project
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')
})

amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})


@api.route('/')
class AmenityList(Resource):
    @api.doc('create_amenity')
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created', amenity_response_model)
    @api.response(400, 'Invalid input data')
    @api.marshal_with(amenity_response_model, code=201)
    def post(self):
        """Register a new amenity"""
        amenity_data = request.json
        
        try:
            # Create new amenity
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('list_amenities')
    @api.response(200, 'List of amenities retrieved successfully', [amenity_response_model])
    @api.marshal_list_with(amenity_response_model)
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities]


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.response(200, 'Amenity details retrieved successfully', amenity_response_model)
    @api.response(404, 'Amenity not found')
    @api.marshal_with(amenity_response_model)
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity with ID {amenity_id} not found")
        return amenity.to_dict()

    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully', amenity_response_model)
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(500, 'Server error')
    @api.marshal_with(amenity_response_model)
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity with ID {amenity_id} not found")
        
        data = request.json
        
        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            if not updated_amenity:
                api.abort(404, f"Failed to update amenity with ID {amenity_id}")
            return updated_amenity.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            print(f"Unexpected error updating amenity: {str(e)}")
            api.abort(500, f"Server error: {str(e)}")
