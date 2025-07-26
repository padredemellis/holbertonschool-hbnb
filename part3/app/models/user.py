#!/usr/bin/python3
"""
User model for the HBnB project
"""
from datetime import datetime
from app.models.base_model import BaseModel
from app.extensions import db, bcrypt


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(128), nullable=False)
    last_name  = db.Column(db.String(128), nullable=False)
    email      = db.Column(db.String(128), unique=True, nullable=False)
    _password  = db.Column('password', db.String(128), nullable=False)
    is_admin   = db.Column(db.Boolean(), default=False)

    reviews = db.relationship(
        'Review',
        back_populates='user',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_name = kwargs.get('first_name', '')
        self.last_name  = kwargs.get('last_name', '')
        self.email      = kwargs.get('email', '')
        self.is_admin   = kwargs.get('is_admin', False)

        raw_pw = kwargs.get('password')
        if raw_pw:
            self.hash_password(raw_pw)

    def hash_password(self, raw_password):
        self._password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self._password, raw_password)

    def verify_password(self, raw_password):
        return self.check_password(raw_password)

    def update(self, data):
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'email' in data:
            self.email = data['email']
        if 'password' in data:
            self.hash_password(data['password'])
        if 'is_admin' in data:
            self.is_admin = data['is_admin']

        self.updated_at = datetime.utcnow()
        return self
