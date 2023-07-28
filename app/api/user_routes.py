from app.api import bp
from app.auth import token_auth
from app.controller import user_controller


@bp.route('/getAllUsers', methods=["GET"])
def get_all_users():
    return user_controller.get_all_users_controller()


@bp.route('/getUserByPhoneNumber/<phone>', methods=["GET"])
def get_user_by_phone_number(phone):
    return user_controller.get_user_by_phone_number_controller(phone)


@bp.route('/getUsersByNameIncludesLetter/<letter>', methods=["GET"])
def get_users_by_name_includes_letter(letter):
    return user_controller.get_users_by_name_includes_letter_controller(letter)


@bp.route('/setUserPhoneNumber/<user_id>', methods=["PUT"])
@token_auth.login_required
def set_user_phone_number(user_id):
    return user_controller.set_user_phone_number_controller(user_id)


@bp.route('/addNTestUsers', methods=['POST'])
def add_n_test_users():
    return user_controller.add_n_test_users_controller()


@bp.route('/signup', methods=['POST'])
def signup():
    return user_controller.signup_controller()


@bp.route('/login', methods=['POST'])
def login():
    return user_controller.login_controller()


@bp.route('/getMyInfo', methods=['GET'])
@token_auth.login_required
def get_my_information():
    return user_controller.get_my_information(token_auth.current_user().id)
