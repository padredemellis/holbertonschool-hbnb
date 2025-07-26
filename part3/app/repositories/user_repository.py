#!/usr/bin/python3
"""
User repository for database operations
"""
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)
    
    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def email_exists(self, email):
        return User.query.filter_by(email=email).count() > 0
        
    def get_user_places(self, user_id):
        user = self.get(user_id)
        if user:
            return user.places
        return []
        
    def get_user_reviews(self, user_id):
        user = self.get(user_id)
        if user:
            return user.reviews
        return []
