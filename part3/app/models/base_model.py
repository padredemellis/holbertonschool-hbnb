#!/usr/bin/python3
"""
Base model for the HBnB project
"""
import uuid
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, id=None, created_at=None, updated_at=None, **kwargs):
        self.id = id or str(uuid.uuid4())
        
        if created_at and isinstance(created_at, str):
            self.created_at = datetime.fromisoformat(created_at)
        else:
            self.created_at = created_at or datetime.utcnow()
            
        if updated_at and isinstance(updated_at, str):
            self.updated_at = datetime.fromisoformat(updated_at)
        else:
            self.updated_at = updated_at or self.created_at
            
        for key, value in kwargs.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)

    def save(self):
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            if key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                result[key] = value
                
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        return result

    def validate(self):
        pass
