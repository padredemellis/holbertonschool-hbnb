#!/usr/bin/python3
"""
In-memory repository for the HBnB application
"""


class InMemoryRepository:
    """In-memory repository for storing and retrieving data"""

    def __init__(self):
        """Initialize an empty repository"""
        self._storage = {}

    def add(self, obj):
        """
        Add an object to the repository

        Args:
            obj: Object to add (must have an id attribute)
        """
        if not hasattr(obj, 'id'):
            raise ValueError("Object must have an id attribute")
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        """
        Get an object by ID

        Args:
            obj_id: ID of the object to retrieve

        Returns:
            Object if found, None otherwise
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Get all objects in the repository

        Returns:
            List of all objects
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update an object in the repository
        
        Args:
            obj_id: ID of the object to update
        data: Dictionary of attributes to update

        Returns:
            Updated object if found, None otherwise
        """
        obj = self.get(obj_id)
        if not obj:
            return None
        
        try:
            if hasattr(obj, 'update'):
                updated_obj = obj.update(data)
                return updated_obj
            else:
                for key, value in data.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                return obj
        except Exception as e:
            print(f"Error in repository update: {str(e)}")
            raise

    def delete(self, obj_id):
        """
        Delete an object from the repository

        Args:
            obj_id: ID of the object to delete

        Returns:
            True if deleted, False otherwise
        """
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """
        Get an object by a specific attribute value

        Args:
            attr_name: Name of the attribute to check
            attr_value: Value of the attribute to match

        Returns:
            First object that matches the attribute value, or None
        """
        for obj in self._storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None
