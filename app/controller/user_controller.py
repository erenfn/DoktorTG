import json
from flask import jsonify, request

from app.controller.helper_controller import is_valid_email, is_valid_name, is_valid_password, is_integer
from app.service import user_service
from errors import bad_request


def get_all_users_controller():
    users = user_service.get_all_users_service()
    return jsonify(users)


def get_user_by_phone_number_controller(phone):
    user = user_service.get_user_by_phone_number_service(phone)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404


def get_users_by_name_includes_letter_controller(letter):
    if not letter or len(letter) != 1:
        return bad_request("Invalid letter provided")

    users = user_service.get_users_by_name_includes_letter_service(letter)
    return jsonify(users)


def set_user_phone_number_controller(user_id):
    data = request.get_json()
    new_phone_number = data.get('phone')

    if not new_phone_number:
        return bad_request("Phone number not provided")

    if not is_integer(new_phone_number):
        return bad_request("Phone number is not valid")

    if user_service.get_user_by_phone_number_service(data['phone']) == new_phone_number:
        return bad_request("Phone number must be unique")

    if user_service.set_user_phone_number_service(user_id, new_phone_number):
        return jsonify({'message': 'Phone number updated successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404


def add_n_test_users_controller():
    data = request.get_json()
    added_users = 0

    for user in data:
        if _create_new_user_controller_test(user):
            added_users += 1

    return json.dumps(added_users)


def _create_new_user_controller_test(data):
    if 'name' not in data or 'surname' not in data or 'phone' not in data or 'email' not in data:
        return False

    if not isinstance(data['name'], str):
        return False

    if not is_integer(data['phone']):
        return False

    if user_service.get_user_by_phone_number_service(data['phone']):
        return False

    if user_service.create_new_user_service(data):
        return True
    else:
        return False


def signup_controller():
    data = request.get_json()
    fields = ['email', 'password', 'phone', 'name', 'surname']

    if not all(field in data for field in fields):
        return bad_request("Missing Information")

    if not all(isinstance(data[field], str) for field in fields):
        return bad_request('Wrong format')

    if not is_integer(data['phone']):
        return bad_request('Phone number must be a number')

    if not is_valid_email(data['email']):
        return bad_request('Invalid email format.')

    if not is_valid_name(data['name']) and is_valid_name(data['surname']):
        return bad_request('Name or surname should not contain any numbers.')

    if not is_valid_password(data['password']):
        return bad_request("Not a valid password")

    if user_service.get_user_by_email_service(data['email']):
        return bad_request('Email already exists')

    if user_service.get_user_by_phone_number_service(data['phone']):
        return bad_request('Phone already exists')

    signup_info = user_service.signup_service(data)
    if signup_info:
        return jsonify(token=signup_info)
    else:
        return bad_request("System Error")


def login_controller():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify(message='Missing email or password'), 400

    user = user_service.authenticate_service(email, password)

    if user:
        token = user.get_token()
        return jsonify(token=token), 200
    else:
        return jsonify(message='Invalid email or password'), 401


def get_my_information(user_id):
    user = user_service.get_user_by_id_service(user_id)
    return jsonify(user)
