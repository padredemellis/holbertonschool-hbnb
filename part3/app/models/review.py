#!/usr/bin/python3
"""
Review model for the HBnB project
"""
from app.models.base_model import BaseModel
from app.extensions import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text     = db.Column(db.Text,    nullable=False)
    rating   = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id  = db.Column(db.String(36), db.ForeignKey('users.id'),  nullable=False)

    place = db.relationship(
        'Place',
        back_populates='reviews',
        lazy=True
    )
    user  = db.relationship(
        'User',
        back_populates='reviews',
        lazy=True
    )

    def __init__(self, text, rating, place, user, **kwargs):
        super().__init__(**kwargs)
        self.text   = text
        self.rating = rating
        self.place  = place
        self.user   = user
        self.validate()

        if hasattr(self.place, 'add_review'):
            self.place.add_review(self)

    def validate(self):
        if not self.text or not isinstance(self.text, str):
            raise ValueError("Review text is required and must be a string")
        if not isinstance(self.rating, int):
            raise ValueError("Rating must be an integer")
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        from app.models.place import Place
        if not isinstance(self.place, Place):
            raise ValueError("Place must be a Place instance")

        from app.models.user import User
        if not isinstance(self.user, User):
            raise ValueError("User must be a User instance")
