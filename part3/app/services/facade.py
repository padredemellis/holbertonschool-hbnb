#!/usr/bin/python3

from app.repositories.user_repository import UserRepository
from app.repositories.place_repository import PlaceRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.amenity_repository import AmenityRepository
from app.extensions import db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.utils.validators import validate_user, validate_place, validate_amenity

class HBnBFacade:

    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()

    @validate_user
    def create_user(self, user_data):
        if 'password' not in user_data or not user_data['password']:
            raise ValueError("Password is required")
        user = User(**user_data)
        return self.user_repo.add(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    @validate_amenity
    def create_amenity(self, data):
        amenity = Amenity(**data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        return self.amenity_repo.update(amenity_id, data)

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

    @validate_place
    def create_place(self, place_data):
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError(f"Owner with ID {place_data['owner_id']} not found")

        place = Place(
            place_data['title'],
            place_data.get('description', ''),
            float(place_data['price']),
            float(place_data['latitude']),
            float(place_data['longitude']),
            owner
        )

        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
                place.add_amenity(amenity)

        return self.place_repo.add(place)

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        return place.to_dict() if place else None

    def get_all_places(self):
        return [p.to_dict() for p in self.place_repo.get_all()]

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    def create_review(self, data):
        user  = self.user_repo.get(data['user_id'])
        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        place = self.place_repo.get(data['place_id'])
        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        rev = Review(
            data['text'],
            int(data['rating']),
            place,
            user
        )
        return self.review_repo.add(rev)

    def get_review(self, review_id):
        rev = self.review_repo.get(review_id)
        return rev.to_dict() if rev else None

    def get_all_reviews(self):
        return [r.to_dict() for r in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return [r.to_dict() for r in place.get_reviews()]

    def get_amenities_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return [
            {
                'id': amenity.id,
                'name': amenity.name
            }
            for amenity in place.amenities
        ]

    def add_amenity_to_place(self, place_id, amenity_id):
        place   = self.place_repo.get(place_id)
        if not place:
            return None
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        place.add_amenity(amenity)
        db.session.commit()
        return {'id': amenity.id, 'name': amenity.name}

    def remove_amenity_from_place(self, place_id, amenity_id):
        place = self.place_repo.get(place_id)
        if not place:
            return False
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False
        if amenity in place.amenities:
            place.amenities.remove(amenity)
        db.session.commit()
        return True

    def update_review(self, review_id, data):
        rev = self.review_repo.update(review_id, data)
        return rev.to_dict() if rev else None

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)

_facade = HBnBFacade()

def create_user(user_data):
    return _facade.create_user(user_data)

def get_user(user_id):
    return _facade.get_user(user_id)

def get_all_users():
    return _facade.get_all_users()

def update_user(user_id, data):
    return _facade.update_user(user_id, data)

def get_user_by_email(email):
    return _facade.get_user_by_email(email)

def create_amenity(data):
    return _facade.create_amenity(data)

def get_amenity(amenity_id):
    return _facade.get_amenity(amenity_id)

def get_all_amenities():
    return _facade.get_all_amenities()

def update_amenity(amenity_id, data):
    return _facade.update_amenity(amenity_id, data)

def delete_amenity(amenity_id):
    return _facade.delete_amenity(amenity_id)

def create_place(place_data):
    return _facade.create_place(place_data)

def get_place(place_id):
    return _facade.get_place(place_id)

def get_all_places():
    return _facade.get_all_places()

def update_place(place_id, data):
    return _facade.update_place(place_id, data)

def delete_place(place_id):
    return _facade.delete_place(place_id)

def get_review(review_id):
    return _facade.get_review(review_id)

def get_all_reviews():
    return _facade.get_all_reviews()

def get_reviews_by_place(place_id):
    return _facade.get_reviews_by_place(place_id)

def update_review(review_id, data):
    return _facade.update_review(review_id, data)

def delete_review(review_id):
    return _facade.delete_review(review_id)

def get_amenities_by_place(place_id):
    return _facade.get_amenities_by_place(place_id)

def add_amenity_to_place(place_id, amenity_id):
    return _facade.add_amenity_to_place(place_id, amenity_id)

def remove_amenity_from_place(place_id, amenity_id):
    return _facade.remove_amenity_from_place(place_id, amenity_id)