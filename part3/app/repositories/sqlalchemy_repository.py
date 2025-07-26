#!/usr/bin/python3
"""
SQLAlchemy repository for database operations
"""
from app.extensions import db
from datetime import datetime

class SQLAlchemyRepository:
    def __init__(self, model):
        self.model = model
    
    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        db.session.refresh(obj)
        return obj
    
    def get(self, obj_id):
        return self.model.query.get(obj_id)
    
    def get_all(self):
        return self.model.query.all()
    
    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if key not in ['id', 'created_at']:
                    setattr(obj, key, value)
            obj.updated_at = datetime.utcnow()
            db.session.commit()
            db.session.refresh(obj)
            return obj
        return None
    
    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False
        
    def get_by_attribute(self, attr_name, attr_value):
        filter_kwargs = {attr_name: attr_value}
        return self.model.query.filter_by(**filter_kwargs).first()
