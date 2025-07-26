#!/usr/bin/python3
"""
Amenity repository for database operations
"""
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.amenity import Amenity

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
    
    def get_amenity_by_name(self, name):
        return Amenity.query.filter_by(name=name).first()
    
    def name_exists(self, name):
        return Amenity.query.filter_by(name=name).count() > 0
        
    def get_amenity_places(self, amenity_id):
        amenity = self.get(amenity_id)
        if amenity:
            return amenity.places
        return []
