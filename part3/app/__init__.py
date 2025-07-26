#!/usr/bin/python3
"""
Initialize Flask application and register API
"""
from flask import Flask, redirect, jsonify
from app.extensions import bcrypt, jwt, db
from flask_restx import Api
from app.api.v1.auth import api as auth_ns

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Añadir token con formato: Bearer {token}'
    }
}

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='Holberton BnB API',
        prefix='/api/v1',
        doc='/api/v1',
        authorizations=authorizations,
        security='Bearer Auth'  
    )

    @app.route('/')
    def index():
        return redirect('/api/v1')

    @app.route('/info')
    def info():
        return jsonify({
            "name": "HBnB API",
            "version": "1.0",
            "author": "HolbertonG4MVD",
            "last_updated": "2025-07-24 14:29:05",
            "documentation": "/api/v1",
            "endpoints": {
                "users": "/api/v1/users",
                "amenities": "/api/v1/amenities",
                "places": "/api/v1/places",
                "reviews": "/api/v1/reviews",
                "auth": "/api/v1/auth",
                "protected": "/api/v1/protected"
            }
        })

    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns

    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(reviews_ns, path='/reviews')
    
    return app