#!/usr/bin/python3
"""
Authentication API endpoints
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, create_refresh_token
from app.services.facade import _facade as facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email':    fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

register_model = api.model('Register', {
    'email':      fields.String(required=True, description='User email'),
    'password':   fields.String(required=True, description='User password'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name':  fields.String(required=True, description='User last name'),
    'is_admin':   fields.Boolean(description='Is admin user', required=False)
})

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    @api.response(201, 'User registered successfully')
    @api.response(400, 'Email already exists or invalid data')
    def post(self):
        """Register a new user"""
        user_data = api.payload or {}
        user_data['is_admin'] = user_data.get('is_admin', False)

        # Check if email is already in use
        if facade.get_user_by_email(user_data['email']):
            api.abort(400, "Email already exists")

        try:
            new_user = facade.create_user(user_data)
            user_dict = new_user.to_dict()
            user_dict.pop('password', None)
            return user_dict, 201
        except Exception as e:
            api.abort(400, str(e))


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(400, 'Validation error')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate a user and return tokens"""
        creds = api.payload or {}
        email    = creds.get('email')
        password = creds.get('password')

        if not email or not password:
            api.abort(400, "Email and password are required")

        user = facade.get_user_by_email(email)
        if not user or not user.verify_password(password):
            api.abort(401, "Invalid email or password")

        access_token  = create_access_token(
            identity=str(user.id),
            additional_claims={'is_admin': user.is_admin}
        )
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            'access_token':  access_token,
            'refresh_token': refresh_token
        }, 200
