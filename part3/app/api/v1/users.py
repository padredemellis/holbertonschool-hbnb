#!/usr/bin/python3
"""
User API endpoints
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import _facade as facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')

user_model = api.model('User', {    
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password for user'),
    'is_admin': fields.Boolean(description='Admin status of the user')
})

user_update_model = api.model('UserUpdate', {    
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password for user'),
    'is_admin': fields.Boolean(description='Admin status of the user')
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Admin status of the user'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})

@api.route('/')
class UserList(Resource):
    @api.doc('create_user', security='Bearer Auth')
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', user_response_model)
    @api.response(400, 'Email already registered or invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Admin privileges required')
    @api.marshal_with(user_response_model, code=201)
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, "Admin privileges required to create users")
            
        user_data = request.get_json() or {}

        existing_user = facade.get_user_by_email(user_data.get('email'))
        if existing_user:
            api.abort(400, "Email already registered")

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('list_users')
    @api.response(200, 'List of users retrieved successfully', [user_response_model])
    @api.marshal_list_with(user_response_model)
    def get(self):
        users = facade.get_all_users()
        return [user.to_dict() for user in users]


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user', security='Bearer Auth')
    @api.response(200, 'User details retrieved successfully', user_response_model)
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.marshal_with(user_response_model)
    @jwt_required()
    def get(self, user_id):
        claims = get_jwt()
        current_user = get_jwt_identity()
        
        if not (claims.get('is_admin', False) or current_user == user_id):
            api.abort(403, "Unauthorized access")

        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User with ID {user_id} not found")
        return user.to_dict()

    @api.doc('update_user', security='Bearer Auth')
    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully', user_response_model)
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(user_response_model)
    @jwt_required()
    def put(self, user_id):
        claims = get_jwt()
        current_user = get_jwt_identity()
        is_admin = claims.get('is_admin', False)
        
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User with ID {user_id} not found")
            
        data = request.get_json() or {}

        if not (is_admin or current_user == user_id):
            api.abort(403, "Unauthorized action")
            
        if is_admin:
            if 'email' in data and data['email'] != user.email:
                existing_user = facade.get_user_by_email(data['email'])
                if existing_user and existing_user.id != user_id:
                    api.abort(400, "Email already registered")
            try:
                updated_user = facade.update_user(user_id, data)
                return updated_user.to_dict()
            except ValueError as e:
                api.abort(400, str(e))
                
        else:
            restricted_fields = ['email', 'password', 'is_admin']
            for field in restricted_fields:
                if field in data:
                    api.abort(400, f"You cannot modify {field} through this endpoint")
                    
            try:
                updated_user = facade.update_user(user_id, data)
                return updated_user.to_dict()
            except ValueError as e:
                api.abort(400, str(e))

    @api.doc('delete_user', security='Bearer Auth')
    @api.response(204, 'User deleted successfully')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @jwt_required()
    def delete(self, user_id):
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, "Admin privileges required to delete users")
            
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User with ID {user_id} not found")
            
        success = facade.delete_user(user_id)
        return '', 204