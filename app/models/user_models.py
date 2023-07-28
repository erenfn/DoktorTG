import base64
import os
from datetime import datetime, timedelta
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(14), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(120))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'phone': self.phone,
            'email': self.email
        }
        return data

    def from_dict(self, d: dict):
        self.name = d['name']
        self.surname = d['surname']
        self.phone = d['phone']
        self.email = d['email']
        return self

    def alternative_from_dict(self, data):
        for field in ['name', 'surname', 'phone', 'email', 'password']:
            if field in data:
                setattr(self, field, data[field])
        return self

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=60 * 60 * 24 * 7):
        now = datetime.now()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        db.session.commit()
        return self.token

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.now():
            return None
        return user
