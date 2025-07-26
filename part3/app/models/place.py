#!/usr/bin/python3
"""
Place model for the HBnB project
"""
from app.models.base_model import BaseModel
from app.extensions import db
from app.models.user import User
from app.models.associations import place_amenity

class Place(BaseModel):
    __tablename__ = 'places'

    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price       = db.Column(db.Float, nullable=False)
    latitude    = db.Column(db.Float, nullable=False)
    longitude   = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    owner    = db.relationship(
        'User',
        backref=db.backref('places', lazy=True),
        lazy=True
    )

    reviews = db.relationship(
        'Review',
        back_populates='place',
        lazy=True,
        cascade="all, delete-orphan"
    )

    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        lazy='subquery',
        backref=db.backref('places', lazy=True)
    )

    def __init__(self, title, description, price, latitude, longitude, owner, **kwargs):
        super().__init__(**kwargs)
        self.title       = title
        self.description = description
        self.price       = price
        self.latitude    = latitude
        self.longitude   = longitude
        self.owner       = owner
        self.validate()

    def validate(self):
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Title is required and must be a string")
        if len(self.title) > 100:
            raise ValueError("Title must be at most 100 characters")

        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("Description must be a string")

        if not isinstance(self.price, (int, float)) or self.price <= 0:
            raise ValueError("Price must be a positive number")

        if not isinstance(self.latitude, (int, float)) or not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")

        if not isinstance(self.longitude, (int, float)) or not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")

        if not isinstance(self.owner, User):
            raise ValueError("Owner must be a User instance")

    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def get_reviews(self):
        return self.reviews

    def get_amenities(self):
        return self.amenities
