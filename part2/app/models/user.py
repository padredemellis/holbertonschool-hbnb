#!/usr/bin/python3
"""
User model for the HBnB project
"""
import re
from app.models.base_model import BaseModel


class User(BaseModel):
    """User class for representing users in the HBnB application"""

    def __init__(self, first_name, last_name, email, is_admin=False, **kwargs):
        """
        Initialize a new User instance

        Args:
            first_name (str): First name of the user
            last_name (str): Last name of the user
            email (str): Email address of the user
            is_admin (bool, optional): Admin status. Defaults to False.
            **kwargs: Additional attributes to set
        """
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.validate()

    def validate(self):
        """
        Validate user attributes

        Raises:
            ValueError: If any validation fails
        """
        if not self.first_name or not isinstance(self.first_name, str):
            raise ValueError("First name is required and must be a string")
        if len(self.first_name) > 50:
            raise ValueError("First name must be at most 50 characters")

        if not self.last_name or not isinstance(self.last_name, str):
            raise ValueError("Last name is required and must be a string")
        if len(self.last_name) > 50:
            raise ValueError("Last name must be at most 50 characters")

        if not self.email or not isinstance(self.email, str):
            raise ValueError("Email is required and must be a string")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValueError("Invalid email format")

        if not isinstance(self.is_admin, bool):
            raise ValueError("is_admin must be a boolean")
