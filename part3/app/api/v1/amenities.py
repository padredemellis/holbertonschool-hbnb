#!/usr/bin/python3
"""
Amenity API endpoints for the HBnB project
"""
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity'),
})

amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp'),
})

@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.response(200, 'List of amenities retrieved successfully', [amenity_response_model])
    @api.marshal_list_with(amenity_response_model)
    def get(self):
        """Retrieve a list of all amenities (public)"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities]

    @api.doc('create_amenity')
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created', amenity_response_model)
    @api.response(400, 'Invalid input data')
    @api.marshal_with(amenity_response_model, code=201)
    @jwt_required()
    def post(self):
        """Register a new amenity (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, "Admin privileges required")

        data = request.get_json() or {}
        if 'name' not in data or not data['name']:
            api.abort(400, "Missing name")

        try:
            new = facade.create_amenity(data)
            return new.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.response(200, 'Amenity details retrieved successfully', amenity_response_model)
    @api.response(404, 'Amenity not found')
    @api.marshal_with(amenity_response_model)
    def get(self, amenity_id):
        """Get amenity details by ID (public)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity.to_dict()

    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully', amenity_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    @api.marshal_with(amenity_response_model)
    @jwt_required()
    def put(self, amenity_id):
        """Update an existing amenity (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, "Admin privileges required")

        data = request.get_json() or {}
        if 'name' in data and not data['name']:
            api.abort(400, "Amenity name cannot be empty")

        try:
            updated = facade.update_amenity(amenity_id, data)
            if not updated:
                api.abort(404, "Amenity not found")
            return updated.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_amenity')
    @api.response(204, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, "Admin privileges required")

        success = facade.delete_amenity(amenity_id)
        if not success:
            api.abort(404, "Amenity not found")
        return '', 204
