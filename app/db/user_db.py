from typing import Optional
from app import db
from app.models.user_models import User


def get_user_by_phone_number(phone):
    return db.session.query(User).filter(User.phone == phone).first()


def insert_new_user_to_db(user):
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def get_all_users():
    return db.session.query(User).all()


def get_users_by_name_includes_letter(letter):
    return db.session.query(User).filter(User.name.ilike('%{}%'.format(letter))).all()


def set_user_phone_number(user_id, new_phone_number):
    user = db.session.query(User).get(user_id)
    if user:
        try:
            user.phone = new_phone_number
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
    else:
        return False


def get_user_by_email_db(email):
    return db.session.query(User).filter(User.email == email).first()


def get_user_by_id_db(user_id) -> Optional[User]:
    return db.session.query(User).get(user_id)