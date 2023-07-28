from datetime import datetime
from sqlalchemy import ForeignKey

from app import db
from app.models.user_models import User


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'location': self.location
        }
        return data

    def from_dict(self, data):
        self.name = data['name']
        self.location = data['location']
        return self

    def alternative_from_dict(self, data):
        for field in ['name', 'location']:
            if field in data:
                setattr(self, field, data[field])
        return self


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    # address = db.Column(db.String(200))
    hospital = db.Column(db.Integer, ForeignKey(Hospital.id))

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'phone_number': self.phone_number,
            'email': self.email,
            # 'address': self.address,
            'hospital': self.hospital
        }
        return data

    def from_dict(self, data):
        self.name = data['name']
        self.department = data['department']
        self.phone_number = data['phone_number']
        self.email = data['email']
        # self.address = data['address']
        self.hospital = data['hospital']
        return self

    def alternative_from_dict(self, data):
        for field in ['name', 'department', 'phone_number', 'email', 'hospital']:
            if field in data:
                setattr(self, field, data[field])
        return self


class DoctorSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100))
    location = db.Column(db.String(200))
    hospital_id = db.Column(db.Integer, db.ForeignKey(Hospital.id))
    search_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    patient_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def to_dict(self):
        data = {
            'id': self.id,
            'department': self.department,
            'location': self.location,
            'patient_id': self.patient_id,
            'hospital_id': self.hospital_id,
            'search_date': self.search_date.isoformat()
        }
        return data

    def from_dict(self, data):
        for field in ['department', 'location', 'search_date', 'patient_id', 'hospital_id']:
            if field in data:
                setattr(self, field, data[field])
        return self


class DoctorContactRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey(Doctor.id), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        data = {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'patient_id': self.patient_id,
            'request_date': self.request_date.isoformat()
        }
        return data

    def from_dict(self, data):
        self.doctor_id = data['doctor_id']
        self.patient_id = data['patient_id']
        if 'request_date' in data:
            self.request_date = data['request_date']
        return self

    def alternative_from_dict(self, data):
        for field in ['doctor_id', 'patient_id', 'request_date']:
            if field in data:
                setattr(self, field, data[field])
        return self
