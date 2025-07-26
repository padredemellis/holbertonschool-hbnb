#!/usr/bin/python3
"""
Extensions for the HBnB application
"""
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()
