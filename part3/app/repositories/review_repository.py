#!/usr/bin/python3
"""
Review repository for database operations
"""
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.review import Review

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)
    
    def get_reviews_by_rating(self, min_rating):
        return Review.query.filter(Review.rating >= min_rating).all()
        
    def get_reviews_by_place(self, place_id):
        return Review.query.filter_by(place_id=place_id).all()
        
    def get_reviews_by_user(self, user_id):
        return Review.query.filter_by(user_id=user_id).all()
