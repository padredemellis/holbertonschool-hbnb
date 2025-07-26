#!/usr/bin/python3
"""
Initialize Flask application and register API
"""
from flask import Flask, redirect, jsonify

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        """Redireccionar a la documentación API"""
        return redirect('/api/v1')
    
    @app.route('/info')
    def info():
        """Mostrar información básica sobre la API"""
        return jsonify({
            "name": "HBnB API",
            "version": "1.0",
            "author": "HolbertonG4MVD",
            "last_updated": "2025-06-22 15:49:03",
            "documentation": "/api/v1",
            "endpoints": {
                "users": "/api/v1/users",
                "amenities": "/api/v1/amenities",
                "places": "/api/v1/places",
                "reviews": "/api/v1/reviews"
            }
        })
    
    from flask_restx import Api
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='Holberton BnB API',
        prefix='/api/v1',
        doc='/api/v1'
    )
    
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(reviews_ns, path='/reviews')
    
    return app
