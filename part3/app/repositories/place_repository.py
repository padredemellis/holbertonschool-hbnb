#!/usr/bin/python3
"""
Place repository for database operations
"""
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.place import Place

class PlaceRepository(SQLAlchemyRepository):
    
    def __init__(self):
        super().__init__(Place)
    
    def get_places_by_price_range(self, min_price, max_price):
        return Place.query.filter(
            Place.price >= min_price,
            Place.price <= max_price
        ).all()
    
    def get_places_by_owner(self, owner_id):
        return Place.query.filter_by(owner_id=owner_id).all()
    
    def add_amenity_to_place(self, place_id, amenity):
        place = self.get(place_id)
        if place and amenity not in place.amenities:
            place.amenities.append(amenity)
            self.session.commit()
            return place
        return None
