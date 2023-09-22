from flask import jsonify, request

from app.controller.doctor_helper_controller import is_valid_hospital_data, is_valid_doctor_search_data, \
    check_doctor_data, is_valid_doctor_request_data, check_doctor_update_data
from app.service import doctor_service
from errors import bad_request


def get_all_doctors_controller():
    doctors = doctor_service.get_all_doctors_service()
    return jsonify(doctors)


def get_doctor_by_name_controller(name):
    if not name or not isinstance(name, str):
        return bad_request("Invalid format")
    doctor = doctor_service.get_doctor_by_name_service(name)
    if doctor:
        return jsonify(doctor)
    else:
        return jsonify({'error': 'Doctor not found'}), 404


def search_doctors_by_department_controller(department):
    if not department or not isinstance(department, str) or department == '':
        return bad_request("Invalid format")
    doctors = doctor_service.search_doctors_by_department_service(department)
    return jsonify(doctors)


def add_doctor_controller():
    data = request.get_json()
    check_failed = check_doctor_data(data)
    if check_failed:
        return check_failed
    if doctor_service.add_doctor_service(data):
        return jsonify({'message': 'Doctor added successfully'}), 200
    else:
        return jsonify({'error': 'Cannot add Doctor'}), 403


def update_doctor_controller(doctor_id):
    data = request.get_json()
    check_failed = check_doctor_update_data(data, doctor_id)
    if check_failed:
        return check_failed
    if doctor_service.update_doctor_service(doctor_id, data):
        return jsonify({'message': 'Doctor information updated successfully'}), 200
    else:
        return jsonify({'error': 'Cannot update Doctor Information'}), 403


def get_doctors_by_name_includes_phrase_controller(phrase):
    if not phrase or not isinstance(phrase, str) or phrase == '':
        return bad_request("Invalid format")
    doctors = doctor_service.get_doctors_by_name_includes_phrase_service(phrase)
    return jsonify(doctors)


def get_doctors_in_hospital_controller(hospital_name):
    if not hospital_name or not isinstance(hospital_name, str) or hospital_name == '':
        return bad_request("Invalid format")
    doctors = doctor_service.get_doctors_in_hospital_by_name_service(hospital_name)
    return jsonify(doctors)


def add_hospital_controller():
    data = request.get_json()
    if not is_valid_hospital_data(data):
        return bad_request("Invalid hospital data")

    if doctor_service.add_hospital_service(data):
        return jsonify({'message': 'Hospital created successfully'}), 200
    else:
        return jsonify({'error': 'Cannot create Hospital'}), 403


def doctor_search_controller(user_id):
    data = request.get_json()
    if not is_valid_doctor_search_data(data):
        return bad_request("Invalid doctor search data")

    doctors = doctor_service.doctor_search_service(data, user_id)
    if doctors:
        return jsonify(doctors)
    else:
        return jsonify({'error': 'System Error'}), 403


def add_doctor_contact_request_controller(user_id):
    data = request.get_json()
    if not is_valid_doctor_request_data(data):
        return bad_request("Invalid doctor contact request data")
    if not doctor_service.get_doctor_by_id_service(data['doctor_id']):
        return bad_request("Cannot find doctor")
    if doctor_service.add_doctor_contact_request_service(data, user_id):
        return jsonify({'message': 'Doctor contact request created successfully'}), 200
    else:
        return jsonify({'error': 'Cannot create Doctor contact request'}), 403


def get_hospital_id_by_name_controller(hospital_name):
    if not hospital_name or not isinstance(hospital_name, str) or hospital_name == '':
        return bad_request("Invalid format")

    hospital_id = doctor_service.get_hospital_id_by_name_service(hospital_name)
    if hospital_id is not None:
        return jsonify({'hospital_id': hospital_id})
    else:
        return jsonify({'error': 'Hospital not found'}), 404


def get_doctor_by_department_controller(department):
    if not department or not isinstance(department, str) or department == '':
        return bad_request("Invalid format")

    doctors = doctor_service.get_doctors_by_department_service(department)
    if doctors:
        return jsonify(doctors)
    else:
        return jsonify({'error': 'No doctors found for the given department'}), 404


def get_all_hospitals_controller():
    hospitals = doctor_service.get_all_hospitals_service()
    return jsonify(hospitals)