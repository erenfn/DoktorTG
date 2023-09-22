from app.db import user_db
from app.models.user_models import User
from typing import Optional


def get_user_by_phone_number_service(phone):
    user = user_db.get_user_by_phone_number(phone)
    if user:
        return user.to_dict()
    else:
        return None


def create_new_user_service(data):
    user = User()
    user.from_dict(data)
    return user_db.insert_new_user_to_db(user)


def get_all_users_service():
    users = user_db.get_all_users()
    return [user.to_dict() for user in users]


def get_users_by_name_includes_letter_service(letter):
    users = user_db.get_users_by_name_includes_letter(letter)
    return [user.to_dict() for user in users]


def set_user_phone_number_service(user_id, new_phone_number):
    return user_db.set_user_phone_number(user_id, new_phone_number)


def signup_service(data):
    new_user = User()
    new_user.set_password(data['password'])
    new_user.from_dict(data)
    if user_db.insert_new_user_to_db(new_user):
        return new_user.get_token(), new_user.name
    return False


def get_user_by_email_service(email):
    return user_db.get_user_by_email_db(email)


def authenticate_service(email, password) -> Optional[User]:
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None


def get_user_by_id_service(user_id) -> Optional[dict]:
    user = user_db.get_user_by_id_db(user_id)
    if user:
        return user.to_dict()
    else:
        return None
