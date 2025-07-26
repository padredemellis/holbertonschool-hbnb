#!/usr/bin/python3
"""
Amenity model for the HBnB project
"""
from app.models.base_model import BaseModel
from app.extensions import db
from datetime import datetime

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.validate()

    def validate(self):
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Amenity must have a valid name")
        
        if self.description and not isinstance(self.description, str):
            raise ValueError("Description must be a string")
        
    def update(self, data):
        if 'name' in data:
            self.name = data['name']
        if 'description' in data:
            self.description = data['description']
        
        self.updated_at = datetime.utcnow()
        
        self.validate()
        return self
