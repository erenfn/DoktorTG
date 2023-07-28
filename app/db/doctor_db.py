from typing import Optional, List
from sqlalchemy import func
from app import db
from app.models.doctor_models import Doctor, Hospital, DoctorSearch

def get_doctor_by_id_db(doctor_id):
    return db.session.query(Doctor).filter(Doctor.id == doctor_id).first()


def get_doctors_db(name=None, department=None) -> List[Doctor]:
    if not any(get_doctors_db.__code__.co_varnames):
        return []
    elif name:
        return db.session.query(Doctor).filter(func.lower(Doctor.name) == func.lower(name)).all()
    else:
        return db.session.query(Doctor).filter(func.lower(Doctor.department) == func.lower(department)).all()


def get_doctors_unique_db(email=None, phone_number=None) -> Optional[Doctor]:
    if not any(get_doctors_db.__code__.co_varnames):
        return None
    elif email:
        return db.session.query(Doctor).filter(Doctor.email == email).first()
    else:
        return db.session.query(Doctor).filter(Doctor.phone_number == phone_number).first()


def insert_db(x):
    try:
        db.session.add(x)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def get_all_doctors_db():
    return db.session.query(Doctor).all()


def search_doctors_by_department_db(department):
    return db.session.query(Doctor).filter(Doctor.department.ilike('%{}%'.format(department))).all()


def update_doctor_in_db(doctor):
    try:
        db.session.merge(doctor)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def delete_doctor_from_db(doctor_id):
    doctor = db.session.query(Doctor).get(doctor_id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        return True
    else:
        return False


def get_doctors_by_name_includes_phrase_db(phrase):
    return db.session.query(Doctor).filter(Doctor.name.ilike(f'%{phrase}%')).all()


def get_doctors_in_hospital_db(hospital_name: str = None, hospital_id: int = None) -> List[Doctor]:
    if hospital_name is None and hospital_id is None:
        return []
    if hospital_name:
        return db.session.query(Doctor).join(Hospital).filter(Hospital.name == hospital_name).all()
    else:
        return db.session.query(Doctor).join(Hospital).filter(Hospital.id == hospital_id).all()



def get_hospital_id_by_name_db(hospital_name) -> Hospital:
    hospital = db.session.query(Hospital).filter(Hospital.name == hospital_name).first()
    if hospital:
        return hospital.id
    else:
        return None



def search_doctors_db(doctor_search: DoctorSearch) -> List:
    query = db.session.query(Doctor)

    if doctor_search.hospital_id is not None:
        query = query.filter(Doctor.hospital == doctor_search.hospital_id)

    if doctor_search.department is not None:
        query = query.filter(Doctor.department.ilike(f'%{doctor_search.department}%'))

    if doctor_search.location is not None:
        query = query.join(Hospital, Doctor.hospital == Hospital.id)
        # Filter the doctors based on the hospital location
        query = query.filter(Hospital.location.ilike(f'%{doctor_search.location}%'))

    return query.all()

