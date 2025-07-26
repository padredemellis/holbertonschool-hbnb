#!/usr/bin/python3
"""
User API endpoints
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
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
    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', user_response_model)
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(user_response_model, code=201)
    def post(self):
        """Register a new user"""
        user_data = request.json

        existing_user = facade.get_user_by_email(user_data['email'])
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
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users]


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.response(200, 'User details retrieved successfully', user_response_model)
    @api.response(404, 'User not found')
    @api.marshal_with(user_response_model)
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User with ID {user_id} not found")
        return user.to_dict()

    @api.doc('update_user')
    @api.expect(user_model)
    @api.response(200, 'User updated successfully', user_response_model)
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(user_response_model)
    def put(self, user_id):
        """Update a user's information"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User with ID {user_id} not found")

        data = request.json
        
        if 'email' in data and data['email'] != user.email:
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                api.abort(400, "Email already registered")
        
        try:
            updated_user = facade.update_user(user_id, data)
            
            if not updated_user:
                updated_user = facade.get_user(user_id)
                if not updated_user:
                    api.abort(404, f"Failed to update user with ID {user_id}")
            
            return updated_user.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
