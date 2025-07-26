#!/usr/bin/python3
"""
Repository module for the HBnB project
"""
from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract base class for repositories"""
    
    @abstractmethod
    def add(self, obj):
        """Add an object to the repository"""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Get an object by ID"""
        pass

    @abstractmethod
    def get_all(self):
        """Get all objects"""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object by ID"""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by ID"""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by attribute"""
        pass


class InMemoryRepository(Repository):
    """In-memory repository implementation"""
    
    def __init__(self):
        """Initialize the repository"""
        self._storage = {}

    def add(self, obj):
        """Add an object to the repository"""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Get an object by ID"""
        return self._storage.get(obj_id)

    def get_all(self):
        """Get all objects"""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object by ID"""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Delete an object by ID"""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by attribute"""
        return next((obj for obj in self._storage.values() 
                   if getattr(obj, attr_name) == attr_value), None)