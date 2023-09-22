from app.controller.helper_controller import is_integer, is_valid_email, is_valid_name
from app.service import doctor_service
from errors import bad_request


def is_valid_doctor_request_data(data):
    fields = {'doctor_id'}
    return all(field in data for field in fields) \
        and all(isinstance(data[field], int) for field in fields)


def is_valid_doctor_search_data(data):
    fields = {'department', 'location', 'hospital_id'}

    if 'hospital_id' in data and not isinstance(data['hospital_id'], int):
        return False
    if 'department' in data and not isinstance(data['department'], str):
        return False
    if 'location' in data and not isinstance(data['location'], str):
        return False
    return any(field in data for field in fields)


def is_valid_hospital_data(data):
    fields = {'name', 'location'}
    return all(field in data for field in fields) \
        and all(isinstance(data[field], str) for field in fields)


def is_valid_doctor_data(data):
    fields = {'name', 'department', 'phone_number', 'email', 'hospital'}
    return all(field in data for field in fields) \
        and all(isinstance(data[field], str) for field in fields - {'hospital'}) \
        and is_integer(data['hospital'])


def is_valid_doctor_update_data(data):
    fields = {'name', 'department', 'phone_number', 'email', 'hospital'}

    if 'hospital' in data and not isinstance(data['hospital'], int):
        return False

    for field in fields - {'hospital'}:
        if field in data and not isinstance(data[field], str):
            return False

    return any(field in data for field in fields)


def check_doctor_update_data(data, doctor_id):
    if not data or not is_valid_doctor_update_data(data):
        return bad_request("Invalid doctor data")

    if 'phone_number' in data:
        doctor = doctor_service.get_doctor_by_phone_service(data['phone_number'])
        if doctor and doctor['id'] != doctor_id:
            return bad_request('phone number already exists')
        if not is_integer(data['phone_number']):
            return bad_request('Phone number must be a number')

    if 'email' in data:
        doctor = doctor_service.get_doctor_by_email_service(data['email'])
        if doctor and doctor['id'] != doctor_id:
            return bad_request('email already exists')
        if not is_valid_email(data['email']):
            return bad_request('Invalid email format.')

    if 'name' in data and not is_valid_name(data['name']):
        return bad_request('Name should not contain any numbers.')

    return None


def check_doctor_data(data):
    if not data or not is_valid_doctor_data(data):
        return bad_request("Invalid doctor data")

    data['hospital'] = int(data['hospital'])

    if doctor_service.get_doctor_by_phone_service(data['phone_number']):
        return bad_request('phone number already exists')

    if doctor_service.get_doctor_by_email_service(data['email']):
        return bad_request('email already exists')

    if not is_integer(data['phone_number']):
        return bad_request('Phone number must be a number')

    if not is_valid_email(data['email']):
        return bad_request('Invalid email format.')

    if not is_valid_name(data['name']):
        return bad_request('Name should not contain any numbers.')

    if not doctor_service.get_hospital_by_id_service(data['hospital']):
        return bad_request('Hospital does not exist')

    return None
