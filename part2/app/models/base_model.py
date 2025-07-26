#!/usr/bin/python3
"""
Base model for the HBnB project
"""
import uuid
from datetime import datetime


class BaseModel:
    """Base class for all models in the HBnB application"""

    def __init__(self, id=None, created_at=None, updated_at=None, **kwargs):
        """
        Initialize a new BaseModel instance

        Args:
            id (str, optional): The ID of the instance. Defaults to a new UUID.
            created_at (datetime, optional): Creation timestamp. Defaults to now.
            updated_at (datetime, optional): Update timestamp. Defaults to now.
            **kwargs: Additional attributes to set
        """
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
        """Update the updated_at timestamp when the object is modified"""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """
        Update attributes based on a dictionary of values

        Args:
            data (dict): Dictionary of attributes to update
        """
        for key, value in data.items():
            if key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """
        Convert the instance to a dictionary for serialization

        Returns:
            dict: Dictionary representation of the instance
        """
        result = self.__dict__.copy()
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        return result

    def validate(self):
        """
        Validate the instance attributes

        Raises:
            ValueError: If validation fails
        """
        pass