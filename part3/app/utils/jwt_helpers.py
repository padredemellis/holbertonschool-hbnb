#!/usr/bin/python3
"""
JWT helper utilities for testing and demonstrating authentication
"""
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace("jwt_test", description="JWT testing utilities")

@api.route("/test")
class JWTTestResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        claims = get_jwt()
        return {
            "message": f"Autenticación exitosa para usuario {current_user}",
            "is_admin": claims.get('is_admin', False)
        }, 200