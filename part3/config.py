#!/usr/bin/python3
"""
Configuration for the HBnB project
"""
import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'temporarysecret')
    DEBUG = False
    
    # Configuración JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'temporaryjwtsecret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}