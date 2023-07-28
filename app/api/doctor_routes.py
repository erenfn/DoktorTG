from app.api import bp
from app.auth import token_auth
from app.controller import doctor_controller


@bp.route('/getAllDoctors', methods=["GET"])
def get_all_doctors():
    return doctor_controller.get_all_doctors_controller()


@bp.route('/getDoctorByName/<name>', methods=["GET"])
def get_doctor_by_name(name):
    return doctor_controller.get_doctor_by_name_controller(name)


@bp.route('/searchDoctorsByDepartment/<department>', methods=["GET"])
def search_doctors_by_department(department):
    return doctor_controller.search_doctors_by_department_controller(department)


@bp.route('/addDoctor', methods=["POST"])
def add_doctor():
    return doctor_controller.add_doctor_controller()


@bp.route('/addHospital', methods=["POST"])
def add_hospital():
    return doctor_controller.add_hospital_controller()


# @bp.route('/addDoctorSearch', methods=["POST"])
# @token_auth.login_required
# def add_doctor_search():
#     return doctor_controller.add_doctor_search_controller(token_auth.current_user().id)

@bp.route('/doctorSearch', methods=["GET"])
@token_auth.login_required
def doctor_search():
    return doctor_controller.doctor_search_controller(token_auth.current_user().id)


@bp.route('/addDoctorContactRequest', methods=["POST"])
@token_auth.login_required
def add_doctor_contact_request():
    return doctor_controller.add_doctor_contact_request_controller(token_auth.current_user().id)


@bp.route('/updateDoctor/<int:doctor_id>', methods=["PUT"])
def update_doctor(doctor_id):
    return doctor_controller.update_doctor_controller(doctor_id)


@bp.route('/getDoctorsByNameIncludesPhrase/<phrase>', methods=["GET"])
def get_doctors_by_name_includes_phrase(phrase):
    return doctor_controller.get_doctors_by_name_includes_phrase_controller(phrase)


@bp.route('/getDoctorsInHospital/<hospital_name>', methods=["GET"])
def get_doctors_in_hospital(hospital_name):
    return doctor_controller.get_doctors_in_hospital_controller(hospital_name)


@bp.route('/getHospitalByName/<hospital_name>', methods=["GET"])
def get_hospital_id_by_name(hospital_name):
    return doctor_controller.get_hospital_id_by_name_controller(hospital_name)