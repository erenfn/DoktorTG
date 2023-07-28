from flask import jsonify

from app.db import doctor_db
from app.models.doctor_models import Doctor, Hospital, DoctorSearch, DoctorContactRequest
from typing import Optional, Dict


def get_doctor_by_id_service(doctor_id) -> Optional[Dict]:
    doctor = doctor_db.get_doctor_by_id_db(doctor_id)
    if doctor:
        return doctor.to_dict()
    else:
        return None


def search_doctors_by_department_service(department):
    doctors = doctor_db.search_doctors_by_department_db(department)
    return [doctor.to_dict() for doctor in doctors]


def get_all_doctors_service():
    doctors = doctor_db.get_all_doctors_db()
    return [doctor.to_dict() for doctor in doctors]


def add_doctor_service(data):
    doctor = Doctor().from_dict(data)
    return doctor_db.insert_db(doctor)


def update_doctor_service(doctor_id, data):
    doctor = doctor_db.get_doctor_by_id_db(doctor_id)
    if doctor:
        doctor.alternative_from_dict(data)
        return doctor_db.update_doctor_in_db(doctor)
    else:
        return None


def delete_doctor_service(doctor_id):
    return doctor_db.delete_doctor_from_db(doctor_id)


def get_doctors_by_name_includes_phrase_service(phrase):
    doctors = doctor_db.get_doctors_by_name_includes_phrase_db(phrase)
    return [doctor.to_dict() for doctor in doctors]


def get_doctors_in_hospital_by_name_service(hospital_name):
    doctors = doctor_db.get_doctors_in_hospital_db(hospital_name=hospital_name)
    return [doctor.to_dict() for doctor in doctors]


def get_doctors_in_hospital_by_id_service(hospital_id):
    doctors = doctor_db.get_doctors_in_hospital_db(hospital_id=hospital_id)
    return [doctor.to_dict() for doctor in doctors]


def get_doctor_by_name_service(name):
    doctors = doctor_db.get_doctors_db(name=name)
    return [doctor.to_dict() for doctor in doctors]


def add_hospital_service(data):
    hospital = Hospital().from_dict(data)
    return doctor_db.insert_db(hospital)


def doctor_search_service(data, user_id):
    data['patient_id'] = user_id
    doctor_search = DoctorSearch().from_dict(data)
    if not doctor_db.insert_db(doctor_search):
        return None

    doctors = doctor_db.search_doctors_db(doctor_search)
    return [doctor.to_dict() for doctor in doctors]


def add_doctor_contact_request_service(data, user_id):
    data['patient_id'] = user_id
    doctor_contact_request = DoctorContactRequest().from_dict(data)
    return doctor_db.insert_db(doctor_contact_request)


def get_hospital_id_by_name_service(hospital_name):
    hospital = doctor_db.get_hospital_id_by_name_db(hospital_name)
    return hospital.to_dict()


def get_doctors_by_department_service(department):
    doctors = doctor_db.get_doctors_db(department=department)
    return [doctor.to_dict() for doctor in doctors]


def get_doctor_by_phone_service(phone):
    doctor = doctor_db.get_doctors_unique_db(phone_number=phone)
    if doctor:
        return doctor.to_dict()
    else:
        return doctor


def get_doctor_by_email_service(email):
    doctor = doctor_db.get_doctors_unique_db(email=email)
    if doctor:
        return doctor.to_dict()
    else:
        return doctor
